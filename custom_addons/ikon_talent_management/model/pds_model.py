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

    _inherit = "hr.applicant"

    _description = "Personal Data Sheet"


    pds_fullname = fields.Char(string="Nama", default="Fullname Test")
    pds_nik = fields.Char(string="Nomor Induk Kependudukan")
    pds_addressNIK = fields.Char(string="Alamat Seuai NIK")
    pds_currentAddress = fields.Char(string="Alamat sesuai domisili sekarang")
    pds_phoneNumber = fields.Char(string="No Hp")
    pds_email = fields.Char(string="Personal Email")
    pds_placeOfBirth = fields.Char(string="Place of birth")
    pds_nationality = fields.Char(string="Nationality")
    pds_religion = fields.Selection(NATIONALITY, default=NATIONALITY[0][0])



    # applicant_id = fields.Many2one('hr.applicant', string="Applicant FK")

