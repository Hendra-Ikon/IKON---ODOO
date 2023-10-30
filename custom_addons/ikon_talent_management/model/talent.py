from odoo import models, fields, api

class TalentManagementTalentInherit(models.Model):
    _name = 'talent.management.talent.inherit'
    _description = 'Inherited Talent Management'

    name = fields.Char(string='Name', required=True)
    no_tlp = fields.Char(string='Phone Number')
    skill = fields.Char(string='Headline', required=True)
    talent_id = fields.Many2one('talent.management.talent', string='Talent')
    url = fields.Char(string='URL Linkedin')
    experience = fields.Char(string='Experience')
