from odoo import models, fields, api
from odoo.http import request
import logging

logger = logging.getLogger(__name__)
from odoo.addons.base.models.ir_mail_server import MailDeliveryException
from odoo.addons.auth_signup.models.res_partner import SignupError, now
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class AppliedJob(models.Model):
    _inherit = "hr.applicant"

    # is_interviewer = fields.Boolean(compute='_compute_is_interviewer')
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

    nice_to_have = fields.Html(string='Nice to Have')
    req_skill = fields.Html(string='Required Skills')
    min_req = fields.Html(string='Minimum Requirements')
    # nice_to_have = fields.One2many('custom.nice_to_have', 'job_id', string='Nice to Have Items')
    # req_skill = fields.One2many('custom.reqskill', 'job_id', string='Req Skill Items')
    # min_req = fields.One2many('custom.minreq', 'job_id', string='Minimum Req Items')
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
        user = self.env['res.users'].with_context(applicant=True).create({
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

            # template_id = self.env.ref('ikon_recruitment.custom_set_password_email')
            # if template_id:
            #     template_id.send_mail(user.id, force_send=True)

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
            
    def pds_send_mail(self):
        name = self.partner_name  # Replace with the actual field you want to use for the user's name
        email = self.email_from  # Replace with the actual field you want to use for the user's email
        
        logger.info('name', name)
        logger.info('eamil', email)
        # Create a new user
        # user = self.env['res.users'].create({
        #     'name': name,
        #     'login': email,
        #     'email': email,
        # })

        # portal_group_id = self.env.ref('base.group_portal').id
        # if portal_group_id:
        #     # Remove the user from existing groups
        #     user.write({'groups_id': [(3, group_id) for group_id in user.groups_id.ids]})

        #     # Add the user to the portal group
        #     user.write({'groups_id': [(4, portal_group_id)]})

        #     template_id = self.env.ref('ikon_recruitment.set_password_email')
        #     if template_id:
        #         template_id.send_mail(user.id, force_send=True)

        #         notification = {
        #             'type': 'ir.actions.client',
        #             'tag': 'display_notification',
        #             'params': {
        #                 'title': 'Success',
        #                 'message': 'Successfully sent login invitation',
        #                 # 'sticky': True,
        #             }
        #         }

        #         return notification

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

class CustomResUsers(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals_list):
        # overridden to automatically invite user to sign up
        users = super(CustomResUsers, self).create(vals_list)
        applicant = self.env.context.get('applicant', False)
        
        # if not self.env.context.get('no_reset_password'):
        #     users_with_email = users.filtered('email')
        #     if users_with_email:
        #         try:
        #             users_with_email.with_context(create_user=True, applicant=applicant).action_reset_password()
        #         except MailDeliveryException:
        #             users_with_email.partner_id.with_context(create_user=True).signup_cancel()
        return users

    def action_reset_password(self):
        """ create signup token for each user, and send their signup url by email """
        if self.env.context.get('install_mode', False):
            return
        if self.filtered(lambda user: not user.active):
            raise UserError(_("You cannot perform this action on an archived user."))
        # prepare reset password signup
        create_mode = bool(self.env.context.get('create_user'))

        # no time limit for initial invitation, only for reset password
        expiration = False if create_mode else now(days=+1)

        self.mapped('partner_id').signup_prepare(signup_type="reset", expiration=expiration)

        # send email to users with their signup url
        template = False
        if create_mode:
            try:
                if self.env.context.get('applicant'):
                    template = self.env.ref('ikon_recruitment.custom_set_password_email', raise_if_not_found=False)
                else:
                    template = self.env.ref('auth_signup.set_password_email', raise_if_not_found=False)
            except ValueError:
                pass
        if not template:
            template = self.env.ref('auth_signup.reset_password_email')
        assert template._name == 'mail.template'

        email_values = {
            'email_cc': False,
            'auto_delete': True,
            'message_type': 'user_notification',
            'recipient_ids': [],
            'partner_ids': [],
            'scheduled_date': False,
        }

        for user in self:
            if not user.email:
                raise UserError(_("Cannot send email: user %s has no email address.", user.name))
            email_values['email_to'] = user.email
            # TDE FIXME: make this template technical (qweb)
            with self.env.cr.savepoint():
                force_send = not(self.env.context.get('import_file', False))
                template.send_mail(user.id, force_send=force_send, raise_exception=True, email_values=email_values)
            _logger.info("Password reset email sent for user <%s> to <%s>", user.login, user.email)
