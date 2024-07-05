
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class InheritAccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
 
    date = fields.Date(
        'Date',
        required=True,
        index=True,
        default=fields.Date.context_today,
        readonly=True
    )
    name = fields.Text(
        'Description',
        required=True,
    )

    amount = fields.Monetary(
        'Hours',
        required=True,
        default=0.0,
    )

