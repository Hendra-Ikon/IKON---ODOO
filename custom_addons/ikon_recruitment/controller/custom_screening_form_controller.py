import json
import base64

from odoo import http, fields
from odoo.http import request
from datetime import datetime
import logging
# from odoo.addons.website.controllers.form import WebsiteForm

from werkzeug.exceptions import BadRequest
from psycopg2 import IntegrityError
from odoo.exceptions import ValidationError, UserError

from odoo import http, SUPERUSER_ID, _, _lt
from odoo.tools import plaintext2html

from odoo.addons.base.models.ir_qweb_fields import nl2br

_logger = logging.getLogger(__name__)

class ScreeningController(http.Controller):

    @http.route('/web/screening-form/<string:token>', methods=['GET'], type='http', auth='public', website=True, csrf=False)
    def screening_form(self, token, **kw):
        # Search for the user based on the email
        email = kw.get('email')
        applicant = request.env['hr.applicant'].sudo().search([('email_from', '=', email)], limit=1)

        # Validate token and form expiration
        form = request.env['hr.applicant'].sudo().search([
            ('screening_token', '=', token),
            ('screening_token_expiration', '>=', fields.Datetime.now())
        ], limit=1)
        
        if not form:
            return request.render('http_routing.404')  # Handle case if expired
        
        _logger.info(f"User with email {email} found: {applicant.name}")

        data = {}
        if applicant:
            data = {
                'applicant': applicant,
            }
        
        # Pass form and user to the template
        return request.render('ikon_recruitment.custom_screening_form_website', data)
    
    # @http.route('/screening-thank-you', type='http', auth="public", multilang=False)
    # def screening_thank_you(self, **kwargs):
    #     # This is a workaround to don't add language prefix to <form action="/website/form/" ...>
    #     return request.render('ikon_recruitment.screening_thankyou')

    @http.route('/screening-form/submit', type='http', auth="public", methods=['POST'], multilang=False)
    def website_form_empty(self, **kwargs):
        # This is a workaround to don't add language prefix to <form action="/website/form/" ...>
        return ""
    
    # Override the '/website/form/<string:model_name>' route
    @http.route('/screening-form/submit/<string:model_name>', type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def website_form(self, model_name, **kwargs):
        # Partial CSRF check, only performed when session is authenticated, as there
        # is no real risk for unauthenticated sessions here. It's a common case for
        # embedded forms now: SameSite policy rejects the cookies, so the session
        # is lost, and the CSRF check fails, breaking the post for no good reason.
        csrf_token = request.params.pop('csrf_token', None)
        if request.session.uid and not request.validate_csrf(csrf_token):
            raise BadRequest('Session expired (invalid CSRF token)')
        try:
            # The except clause below should not let what has been done inside
            # here be committed. It should not either roll back everything in
            # this controller method. Instead, we use a savepoint to roll back
            # what has been done inside the try clause.
            with request.env.cr.savepoint():
                if request.env['ir.http']._verify_request_recaptcha_token('website_form'):
                    # request.params was modified, update kwargs to reflect the changes
                    kwargs = dict(request.params)
                    kwargs.pop('model_name')
                    return self._handle_website_form(model_name, **kwargs)
            error = _("Suspicious activity detected by Google reCaptcha.")
        except (ValidationError, UserError) as e:
            error = e.args[0]
        return json.dumps({
            'error': error,
        })
    
    def _handle_website_form(self, model_name, **kwargs):
        model_record = request.env['ir.model'].sudo().search([('model', '=', model_name), ('website_form_access', '=', True)])
        if not model_record:
            return json.dumps({
                'error': _("The form's specified model does not exist")
            })

        try:
            data = self.extract_data(model_record, kwargs)
        # If we encounter an issue while extracting data
        except ValidationError as e:
            # I couldn't find a cleaner way to pass data to an exception
            return json.dumps({'error_fields': e.args[0]})

        try:
            id_record = self.insert_record(request, model_record, data)
            
        # Some fields have additional SQL constraints that we can't check generically
        # Ex: crm.lead.probability which is a float between 0 and 1
        # TODO: How to get the name of the erroneous field ?
        except IntegrityError:
            return json.dumps(False)

        request.session['form_builder_model_model'] = model_record.model
        request.session['form_builder_model'] = model_record.name
        request.session['form_builder_id'] = id_record

        return json.dumps({'id': id_record})

    # Dict of dynamically called filters following type of field to be fault tolerent

    def identity(self, field_label, field_input):
        return field_input

    def integer(self, field_label, field_input):
        return int(field_input)

    def floating(self, field_label, field_input):
        return float(field_input)

    def html(self, field_label, field_input):
        return plaintext2html(field_input)

    def boolean(self, field_label, field_input):
        if field_input.lower() == 'true':
            return True
        elif field_input.lower() == 'false':
            return False
        return None

    def binary(self, field_label, field_input):
        return base64.b64encode(field_input.read())

    def one2many(self, field_label, field_input):
        return [int(i) for i in field_input.split(',')]

    def many2many(self, field_label, field_input, *args):
        return [(args[0] if args else (6, 0)) + (self.one2many(field_label, field_input),)]

    _input_filters = {
        'char': identity,
        'text': identity,
        'html': html,
        'date': identity,
        'datetime': identity,
        'many2one': integer,
        'one2many': one2many,
        'many2many': many2many,
        'selection': identity,
        'boolean': boolean,
        'integer': integer,
        'float': floating,
        'binary': binary,
        'monetary': floating,
    }

    # Extract all data sent by the form and sort its on several properties
    def extract_data(self, model, values):
        dest_model = request.env[model.sudo().model]

        data = {}
        
        # Field mapping for the form data to the hr.applicant fields
        authorized_fields = {
            'applicant_id': {'type':'many2one', 'required':'False'},
            'partner_name': {'type':'char', 'required':'False'},  # Full name
            'partner_phone': {'type':'char', 'required':'False'},  # Phone number
            'email_from': {'type':'char', 'required':'False'},  # Email
            'name': {'type':'char', 'required':'False'},  # Position applied for
            'screening_availability_status': {'type':'char', 'required':'False'},
            'screening_start_date': {'type':'date', 'required':'False'},
            'screening_current_emp_stats': {'type':'char', 'required':'False'},
            'screening_laptop_ownership': {'type':'selection', 'required':'False'},
            'screening_wfo_availability': {'type':'boolean', 'required':'False'},
            'screening_bank_client_agreement': {'type':'selection', 'required':'False'},
            'screening_bank_client_exp': {'type':'text', 'required':'False'},
            'screening_past_proj_desc': {'type':'text', 'required':'False'},
            'screening_in_five_years': {'type':'text', 'required':'False'},
            'current_salary': {'type':'integer', 'required':'False'},
            'screening_current_benefits': {'type':'text', 'required':'False'},
            'screening_net_or_gross': {'type':'selection', 'required':'False'},
            'expected_salary': {'type':'integer', 'required':'False'},
            'screening_other_expectation': {'type':'text', 'required':'False'},
            'screening_negotiability': {'type':'selection', 'required':'False'}
        }

        error_fields = []
        print(values)
        for field_name, field_value in values.items():
            # If it's a known field
            if field_name in authorized_fields:
                try:
                    input_filter = self._input_filters[authorized_fields[field_name]['type']]
                    data[field_name] = input_filter(self, field_name, field_value)
                except ValueError:
                    error_fields.append(field_name)

        # This function can be defined on any model to provide
        # a model-specific filtering of the record values
        # Example:
        # def website_form_input_filter(self, values):
        #     values['name'] = '%s\'s Application' % values['partner_name']
        #     return values
        if hasattr(dest_model, "website_form_input_filter"):
            data = dest_model.website_form_input_filter(request, data)

        print(data)
        missing_required_fields = [label for label, field in authorized_fields.items() if field['required'] and label not in data]
        if any(error_fields):
            raise ValidationError(error_fields + missing_required_fields)

        return data

    def insert_record(self, request, model, values):
        model_name = model.sudo().model
        applicant_id = values.get('applicant_id')
        if model_name == 'mail.mail':
            values.update({'reply_to': values.get('email_from')})
        record = request.env[model_name].with_user(SUPERUSER_ID).with_context(
            mail_create_nosubscribe=True,
            commit_assetsbundle=False,
        ).search([('id', '=', applicant_id)], limit=1)

        # Check if the record is found before calling write
        if record:
            record.write(values)
        else:
            raise ValueError(f"Record with applicant_id {applicant_id} not found.")

        return record.id