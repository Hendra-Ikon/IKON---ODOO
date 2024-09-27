from odoo import http
from odoo.http import request
from odoo.tools import plaintext2html
from odoo.exceptions import ValidationError
from odoo.addons.website.controllers.form import WebsiteForm  # Import the existing controller
from odoo import SUPERUSER_ID, _, _lt
import base64

class CustomWebsiteForm(WebsiteForm):
    
    # Constants string to make metadata readable on a text field

    _meta_label = _lt("Metadata")  # Title for meta data

    # Dict of dynamically called filters following type of field to be fault tolerent

    def identity(self, field_label, field_input):
        return field_input

    def integer(self, field_label, field_input):
        return int(field_input)

    def floating(self, field_label, field_input):
        # Handle the case for Indonesian number format
        print("here4")
        if isinstance(field_input, str):
            print("here5")
            field_input = field_input.replace('.', '')
            print("here6", field_input)
            print("here7", float(field_input))
        return float(field_input)

    def html(self, field_label, field_input):
        return plaintext2html(field_input)

    def boolean(self, field_label, field_input):
        return bool(field_input)

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

    
    def extract_data(self, model, values):
        dest_model = request.env[model.sudo().model]

        data = {
            'record': {},        # Values to create record
            'attachments': [],  # Attached files
            'custom': '',        # Custom fields values
            'meta': '',         # Add metadata if enabled
        }

        authorized_fields = model.with_user(SUPERUSER_ID)._get_form_writable_fields()

        # Add your custom field to authorized_fields if it doesn't already exist
        if 'salary_expected' not in authorized_fields:
            authorized_fields['salary_expected'] = {'type': 'float', 'required': False}
        print("authorized fields:", authorized_fields)
        error_fields = []
        custom_fields = []

        for field_name, field_value in values.items():
            # If the value of the field if a file
            if hasattr(field_value, 'filename'):
                # Undo file upload field name indexing
                field_name = field_name.split('[', 1)[0]

                # If it's an actual binary field, convert the input file
                # If it's not, we'll use attachments instead
                if field_name in authorized_fields and authorized_fields[field_name]['type'] == 'binary':
                    data['record'][field_name] = base64.b64encode(field_value.read())
                    field_value.stream.seek(0)  # do not consume value forever
                    if authorized_fields[field_name]['manual'] and field_name + "_filename" in dest_model:
                        data['record'][field_name + "_filename"] = field_value.filename
                else:
                    field_value.field_name = field_name
                    data['attachments'].append(field_value)

            # If it's a known field
            elif field_name in authorized_fields:
                try:
                    print("here1", field_name)
                    input_filter = self._input_filters[authorized_fields[field_name]['type']]
                    print("here2", input_filter, field_value)
                    data['record'][field_name] = input_filter(self, field_name, field_value)
                    print("here3")
                except ValueError:
                    error_fields.append(field_name)

                if dest_model._name == 'mail.mail' and field_name == 'email_from':
                    # As the "email_from" is used to populate the email_from of the
                    # sent mail.mail, it could be filtered out at sending time if no
                    # outgoing mail server "from_filter" match the sender email.
                    # To make sure the email contains that (important) information
                    # we also add it to the "custom message" that will be included
                    # in the body of the email sent.
                    custom_fields.append((_('email'), field_value))

            # If it's a custom field
            elif field_name != 'context':
                custom_fields.append((field_name, field_value))

        data['custom'] = "\n".join([u"%s : %s" % v for v in custom_fields])

        # Add metadata if enabled  # ICP for retrocompatibility
        if request.env['ir.config_parameter'].sudo().get_param('website_form_enable_metadata'):
            environ = request.httprequest.headers.environ
            data['meta'] += "%s : %s\n%s : %s\n%s : %s\n%s : %s\n" % (
                "IP", environ.get("REMOTE_ADDR"),
                "USER_AGENT", environ.get("HTTP_USER_AGENT"),
                "ACCEPT_LANGUAGE", environ.get("HTTP_ACCEPT_LANGUAGE"),
                "REFERER", environ.get("HTTP_REFERER")
            )

        # This function can be defined on any model to provide
        # a model-specific filtering of the record values
        # Example:
        # def website_form_input_filter(self, values):
        #     values['name'] = '%s\'s Application' % values['partner_name']
        #     return values
        if hasattr(dest_model, "website_form_input_filter"):
            data['record'] = dest_model.website_form_input_filter(request, data['record'])

        missing_required_fields = [label for label, field in authorized_fields.items() if field['required'] and label not in data['record']]
        if any(error_fields):
            raise ValidationError(error_fields + missing_required_fields)

        return data

