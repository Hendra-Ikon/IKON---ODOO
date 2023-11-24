from odoo import api, models, fields, exceptions


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
