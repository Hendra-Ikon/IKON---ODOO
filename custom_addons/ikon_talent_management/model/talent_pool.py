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

        for row in range(1, sheet.nrows):
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

    def get_field_name(self, column_name):

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


class TalentData(models.Model):
    _name = "talent.pool.data"

    no = fields.Integer(string="No")
    nama = fields.Char(string="Nama")
    email = fields.Char(string="Email")
    posisi = fields.Char(string="Posisi")
    sumber = fields.Char(string="Sumber")
    degree = fields.Selection([
        ('sma', 'SMA'),
        ('smk', 'SMK'),
        ('s1', 'S1'),
        ('s2', 'S2'),
    ])
    major = fields.Char(string="Major")
    universitas = fields.Char(string="Universitas")
    notes = fields.Char(string="Additional Notes")
    attachment = fields.Binary(string="Attachment File", max_file_size=1048576)
    job_id = fields.Many2one('hr.job', string='Move to Applicant')

    def move_to_applicant(self):

        for appl in self:

            job_name = appl.job_id.name if appl.job_id else ''

            applicant_name = f'{appl.name} - {job_name}'

            hr_applicant = self.env['hr.applicant'].create({
                'name': applicant_name,
                'partner_name': appl.name,
                'partner_mobile': appl.no_tlp,
                'job_id': appl.job_id.id,
                # 'cover_letter': record.skill,
                'linkedin_profile': appl.url,
                'description': appl.experience,
            })

            message = "Successfully move to applicant"
            action = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': message,
                    'sticky': False,
                }
            }

            return action

