import json
import logging

import requests
import werkzeug.http

from odoo import api, fields, models
from odoo.exceptions import AccessDenied, UserError
from odoo.addons.auth_signup.models.res_users import SignupError

from odoo.addons import base
base.models.res_users.USER_PRIVATE_FIELDS.append('oauth_access_token')

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    oauth_provider_id = fields.Many2one('auth.oauth.provider', string='OAuth Provider')
    oauth_uid = fields.Char(string='OAuth User ID', help="Oauth Provider user_id", copy=False)
    oauth_access_token = fields.Char(string='OAuth Access Token', readonly=True, copy=False)

    _sql_constraints = [
        ('uniq_users_oauth_provider_oauth_uid', 'unique(oauth_provider_id, oauth_uid)', 'OAuth UID must be unique per provider'),
    ]

    def _auth_oauth_rpc(self, endpoint, access_token):
        _logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>> _auth_oauth_rpc")
        # validate access token by requesting data to oidc user endpoint
        response = requests.get(endpoint, headers={'Authorization': 'Bearer %s' % access_token}, timeout=10)
        _logger.info(response)
        if response.ok: # nb: could be a successful failure
            return response.json()

        auth_challenge = werkzeug.http.parse_www_authenticate_header(
            response.headers.get('WWW-Authenticate'))
        if auth_challenge.type == 'bearer' and 'error' in auth_challenge:
            return dict(auth_challenge)
        _logger.info("=============================================")
        return {'error': 'invalid_request'}

    @api.model
    def _auth_oauth_validate(self, provider, access_token):
        """ return the validation data corresponding to the access token """
        oauth_provider = self.env['auth.oauth.provider'].browse(provider)
        validation = self._auth_oauth_rpc(oauth_provider.validation_endpoint, access_token)
        if validation.get("error"):
            raise Exception(validation['error'])
        if oauth_provider.data_endpoint:
            data = self._auth_oauth_rpc(oauth_provider.data_endpoint, access_token)
            validation.update(data)
        # unify subject key, pop all possible and get most sensible. When this
        # is reworked, BC should be dropped and only the `sub` key should be
        # used (here, in _generate_signup_values, and in _auth_oauth_signin)
        subject = next(filter(None, [
            validation.pop(key, None)
            for key in [
                'sub', # standard
                'id', # google v1 userinfo, facebook opengraph
                'user_id', # google tokeninfo, odoo (tokeninfo)
            ]
        ]), None)
        if not subject:
            _logger.error("missing subject identity")
            raise AccessDenied('Missing subject identity')
        validation['user_id'] = subject

        return validation

    @api.model
    def _generate_signup_values(self, provider, validation, params):
        oauth_uid = validation['user_id']
        email = validation.get('email', 'provider_%s_user_%s' % (provider, oauth_uid))
        name = validation.get('name', email)
        access_token = params['access_token']
        _logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>> _generate_signup_values")
        _logger.info(validation)
        _logger.info(params)
        _logger.info("=============================================")
        return {
            'name': name,
            'login': email,
            'email': email,
            'oauth_provider_id': provider,
            'oauth_uid': oauth_uid,
            'oauth_access_token': params['access_token'],
            'active': True,
        }

    @api.model
    def _auth_oauth_signin(self, provider, validation, params):
        """ retrieve and sign in the user corresponding to provider and validated access token
            :param provider: oauth provider id (int)
            :param validation: result of validation of access token (dict)
            :param params: oauth parameters (dict)
            :return: user login (str)
            :raise: AccessDenied if signin failed

            This method can be overridden to add alternative signin methods.
        """
        oauth_uid = validation['user_id']
        try:
            oauth_user = self.search([("oauth_uid", "=", oauth_uid), ('oauth_provider_id', '=', provider)])
            if not oauth_user:
                _logger.error("not oauth user")
                raise AccessDenied()
            assert len(oauth_user) == 1
            oauth_user.write({'oauth_access_token': params['access_token']})
            return oauth_user.login
        except AccessDenied as access_denied_exception:
            if self.env.context.get('no_user_creation'):
                return None
            state = json.loads(params['state'])
            token = state.get('t')
            _logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>> _auth_oauth_signin")
            _logger.info(params)
            _logger.info(state)
            _logger.info("=============================================")
            values = self._generate_signup_values(provider, validation, params)
            # signup
            try:
                # TODO: set role to user
                _logger.info("signup >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                login, _ = self.signup(values, token)
                _logger.info(login)
                return login
            except (SignupError, UserError):
                raise access_denied_exception

    @api.model
    def auth_oauth(self, provider, params):
        # Advice by Google (to avoid Confused Deputy Problem)
        # if validation.audience != OUR_CLIENT_ID:
        #   abort()
        # else:
        #   continue with the process
        access_token = params.get('access_token')
        validation = self._auth_oauth_validate(provider, access_token)

        # retrieve and sign in user
        login = self._auth_oauth_signin(provider, validation, params)
        if not login:
            _logger.error("not login")
            raise AccessDenied()
        # return user credentials
        return (self.env.cr.dbname, login, access_token)

    def _check_credentials(self, password, env):
        try:
            return super(ResUsers, self)._check_credentials(password, env)
        except AccessDenied:
            passwd_allowed = env['interactive'] or not self.env.user._rpc_api_keys_only()
            if passwd_allowed and self.env.user.active:
                res = self.sudo().search([('id', '=', self.env.uid), ('oauth_access_token', '=', password)])
                if res:
                    return
            raise

    def _get_session_token_fields(self):
        return super(ResUsers, self)._get_session_token_fields() | {'oauth_access_token'}
