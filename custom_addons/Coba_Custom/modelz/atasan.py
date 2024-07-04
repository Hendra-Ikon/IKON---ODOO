from odoo import api, fields, models

class KaryawannIkon(models.Model):
    _name = "karyawann.ikon"
    _inherit = ['mail.thread']
    _description = "Karyawann Records"

    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string="Age", required=True, tracking=True)
    married = fields.Boolean(string="Married?", tracking=True)
    noted = fields.Text(string="Notes")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")