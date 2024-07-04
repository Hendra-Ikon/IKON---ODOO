from odoo import api, fields, models


class Skill(models.Model):
    _name = 'custom.skill'
    _description = 'Skill'

    name = fields.Char(string='Skill Name', required=True)

class CustomSkillRequirement(models.Model):
    _inherit = "hr.job"

    skill_ids = fields.Many2many('custom.skill', string='Skills')




