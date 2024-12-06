from odoo import models, fields, api

class Expense(models.Model):
    _inherit = 'hr.expense'

    approvers = fields.Many2many('res.users', string='Approvers')

    @api.model
    def create(self, vals):
        record = super(Expense, self).create(vals)
        if record.employee_id:
            record.approvers = record.employee_id.expense_approvers
        return record

    def write(self, vals):
        res = super(Expense, self).write(vals)
        for record in self:
            if 'employee_id' in vals:
                record.approvers = record.employee_id.expense_approvers
        return res
