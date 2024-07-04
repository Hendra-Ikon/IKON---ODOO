from odoo import api, fields, models

class ModelPeriod(models.Model):
    _name = "model.period"
    _description = "Periods Model"

    account_move_id = fields.Many2one("account.move", string="Account Move", readonly=True)
    sale_order_id = fields.Many2one("sale.order", string="Sale order", readonly=True)
    name = fields.Char(string="nama")
    period_start = fields.Date(string="Period Start")
    period_end = fields.Date(string="Period End")


