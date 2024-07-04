from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = "hr.employee"
    
    experience_ids = fields.One2many('hr.experience', 'employee_id' ,string="Experience")