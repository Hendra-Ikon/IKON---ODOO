from odoo import api, fields, models

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "doctor record"

    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    speciality = fields.Char(string="Speciality", required=True)
    customer = fields.Many2one('res.partner', string="Customer")