import xlrd
from odoo import models, fields
from base64 import b64decode
import logging
_logger = logging.getLogger(__name__)

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

        action = {
            'name': 'Talent Data',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'talent.pool.data',
            'view_id': False,
            'target': 'current',
            'menu_id': 273,
        }

        return action

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
    job_id = fields.Many2one('hr.job', string='Move to Applicant', required=True)

    def move_to_applicant(self):

        for appl in self:

            job_name = appl.job_id.name if appl.job_id else ''

            applicant_name = f'{appl.nama} - {job_name}'

            temp_degree = fields.Char(string="Temporary Degree Value")
            if appl.degree:
                temp_degree = appl.degree
            source_id = self.env['utm.source'].search([('name', '=', appl.sumber)], limit=1)
            degree_id = self.env['hr.recruitment.degree'].search([('name', '=', appl.degree.upper())], limit=1)


            if not source_id:
                source_id = self.env['utm.source'].create({
                    'name': appl.sumber,
                    # Add other fields as needed
                })

            if not degree_id:
                degree_id = self.env['hr.recruitment.degree'].create({
                    'name': appl.degree.upper(),
                    # Add other fields as needed
                })

            print(f"********* DEGREE *********: {appl.degree}")

            hr_applicant = self.env['hr.applicant'].create({
                'name': applicant_name,
                'partner_name': appl.nama,
                'email_from': appl.email,
                "from_talent_posisi": appl.posisi,
                'source_id': source_id.id if source_id else False,
                "from_talent_sumber": appl.sumber,
                'type_id': degree_id.id if degree_id else False,
                "from_talent_degree": appl.degree,
                "from_talent_major": appl.major,
                "from_talent_universitas": appl.universitas,
                "from_talent_notes": appl.notes,
                "from_talent_attachment": appl.attachment,
                'job_id': appl.job_id.id,
            })

            self.unlink()

            message = "Successfully move to applicant"
            action = {
                'name': 'Talent Data',
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': 'talent.pool.data',
                'view_id': False,
                'target': 'current',
                'menu_id': 273,
            }

            return action

class HrApplicantInherit(models.Model):

    _inherit = "hr.applicant"

    from_talent_posisi = fields.Char(string="Posisi")
    from_talent_sumber = fields.Char(string="Sumber")
    from_talent_degree = fields.Selection([
        ('sma', 'SMA'),
        ('smk', 'SMK'),
        ('s1', 'S1'),
        ('s2', 'S2'),
    ])
    from_talent_major = fields.Char(string="Major")
    from_talent_universitas = fields.Char(string="Universitas")
    from_talent_notes = fields.Char(string="Additional Notes")
    from_talent_attachment = fields.Binary(string="Attachment File", max_file_size=1048576)

    def move_to_talent_pool(self):

        for data in self:

            talent_data = self.env["talent.pool.data"].create({
                "nama": data.partner_name,
                "email": data.email_from,
                "posisi": data.from_talent_posisi,
                "sumber": data.from_talent_sumber,
                "degree": data.from_talent_degree,
                "major": data.from_talent_major,
                "universitas": data.from_talent_universitas,
                "notes": data.from_talent_notes,
                "attachment": data.from_talent_attachment

            })

            self.unlink()

            action = {
                'name': 'Talent Data',
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': 'talent.pool.data',
                'view_id': False,
                'target': 'current',
                'menu_id': 273,
            }

            return action

