from odoo import api, models, fields, exceptions
import logging

logger = logging.getLogger(__name__)

class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    indeed_profile = fields.Char(string="Indeed Profile")
    glints_profile = fields.Char(string="Glints Profile")
    nik = fields.Char(string="NIK")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender")
    dob = fields.Date(string="Date of Birth")
    address = fields.Char(string="Address")
    martial_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
    ], string="Martial Status")
    religion = fields.Selection([
        ('islamic', 'Islam'),
        ('christian', 'Christian'),
        ('hindu', 'Hindu'),
        ('buddha', 'Buddha'),
        ('catholic', 'Catholic'),
        ('khonghucu', 'Khonghucu'),
        ('not say', 'Rather Not Say')
    ], string="Religion")
    last_salary = fields.Integer(string='Last Salary')
    fresh_grad = fields.Boolean(string="Fresh Graduate")
    experience_ids = fields.One2many('hr.experience', 'applicant_id', string="Experience")
    result = fields.Char('Result')
    custom_skill = fields.Text(string="Custom skill")
    skill_ids = fields.Many2many('hr.skill', compute='_compute_skill_ids', store=True, string="SkillID")
    pds_fill = fields.Integer(string="PDS Fill")
    pds_percentage = fields.Integer(string="PDS Fill", compute='_compute_pds_percentage', store=False)
    pds_send = fields.Boolean(string="Pds Send")
    @api.depends('pds_fill')
    def _compute_pds_percentage(self):
        for record in self:
            total_value = 14
            if total_value != 0:
                percentage = (record.pds_fill / total_value) * 100
                record.pds_percentage = int(percentage)
            else:
                record.pds_percentage = 0

    def pds_fills(self):
        return {
        'warning': {'title': "PDS", 'message': "PDS FILL", 'type': 'notification'},
    }




    # def _compute_pds_percentage(self):
    #     for record in self:
    #         total_value = 8  # Angka yang Anda maksud
    #         if total_value != 0:
    #             record.pds_percentage = (record.pds_fill / total_value) * 100
    #         else:
    #             record.pds_percentage = 0.0

    # @api.constrains('email_from')
    # def _check_duplicate_email(self):
    #     for applicant in self:
    #         domain = [('id', '!=', applicant.id), ('email_from', '=', applicant.email_from)]
    #         if self.search_count(domain) > 0:
    #             raise exceptions.ValidationError("An applicant with this email already exists.")

    @api.constrains('email_from', 'job_id')
    def _check_duplicate_application(self):
        for applicant in self:
            domain = [
                ('id', '!=', applicant.id),
                ('email_from', '=', applicant.email_from),
                ('job_id', '=', applicant.job_id.id),
            ]
            if self.search_count(domain) > 0:
                raise exceptions.ValidationError("An applicant with the same email and job already exists.")

    # PDS MODEL


class JobsApplied(models.Model):
    _inherit = "hr.applicant"

    # _name = "test.print"

    @api.model
    def get_user_job_applications(self, user_id):
        """
        Fetch job applications for a specific user.

        :param user_id: ID of the user for whom to fetch job applications.
        :return: Recordset of job applications for the user.
        """
        current_user = self.env.user
        applications = self.search([('user_id', '=', current_user.id)])
        applied_jobs = applications.mapped('job_id')


        return applied_jobs

class StageSequenced(models.Model):

    _inherit = "hr.applicant"

    stage_id = fields.Many2one('hr.recruitment.stage', 'Stage', ondelete='restrict', tracking=True,
                               compute='_compute_stage', store=True, readonly=False,
                               domain="['|', ('job_ids', '=', False), ('job_ids', '=', job_id)]", track_visibility='onchange',
                               copy=False, index=True,
                               group_expand='_read_group_stage_ids')

    @api.constrains('stage_id')
    def _check_stage_sequence(self):
        for rec in self:
            stages = rec.stage_id.sorted(lambda r: r.sequence)
            for i in range(len(stages) - 1):
                if stages[i].sequence > stages[i + 1].sequence:
                    raise exceptions.ValidationError('Invalid stage sequence!')

    def _default_stage_ids(self):
        # Set the default stages based on your requirements
        stage_obj = self.env['hr.recruitment.stage']
        return [(6, 0, stage_obj.search([]).ids)]

