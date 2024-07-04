from odoo import models, fields, api

class HrExperience(models.Model):
    _name = "hr.experience"
    
    applicant_id = fields.Many2one('hr.applicant', string="Experience")
    emp_id_ = fields.Integer(related='applicant_id.emp_id.id')
    employee_id = fields.Many2one('hr.employee', string="Experience", store=True, compute='_compute_employee_id')
    
    start_date  = fields.Date(string="Start Date")
    end_date    = fields.Date(string="End Date")
    company_name = fields.Char(string="Company Name")
    position = fields.Char(string="Position")
    description = fields.Char(string="Job Description")
    reason_for_leaving = fields.Char(string="Reason For Leaving")
    salary = fields.Integer(string="Salary")
    comp_telp = fields.Char(string="Company Telp Number")
    
    @api.depends('applicant_id', 'emp_id_')
    def _compute_employee_id(self):
        for experience in self:
            if experience.appicant_id.emp_id:
                experience.employee_id = experience.applicant_id.emp_id
    
    