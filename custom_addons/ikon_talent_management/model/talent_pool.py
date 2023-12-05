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

        # Get header row values
        header_row = sheet.row_values(0)

        for row in range(1, sheet.nrows):  # Start from the second row (skip header)
            data = {}
            for col_index, col_value in enumerate(sheet.row_values(row)):
                # Match column name dynamically to field name
                field_name = self.get_field_name(header_row[col_index])
                if field_name:
                    data[field_name] = col_value

            existing_record = talent_pool_model.search([('email', '=', data.get('email'))])
            if not existing_record:
                talent_pool_model.create(data)
            else:
                # Update only the specified fields, keep the existing values for others
                existing_record.write({key: value for key, value in data.items() if key in existing_record._fields})

    # def get_field_name(self, column_name):
    #     # Add your mapping logic here to map column names to field names
    #     # This can be a simple dictionary or a more complex logic based on your requirements
    #     # Example:
    #     field_mapping = {
    #         'Sumber': 'nama',
    #         'Posisi': 'email',
    #         'Nama': 'posisi',
    #         'Email': 'sumber',
    #         'Degree': 'degree',
    #         'Universitas': 'major',
    #         'Major': 'universitas',
    #         'Additional Notes': 'notes',
    #     }
    #     return field_mapping.get(column_name)


    def get_field_name(self, column_name):
        # Add your mapping logic here to map column names to field names
        # This can be a simple dictionary or a more complex logic based on your requirements
        # Example:
        field_mapping = {
            'Nama': 'nama',
            'Email': 'email',
            'Posisi': 'posisi',
            'Sumber': 'sumber',
            'Degree': 'degree',
            'Major': 'major',
            'Universitas': 'universitas',
            'Notes': 'notes',
        }
        return field_mapping.get(column_name)

    # def import_data(self):
    #     file_data = self.data_file
    #     workbook = xlrd.open_workbook(file_contents=b64decode(file_data))
    #     sheet = workbook.sheet_by_index(0)
    #
    #     talent_pool_model = self.env['talent.pool.data']
    #
    #     for row in range(1, sheet.nrows):  # Start from the second row (skip header)
    #         data = {
    #             'nama': sheet.cell_value(row, 1),
    #             'email': sheet.cell_value(row, 2),
    #             'posisi': sheet.cell_value(row, 3),
    #             'sumber': sheet.cell_value(row, 4),
    #             'degree': sheet.cell_value(row, 5),
    #             'major': sheet.cell_value(row, 6),
    #             'universitas': sheet.cell_value(row, 7),
    #             'notes': sheet.cell_value(row, 8)
    #         }
    #
    #         existing_record = talent_pool_model.search([('email', '=', data['email'])])
    #         if not existing_record:
    #             talent_pool_model.create(data)
    #         else:
    #             # Update only the specified fields, keep the existing values for others
    #             existing_record.write({key: value for key, value in data.items() if key in existing_record._fields})


class TalentData(models.Model):
    _name = "talent.pool.data"

    no = fields.Integer(string="No")
    nama = fields.Char(string="Sumber")
    email = fields.Char(string="Posisi")
    posisi = fields.Char(string="Nama")
    sumber = fields.Char(string="Email")
    degree = fields.Selection([
        ('sma', 'SMA'),
        ('smk', 'SMK'),
        ('s1', 'S1'),
        ('s2', 'S2'),
    ])
    major = fields.Char(string="Universitas")
    universitas = fields.Char(string="Major")
    notes = fields.Char(string="Additional Notes")
    attachment = fields.Binary(string="Attachment File", max_file_size=1048576)
