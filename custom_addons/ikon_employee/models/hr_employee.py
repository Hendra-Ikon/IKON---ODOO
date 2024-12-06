from odoo import models, fields

class Employee(models.Model):
    _inherit = 'hr.employee'

    timesheet_approvers = fields.Many2many(
        'res.users',
        'hr_employee_timesheet_approver_rel',
        'employee_id',
        'user_id',
        string='Timesheet Approvers',
        domain=lambda self: [('groups_id', 'in', self.env.ref('ikon_timesheet.timesheet_group').id)],
    )
    
    leave_approvers = fields.Many2many(
        'res.users',
        'hr_employee_leave_approver_rel',
        'employee_id',
        'user_id',
        string='Leave Approvers'
    )
    
    expense_approvers = fields.Many2many(
        'res.users',
        'hr_employee_expense_approver_rel',
        'employee_id',
        'user_id',
        string='Expense Approvers'
    )
