from odoo import fields, models, api


class ResumeModel(models.Model):

    _name = "custom.resume.experience"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    resume_dateStart = fields.Date(string="Resume Start")
    resume_dateEnd = fields.Date(string="Resume End")
    rsm_com_name = fields.Char(string="Company Name")
    rsm_com_job_title = fields.Char(string="Job Title in Company")
    rsm_com_projectDes = fields.Char(string="Project Description")
    resume_tech_used_backend = fields.Many2many('custom.technology.tag', "co_resume_tech_tag_rel", string='Backend Technology Used')
    resume_tech_used_frontend = fields.Many2many('custom.technology.tag', "co_resume_tech_tag_rel", string='Frontend Technology Used')
    resume_tech_used_database = fields.Many2many('custom.technology.tag', "co_resume_tech_tag_rel", string='Database Technology Used')


class TechnologyTag(models.Model):
    _name = 'custom.technology.tag'
    _description = 'Technology Tags'

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

# class ResumeTechUse(models.Model):
#
#     _name = "custom.resume.techUsed"
#
#     resume_id = fields.Many2one(string="Resume Id")
#     resume_tech_use_backend = fields.One2many(string="Backend Technology Used")
#     resume_tech_use_frontend = fields.One2many(string="Frontend Technology Used")
#     resume_tech_use_database = fields.Char(string="Database Technology Used")
#     skill_id = fields.One2many("custom.resume.skill", "resume_techUse_id", string="Skill ID")
#
# class ResumeSkill(models.Model):
#
#     _name = "custom.resume.skill"
#
#     resume_techUse_id = fields.Many2one(string="Techuse ID")
#     skill_name = fields.Char(string="Skill Name")