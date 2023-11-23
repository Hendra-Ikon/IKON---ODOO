from odoo import models, fields, api


class AppliedJob(models.Model):

    _inherit = "hr.applicant"


    applied_jobs = fields.Many2many('hr.job', string='Applied Jobs', compute='_compute_applied_jobs', store=True)

    @api.depends('job_id')
    def _compute_applied_jobs(self):
        for applicant in self:
            if applicant.job_id:
                applicant.applied_jobs = [(6, 0, [applicant.job_id.id])]
            else:
                applicant.applied_jobs = [(5, 0, 0)]  # Clear the Many2many field if no job is selected


class CustomJobDescription(models.Model):
    _inherit = "hr.job"


    lead_data = fields.Char(String="Lead Article")

    nice_to_have = fields.One2many('custom.nice_to_have', 'job_id', string='Nice to Have Items')
    req_skill = fields.One2many('custom.reqskill', 'job_id', string='Req Skill Items')
    min_req = fields.One2many('custom.minreq', 'job_id', string='Minimum Req Items')
    whats_great = fields.One2many('custom.great', 'job_id', string='Whats Great')

class MustHave(models.Model):
    _name = 'custom.nice_to_have'
    _description = 'Custom Must Have'

    name = fields.Char(string='Nice to Have', required=True)
    job_id = fields.Many2one('hr.job', string='Job')
class RequiredSkill(models.Model):
    _name = 'custom.reqskill'
    _description = 'Custom Required Skill'

    name = fields.Char(string='Required Skills', required=True)
    job_id = fields.Many2one('hr.job', string='Job')

class MinReq(models.Model):
    _name = 'custom.minreq'
    _description = 'Custom Required Skill'

    name = fields.Char(string='Minimum Requirement', required=True)
    job_id = fields.Many2one('hr.job', string='Job')
class WhatsGreat(models.Model):
    _name = 'custom.great'
    _description = 'Custom Whats Great'

    name = fields.Char(string='Whats Great', required=True)
    job_id = fields.Many2one('hr.job', string='Job')

class HrApplCrUsrSnEmail(models.Model):
    _inherit = 'hr.applicant'


    # toggle_send_email = fields.Boolean(string="Send Email", default=False)
    #
    # @api.depends("stage_id")
    # def toogle_email(self):
    #     if(self.stage_id == "PDS Submission"):
    #         self.toggle_send_email = True


    def action_create_user_and_send_email(self):
        # Get the applicant's email
        applicant_email = self.user_email

        # Create a user based on the email
        user_vals = {
            'name': self.partner_name,
            'email': applicant_email,
            # Add other user fields as needed
        }
        new_user = self.env['res.users'].create(user_vals)

        # Send an email to the newly created user
        # template_id = self.env.ref('ikon_recruitment.email_template_applicant')
        # if template_id:
        #     template_id.send_mail(new_user.id, force_send=True)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }





