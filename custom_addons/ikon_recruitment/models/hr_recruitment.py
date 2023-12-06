from odoo import models, fields, api
from odoo.http import request


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

    stage_name = fields.Char(related='stage_id.name', string='Stage Name', readonly=True)

    def action_create_user_and_send_email(self):
        name = self.partner_name  # Replace with the actual field you want to use for the user's name
        email = self.email_from  # Replace with the actual field you want to use for the user's email

        # Create a new user
        user = self.env['res.users'].create({
            'name': name,
            'login': email,
            'email': email,
        })

        portal_group_id = self.env.ref('base.group_portal').id
        if portal_group_id:
            # Remove the user from existing groups
            user.write({'groups_id': [(3, group_id) for group_id in user.groups_id.ids]})

            # Add the user to the portal group
            user.write({'groups_id': [(4, portal_group_id)]})

            template_id = self.env.ref('ikon_recruitment.set_password_email')
            if template_id:
                template_id.send_mail(user.id, force_send=True)

                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Success',
                        'message': 'Successfully sent login invitation',
                        # 'sticky': True,
                    }
                }

                return notification

        # template_id = self.env.ref('ikon_recruitment.set_password_email')
        # if template_id:
        #     template_id.send_mail(user.id, force_send=True)
        #
        # notification = {
        #     'type': 'ir.actions.client',
        #     'tag': 'display_notification',
        #     'params': {
        #         'title': 'Success',
        #         'message': 'Successfully send login invitation',
        #         # 'sticky': True,
        #     }
        # }
        #
        #
        # return notification
