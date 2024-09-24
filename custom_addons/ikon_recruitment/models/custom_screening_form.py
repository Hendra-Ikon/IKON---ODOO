import logging
from odoo import models, fields, api
from datetime import datetime, timedelta
import secrets

_logger = logging.getLogger(__name__)

class CustomScreeningForm(models.Model):
    _inherit = "hr.applicant"

    screening_token = fields.Char(string='Screening Token', readonly=True)
    screening_token_expiration = fields.Datetime(string='Screening Token Expiration')
    
    applicant_id = fields.Many2one(
        comodel_name='hr.applicant',
        string='Applicant')
    # Full name = hr.applicant.partner_name
    # Phone No = hr.applicant.partner_phone
    # Email = hr.applicant.email_from
    # Position that you applied = hr.applicant.name
    screening_availability_status = fields.Char(
        string="Availability Status",
        required=False,
        website_form_blacklisted=False,
    )
    screening_start_date = fields.Date(
        string="Start Date",
        website_form_blacklisted=False,
    )
    screening_current_emp_stats = fields.Char(
        string="Current Employment Status",
        required=False,
        website_form_blacklisted=False,
    )
    screening_laptop_ownership = fields.Selection(
        selection=[
            ('yes_yes', "Yes and OK to use it for project"),
            ('yes_no', "Yes but only for personal use"),
            ('no_no', "No")
        ],
        string="Laptop Ownership",
        website_form_blacklisted=False,
    )
    screening_wfo_availability = fields.Boolean(
        string="WFO Availability",
        website_form_blacklisted=False,
    )
    screening_bank_client_agreement = fields.Selection(
        selection=[
            ('yes_yes', "Yes, I am OK to work for banks"),
            ('yes_no', "Yes, but if there is non-bank client, I prefer non-bank clients"),
            ('no_no', "No. I do not want to work for banks / financing companies")
        ],
        string="Working with Banks",
        website_form_blacklisted=False,
    )
    screening_bank_client_exp = fields.Text(
        string="Bank Client Experience",
        website_form_blacklisted=False,
    )
    screening_past_proj_desc = fields.Text(
        string="Past Project(s)",
        website_form_blacklisted=False,
    )
    screening_in_five_years = fields.Text(
        string="Expectation in 5 Years",
        website_form_blacklisted=False,
    )
    # What is your current monthly salary? (Float.2) = hr.applicant.current_salary
    screening_current_benefits = fields.Text(
        string="Current Benefits",
        website_form_blacklisted=False,
    )
    screening_net_or_gross = fields.Selection(
        selection=[
            ('net', "Net"),
            ('gross', "Gross")
        ],
        string="Net or Gross",
        website_form_blacklisted=False,
    )
    # What is your expected montly salary? (Float.2) = hr.applicant.expected_salary
    screening_other_expectation = fields.Text(
        string="Other Expectations",
        website_form_blacklisted=False,
    )
    screening_negotiability = fields.Selection(
        selection=[
            ('yes', "Yes"),
            ('no', "No"),
            ('maybe', "Maybe")
        ],
        string="Negotiability",
        website_form_blacklisted=False,
    )
    
    @api.model
    def clean_expired_tokens(self):
        # This method will be called periodically to clean expired tokens
        expired_tokens = self.search([('screening_token_expiration', '<', fields.Datetime.now())])
        expired_tokens.write({'screening_token': False, 'screening_token_expiration': False})
        
    def generate_screening_url(self):
        # Check if a token exists and if it's expired
        if self.screening_token and self.screening_token_expiration > datetime.now():
            # Return existing token if it's not expired
            base_url = 'http://recruitment.ikonsultan.co.id/'
            return f"{base_url}web/screening-form/{self.screening_token}?email={self.email_from}"
        
        # Generate a unique token
        token = secrets.token_urlsafe(16)
        # Set token expiration (e.g., 1 hour from now)
        token_expiration = fields.Datetime.now() + timedelta(hours=24)
        self.write({
            'screening_token': token,
            'screening_token_expiration': token_expiration
        })
        # Return the full URL
        base_url = 'http://recruitment.ikonsultan.co.id/'
        return f"\'{base_url}web/screening-form/{self.screening_token}?email={self.email_from}\'"
        # return self.screening_token

    def action_send_screening_form(self):
        name = self.partner_name
        email = self.email_from
        
        context = self._context
        current_uid = context.get('uid')
        current_user = self.env['res.users'].browse(current_uid)

        subject = f"{current_user.name} from {current_user.company_id.name} invites you to fill Screening Form for the position you applied"
        user = self.env['res.users'].search([
            ('login', '=', email),
            ('name', '=', name)
            ], limit=1)

        template = self.env.ref('ikon_recruitment.custom_screening_email')
        
        template.write({
            'subject': subject,
            'email_to': self.email_from,
            'body_html': template.body_html.replace(
                '{screening_url}', self.generate_screening_url()).replace(
                '{applicant_name}', name).replace(
                '{creator}', current_user.name)
        })
        
        template.send_mail(user.id, force_send=True, raise_exception=True)
        _logger.info("Screening email sent for user <%s> to <%s>", user.login, user.email)

        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Successfully sent screening email',
                # 'sticky': True,
            }
        }

        return notification