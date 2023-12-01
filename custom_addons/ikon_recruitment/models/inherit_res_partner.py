import random
import werkzeug.urls

from collections import defaultdict
from datetime import datetime, timedelta

from odoo import api, exceptions, fields, models, _

class InheritRes(models.Model):
    _inherit = "res.partner"

    def _get_signup_url_for_action(self, url=None, action=None, view_type=None, menu_id=None, res_id=None, model=None):
        """ generate a signup url for the given partner ids and action, possibly overriding
            the url state components (menu_id, id, view_type) """

        res = dict.fromkeys(self.ids, False)
        for partner in self:
            base_url = partner.get_base_url()
            # when required, make sure the partner has a valid signup token
            if self.env.context.get('signup_valid') and not partner.user_ids:
                partner.sudo().signup_prepare()

            route = 'login'
            # the parameters to encode for the query
            query = {'db': self.env.cr.dbname}
            if self.env.context.get('create_user'):
                query['signup_email'] = partner.email

            signup_type = self.env.context.get('signup_force_type_in_url', partner.sudo().signup_type or '')
            if signup_type:
                route = 'reset_password' if signup_type == 'reset' else signup_type

            if partner.sudo().signup_token and signup_type:
                query['token'] = partner.sudo().signup_token
            elif partner.user_ids:
                query['login'] = partner.user_ids[0].login
            else:
                continue        # no signup token, no user, thus no signup url!

            if url:
                query['redirect'] = url
            else:
                fragment = dict()
                base = '/web#'
                if action == '/mail/view':
                    base = '/mail/view?'
                elif action:
                    fragment['action'] = action
                if view_type:
                    fragment['view_type'] = view_type
                if menu_id:
                    fragment['menu_id'] = menu_id
                if model:
                    fragment['model'] = model
                if res_id:
                    fragment['res_id'] = res_id

                if fragment:
                    query['redirect'] = base + werkzeug.urls.url_encode(fragment)

            signup_url = "/web/%s?%s" % (route, werkzeug.urls.url_encode(query))
            if not self.env.context.get('relative_url'):
                signup_url = werkzeug.urls.url_join("recruitment.ikonsultan.co.id", signup_url)
            res[partner.id] = signup_url

        return res