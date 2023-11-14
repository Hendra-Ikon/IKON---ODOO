from odoo import models, fields

class HrSkill(models.Model):
    _inherit = 'hr.skill'

    mandatory = fields.Boolean(string='Mandatory', default=True)
