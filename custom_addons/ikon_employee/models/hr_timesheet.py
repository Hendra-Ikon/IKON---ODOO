from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)

class Timesheet(models.Model):
    _inherit = 'account.analytic.line'

    approvers = fields.Many2many('res.users', string='Approvers')

    @api.model
    def create(self, vals):
        record = super(Timesheet, self).create(vals)
        if record.employee_id:
            record.approvers = record.employee_id.timesheet_approvers
        return record

    def write(self, vals):
        res = super(Timesheet, self).write(vals)
        for record in self:
            if 'employee_id' in vals:
                record.approvers = record.employee_id.timesheet_approvers
        return res
