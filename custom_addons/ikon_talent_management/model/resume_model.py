import base64

from odoo import fields, models, api
from odoo.http import request
from odoo import models, api
from datetime import datetime


class ResumeModel(models.Model):

    _name = "custom.resume.experience"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    resume_dateStart = fields.Date(string="Resume Start")
    resume_dateEnd = fields.Date(string="Resume End")
    rsm_com_name = fields.Char(string="Project Title",)
    rsm_com_job_title = fields.Char(string="Job Title in Company")
    rsm_com_projectDes = fields.Char(string="Project Description")
    resume_tech_used = fields.Html(string="Frontend Technology Used")
    resume_sys_used = fields.Html(string="System Technology Used")
    resume_tech_used_certificate = fields.Many2many('custom.resume.certif.tag', "resume_certif_tag_rel", string='Resume Certificate')
    resume_key_responsible = fields.Html(string="Key responsibility")
    company_image = fields.Image(string="Company Image")



    # resume_tech_used_frontend = fields.Many2many('custom.frontend.tag', "resume_frontend_tag_rel", string='Frontend Technology Used')
    # resume_tech_used_backend = fields.Many2many('custom.backend.tag', "resume_backend_tag_rel", string='Backend Technology Used')
    # resume_tech_used_database = fields.Many2many('custom.database.tag', "resume_database_tag_rel", string='Database Technology Used')
    # resume_sys_int_appl = fields.Many2many('custom.resume.sysint.apl', "resume_sys_apl_tag_rel", string='Sys Int Application')
    # resume_sys_int_middleware = fields.Many2many('custom.resume.sysint.middleware', "resume_sys_middleware_tag_rel", string='Sys Int middleware')
    # resume_sys_int_email_notif = fields.Many2many('custom.resume.sysint.email.notif', "resume_sys_email_notif_tag_rel", string='Sys Int Email Notif')

    fr_test = fields.Char(string="Frontend Used", compute="_compute_frontend_tech")

    @staticmethod
    def format_date(date):
        # Implementasi untuk mengembalikan format bulan tahun (misal: "Januari 2023")
        if date:
            return date.strftime('%B %Y')  # %B untuk nama bulan penuh, %Y untuk tahun empat digit
        return ''

    @api.depends("resume_tech_used")
    def _compute_frontend_tech(self):
        for resume in self:
            tech_used_frontend_names = [tag.name for tag in resume.resume_tech_used]
            resume.fr_test = ', '.join(tech_used_frontend_names)


    def compute_default_image_binary(self):
        return self.def_image_bin_ikon


class ResumeSysIntEmailNotif(models.Model):
    _name = 'custom.resume.sysint.email.notif'
    _description = 'System Int email notif Tags'

    name = fields.Char(string='Tag Name',)

class ResumeSysIntMiddleware(models.Model):
    _name = 'custom.resume.sysint.middleware'
    _description = 'System Int middleware Tags'

    name = fields.Char(string='Tag Name',)

class ResumeSysIntAppl(models.Model):
    _name = 'custom.resume.sysint.apl'
    _description = 'System Int Apl Tags'

    name = fields.Char(string='Tag Name',)

class ResumeCertificate(models.Model):
    _name = 'custom.resume.certif.tag'
    _description = 'Certif Tags'

    name = fields.Char(string='Tag Name',)

class BackendTag(models.Model):
    _name = 'custom.backend.tag'
    _description = 'Backend Tags'

    name = fields.Char(string='Tag Name',)

class FrontendTag(models.Model):
    _name = 'custom.frontend.tag'
    _description = 'Frontend Tags'

    name = fields.Char(string='Tag Name',)

class DatabaseTag(models.Model):
    _name = 'custom.database.tag'
    _description = 'Database Tags'

    name = fields.Char(string='Tag Name',)



class ResumeCompanyModel(models.Model):

    _name = "custom.resume.experience.company"

    # resume_experience_id = fields.Many2one("custom.resume.experience", string="Experience")
    resume_experience_id = fields.Many2one("hr.applicant", string="Experience")
    rsm_com_name = fields.Char(string="Company Name")
    rsm_com_job_title = fields.Char(string="Job Title in Company")
    rsm_com_projectDes = fields.Char(string="Project Description")
    # summary_id = fields.One2many("custom.resume.summary", "resume_id", string="Summary ID")

class SummaryResume(models.Model):

    _name = "custom.resume.summary"

    resume_id = fields.Many2one(string="Resume Id")
    rsm_sum_name = fields.Char("Summary Field")



