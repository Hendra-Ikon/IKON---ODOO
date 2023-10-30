from odoo import models, fields

class CustomJobDescription(models.Model):
    _inherit = "hr.job"


    lead_data = fields.Char(String="Lead Article", required=True)
    must_have = fields.One2many('custom.musthave', 'job_id', string='Must Have Items')
    req_skill = fields.One2many('custom.reqskill', 'job_id', string='Req Skill Items')
    min_req = fields.One2many('custom.minreq', 'job_id', string='Minimum Req Items')
    whats_great = fields.One2many('custom.great', 'job_id', string='Whats Great')

class MustHave(models.Model):
    _name = 'custom.musthave'
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

# class Perks(models.Model):
#     _name = 'custom.perks'
#     _description = 'Custom Perks'
#
#     name = fields.Char(string='Whats Great', required=True)
#     job_id = fields.Many2one('hr.job', string='Job')




