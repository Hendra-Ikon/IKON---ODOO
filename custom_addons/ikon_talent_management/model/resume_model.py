from odoo import fields, models, api


class ResumeModel(models.Model):

    _name = "cuatom.resume.experience"


    resume_dateStart = fields.Date(string="Resume Start")
    resume_dateEnd = fields.Date(string="Resume End")


class ResumeCompanyModel(models.Model):

    _name = "custom.resume.experience.company"

    resume_company_name = fields.Char(string="Company Name")
    resume_company_job_title = fields.Char(string="Job Title in Company")
    resume_company_projectDes = fields.Char(string="Project Description")
