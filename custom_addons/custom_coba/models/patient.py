from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "patient record"

    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    is_child = fields.Boolean(string="is child?")
    noted = fields.Text(string="Noted")
    gender = fields.Selection([('male', "Male"), ('female', "Female"), ("others", "Others")], string="Gender")