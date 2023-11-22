from odoo import fields, models, api

class PDSData(models.Model):

    _name = "pds.data"

    nama = fields.Char(string="Nama")
    nik = fields.Char(string="Nomor Induk Kependudukan")
    alamat = fields.Char(string="Alamat Rumah")

    applicant_id = fields.Many2one('hr.applicant', string="Applicant FK")