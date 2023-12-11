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
    summary_id = fields.One2many("custom.resume.summary", "resume_id", string="Summary Experience")

class SummaryResume(models.Model):

    _name = "custom.resume.summary"

    resume_id = fields.Many2one(string="Resume Id")
    resume_summary_name = fields.Char("Summary Field")

class ResumeTechUse(models.Model):

    _name = "custom.resume.techUsed"

    resume_id = fields.Many2one(string="Resume Id")
    resume_tech_use_backend = fields.One2many(string="Backend Technology Used")
    resume_tech_use_frontend = fields.One2many(string="Frontend Technology Used")
    resume_tech_use_database = fields.Char(string="Database Technology Used")
    skill_id = fields.One2many("custom.resume.skill", "resume_techUse_id", string="Skill ID")

class ResumeSkill(models.Model):

    _name = "custom.resume.skill"

    resume_techUse_id = fields.Many2one(string="Techuse ID")
    skill_name = fields.Char(string="Skill Name")