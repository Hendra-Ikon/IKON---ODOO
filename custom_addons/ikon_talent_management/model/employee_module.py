from odoo import fields, models, api


class InheritEmployee(models.Model):

    _inherit = "hr.employee"

    # employee_resume = fields.One2many('custom.resume.experience', 'employee_id', string='Resume')
    employee_resumes = fields.One2many('custom.resume.experience', 'employee_id', string='Resume')
    custom_skill = fields.Text(string="Custom skill")
    # pds_education = fields.One2many('custom.edu', 'employee_id', string='Education')
    empl_pds_education = fields.One2many('custom.edu', 'employee_id', string='Education')
    summary_experience = fields.Text(string="Summary of Experience")

    # def action_create_user(self):
    #     return






class ResumeModel(models.Model):

    _inherit = "custom.resume.experience"

    employee_id = fields.Many2one('hr.employee', string='Employee ID')



    # resume_tech_used_frontend = fields.Many2many('custom.frontend.tag', "resume_frontend_tag_rel", string='Frontend Technology Used')
    # resume_tech_used_backend = fields.Many2many('custom.backend.tag', "resume_backend_tag_rel", string='Backend Technology Used')
    # resume_tech_used_database = fields.Many2many('custom.database.tag', "resume_database_tag_rel", string='Database Technology Used')
    # resume_sys_int_appl = fields.Many2many('custom.resume.sysint.apl', "resume_sys_apl_tag_rel", string='Sys Int Application')
    # resume_sys_int_middleware = fields.Many2many('custom.resume.sysint.middleware', "resume_sys_middleware_tag_rel", string='Sys Int middleware')
    # resume_sys_int_email_notif = fields.Many2many('custom.resume.sysint.email.notif', "resume_sys_email_notif_tag_rel", string='Sys Int Email Notif')

    fr_test = fields.Char(string="Frontend Used", compute="_compute_frontend_tech")


    @api.depends("resume_tech_used")
    def _compute_frontend_tech(self):
        for resume in self:
            tech_used_frontend_names = [tag.name for tag in resume.resume_tech_used]
            resume.fr_test = ', '.join(tech_used_frontend_names)







