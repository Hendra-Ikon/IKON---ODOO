from odoo import models, fields, api, _
import logging
logger = logging.getLogger(__name__)
class TimesheetValidation(models.Model):
	_inherit = 'account.analytic.line'

	state = fields.Selection([
		('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected')
		], default='draft', string="States")

	status = fields.Selection([('draft','Draft'),
		('reject', 'Reject'), ('approve', 'Approved')
		], string="Status", required=True, default='draft')

	employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
	approved_id = fields.Many2one('res.users', string='Approved By')
	rejected_id = fields.Many2one('res.users', string='Rejected By',default=fields.Date.today)
	approved_date = fields.Datetime('Approved Date')
	rejected_date = fields.Datetime('Rejected Date')
	rejected_reason = fields.Char('Rejected Reason')

	@api.model
	def create(self, vals):
		vals['state'] = 'submitted'
		return super(TimesheetValidation, self).create(vals)
	def Action_Approve(self):
		self.write({'state': 'approved', 'status': 'approve', 'approved_date': fields.Date.today()})

	def Action_Reject(self):
		self.write({'state': 'rejected', 'status': 'reject'})


		
class TimeSheetValidationWizard(models.TransientModel):
	_name = 'timesheet.validation.wizard'

	reason = fields.Text('Rejected Reason')
	approved_id = fields.Many2one('res.users', string='Approved By')
	rejected_id = fields.Many2one('res.users', string='Rejected By')
	approved_date = fields.Datetime('Approved Date')
	rejected_date = fields.Datetime('Rejected Date')
	status = fields.Selection([('draft','Draft'),
		('reject', 'Reject'), ('approve', 'Approved')
		], string="Status", required=True, default='approve')


	def reject(self):
		active_id = self._context.get('active_id')
		current_record = self.env['account.analytic.line'].search([('id', '=', active_id)])
		
		current_record.status = 'reject'

		if current_record.status == 'reject':
			current_record.rejected_id = self.rejected_id
			current_record.rejected_reason = self.reason
			current_record.state = 'rejected'
			mail_template = self.env.ref('ak_timesheet_approval.timesheet_validation_email_template')
			mail_template.send_mail(current_record.id, force_send=True)

	def approve(self):
		active_id = self._context.get('active_id')
		current_record = self.env['account.analytic.line'].search([('id', '=', active_id)])

		current_record.status = 'approve'

		if current_record.status == 'approve':
			current_record.approved_id = self.approved_id
			current_record.state = 'approved'
			mail_template = self.env.ref('ak_timesheet_approval.timesheet_validation_email_template')
			mail_template.send_mail(current_record.id, force_send=True)

