from odoo import fields, models, api


class InheritEmployee(models.Model):

    _inherit = "hr.employee"

    employee_resumes = fields.One2many('custom.resume.experience', 'employee_id', string='resume')
    custom_skill = fields.Text(string="Custom skill")
    # pds_education = fields.One2many('custom.edu', 'employee_id', string='Education')
    empl_pds_education = fields.One2many('custom.edu', 'employee_id', string='Education')
    summary_experience = fields.Text(string="Summary of Experience")

class ResumeModel(models.Model):

    _inherit = "custom.resume.experience"

    employee_id = fields.Many2one('hr.employee', string='Employee ID')






