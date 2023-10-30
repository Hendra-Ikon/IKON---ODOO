import xlrd
from odoo import models, fields
from base64 import b64decode



class TalentPoolImportWizard(models.TransientModel):
    _name = 'talent.pool.import.wizard'
    _description = 'Talent Pool Import Wizard'

    data_file = fields.Binary('Excel File', required=True)

    def import_data(self):
        file_data = self.data_file
        workbook = xlrd.open_workbook(file_contents=b64decode(file_data))
        sheet = workbook.sheet_by_index(0)

        talent_pool_model = self.env['talent.pool.data']

        for row in range(1, sheet.nrows):  # Start from the second row (skip header)
            data = {
                # 'no': int(sheet.cell_value(row, 0)),
                'sumber': sheet.cell_value(row, 1),
                'posisi': sheet.cell_value(row, 2),
                'nama': sheet.cell_value(row, 3),
                'email': sheet.cell_value(row, 4)
            }
            talent_pool_model.create(data)




class TalentData(models.Model):
    _name = "talent.pool.data"

    no = fields.Integer(string="No")
    sumber = fields.Char(string="Sumber")
    posisi = fields.Char(string="Posisi")
    nama = fields.Char(string="Nama")
    email = fields.Char(string="Email")





