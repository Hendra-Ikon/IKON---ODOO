from odoo import models, fields, api
from datetime import datetime

class CustomScreeningForm(models.Model):
    _inherit = "hr.applicant"
    _description = "Screening Form"

    applicant_id = fields.Many2one(
        comodel_name='hr.applicant', 
        string='Applicant')
    # Full name = hr.applicant.partner_name
    # Phone No = hr.applicant.partner_phone
    # Email = hr.applicant.email_from
    # Position that you applied = hr.applicant.name
    availability_status = fields.Selection(
        selection=[
            (0, 'I am currently available'),
            (1, 'Next month'),
            (2, 'In 2 months'),
            (3, 'In 3 months')
            (4, 'Other')
        ],
        string="Availability Status"
    ) 
    start_date = fields.Date(
        string="Start Date"
    )
    current_emp_stats = fields.Selection(
        selection=[
            (0, "Permanent Employee"),
            (1, "Contract Employee - 6 months"),
            (2, "Contract Employee - 12 months"),
            (3, "Other")
        ],
        string="Current Employment Status"
    )
    laptop_ownership = fields.Selection(
        selection=[
            (0, "Yes and OK to use it for project"),
            (1, "Yes but only for personal use"),
            (2, "No")
        ]
    )
    wfo_availability = fields.Boolean(
        string="WFO Availability"
    )
    bank_client_agreement = fields.Selection(
        selection=[
            (0, "Yes, I am OK to work for banks"),
            (1, "Yes, but if there is non-bank client, I prefer non-bank clients"),
            (2, "No. I do not want to work for banks / financing companies")
        ],
        string="Working with Banks"
    )
    bank_client_exp = fields.Html(
        string="Bank Client Experience"
    )
    past_proj_desc = fields.Html(
        string="Past Project(s)"
    )
    in_five_years = fields.Html(
        string="Expectation in 5 Years"
    )
    # What is your current monthly salary? (Float.2) = hr.applicant.current_salary
    current_benefits = fields.Html(
        string="Current Benefits"
    )
    net_or_gross = fields.Selection(
        selection=[
            (0, "Net"),
            (1, "Gross")
        ],
        string="Net or Gross"
    )
    # What is your expected montly salary? (Float.2) = hr.applicant.expected_salary
    other_expectation = fields.Html(
        string="Other Expectations"
    )
    negotiability = fields.Boolean(
        string="Negotiability"
    )