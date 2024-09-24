from odoo import models, fields, api
from datetime import datetime

class CustomInterviewOne(models.Model):
    _inherit = "hr.applicant"

    applicant_id = fields.Many2one(
        comodel_name='hr.applicant', 
        string='Applicant')
    interviewer_one_ids = fields.Many2many('res.users', 'hr_applicant_res_users_interviewers_one_rel',
        string='Interviewers', index=True, tracking=True,
        domain="[('share', '=', False), ('company_ids', 'in', company_id)]")
    interview_one_date = fields.Date(
        string="Interview Date")
    interview_one_link = fields.Char(
        string="Interview Link")
    interview_one_decision = fields.Selection(
        string="Interview Decision", 
        selection=[
            ('hire', 'Hire'), 
            ('do_not_hire', 'Do Not Hire'), 
            ('second_interview', 'Refer for 2nd Interview')])
    interview_one_summary = fields.Html(string="Summary")

class CustomInterviewTwo(models.Model):
    _inherit = "hr.applicant"

    applicant_id = fields.Many2one(
        comodel_name='hr.applicant', 
        string='Applicant')
    interviewer_two_ids = fields.Many2many('res.users', 'hr_applicant_res_users_interviewers_two_rel',
        string='Interviewers', index=True, tracking=True,
        domain="[('share', '=', False), ('company_ids', 'in', company_id)]")
    interview_two_date = fields.Date(
        string="Interview Date")
    interview_two_link = fields.Char(
        string="Interview Link")
    interview_two_decision = fields.Selection(
        string="Interview Decision", 
        selection=[
            ('hire', 'Hire'), 
            ('do_not_hire', 'Do Not Hire'), 
            ('second_interview', 'Refer for 2nd Interview')])
    interview_two_decision = fields.Selection(
        string="Interview Decision", 
        selection=[
            ('hire', 'Hire'), 
            ('do_not_hire', 'Do Not Hire')])
    interview_two_summary = fields.Html(string="Summary")
    