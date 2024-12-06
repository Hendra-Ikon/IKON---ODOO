from odoo import models, fields, api

class Leave(models.Model):
    _inherit = 'hr.leave'

    approvers = fields.Many2many('res.users', string='Approvers')

    @api.model
    def create(self, vals):
        record = super(Leave, self).create(vals)
        if record.employee_id:
            record.approvers = record.employee_id.leave_approvers
        return record

    def write(self, vals):
        res = super(Leave, self).write(vals)
        for record in self:
            if 'employee_id' in vals:
                record.approvers = record.employee_id.leave_approvers
        return res
