from odoo import models, fields
from odoo.http import request


class HrSkill(models.Model):
    _inherit = 'hr.skill'

    mandatory = fields.Boolean(string='Mandatory', default=True)


