from odoo import fields, models, api

NATIONALITY = [
    ("select", "PLEASE SELECT"),
    ("islam", "ISLAM"),
    ("kristen", "KRISTEN"),
    ("hindu", "HINDU"),
    ("budha", "BUDHA"),
    ("konghuchu", "KONGHUCHU"),

]
class PDSData(models.Model):

    _name = "pds.data"
    _description = "Personal Data Sheet"


    fullname = fields.Char(string="Nama")
    nik = fields.Char(string="Nomor Induk Kependudukan")
    addressNIK = fields.Char(string="Alamat Seuai NIK")
    currentAddress = fields.Char(string="Alamat sesuai domisili sekarang")
    phoneNumber = fields.Char(string="No Hp")
    email = fields.Char(string="Personal Email")
    placeOfBirth = fields.Char(string="Place of birth")
    nationality = fields.Char(string="Nationality")
    religion = fields.Selection(NATIONALITY, default=NATIONALITY[0][0])



    applicant_id = fields.Many2one('hr.applicant', string="Applicant FK")