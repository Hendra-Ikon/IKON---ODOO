import base64

import xlrd
from odoo import models, fields, api
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
            'Additional Notes': 'notes',
        }
        return field_mapping.get(column_name)



class TalentData(models.Model):
    _name = "talent.pool.data"
    _description = 'Talent Pool Data'

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
        ('s3', 'S3'),
        ('d1', 'D1'),
        ('d2', 'D2'),
        ('d3', 'D3'),
        ('d4', 'D4'),
        ('undergraduate', 'Undergraduate'),
    ])
    major = fields.Char(string="Major")
    universitas = fields.Char(string="Universitas")
    notes = fields.Char(string="Additional Notes")
    attachment = fields.Binary(string="Attachment File", max_file_size=1048576, filename="attachment_filename")
    attachment_filename = fields.Char(string="Attachment filename", compute="_compute_attachment_filename")
    cv_ikon = fields.Binary(string="IKON CV", max_file_size=1048576, filename="cv_ikon_filename")
    cv_ikon_filename = fields.Char(string="IKON CV filename", compute="_compute_cv_ikon_attachment_filename")
    job_id = fields.Many2one('hr.job', string='Move to Applicant')

    @api.depends('nama')
    def _compute_attachment_filename(self):
        for record in self:
            if record.nama:
                record.attachment_filename = f"{record.nama}.pdf"
            else:
                record.attachment_filename = False

    @api.depends('nama')
    def _compute_cv_ikon_attachment_filename(self):
        for record in self:
            if record.nama:
                record.cv_ikon_filename = f"{record.nama} IKON CV.pdf"
            else:
                record.cv_ikon_filename = False

    # @api.model
    # def create(self, values):
    #     # Extract the file name from the imported file and set it to the "attachment" field
    #     if 'attachment' in values and 'filename' in values['attachment']:
    #         values['attachment_filename'] = values['attachment']['filename']
    #     return super(TalentData, self).create(values)

    @api.model
    def create(self, values):
        if 'attachment' in values and isinstance(values['attachment'], dict) and 'filename' in values['attachment']:
            values['attachment_filename'] = values['attachment']['filename']
        return super(TalentData, self).create(values)

    def move_to_applicant(self):

        for appl in self:

            job_name = appl.job_id.name if appl.job_id else ''

            applicant_name = f'{appl.nama} - {job_name}'

            attachment_data = appl.attachment
            attachment_data_base64 = False
            attachment_name = "Attachment"  # Default name if attachment_data is not present
            if attachment_data:
                attachment_data_base64 = base64.b64encode(attachment_data).decode('utf-8')
                attachment_name = f'CV-{appl.nama}' or "Attachment"

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
                "attachment_ids": [(0, 0, {
                    'name': attachment_name,
                    'datas': appl.attachment,
                    'res_model': 'hr.applicant',
                })],
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

    from_talent_posisi = fields.Char(string="Posisi", store=True)
    from_talent_sumber = fields.Char(string="Sumber")
    from_talent_degree = fields.Selection([
        ('sma', 'SMA'),
        ('smk', 'SMK'),
        ('s1', 'S1'),
        ('s2', 'S2'),
        ('s3', 'S3'),
        ('d1', 'D1'),
        ('d2', 'D2'),
        ('d3', 'D3'),
        ('d4', 'D4'),
        ('undergraduate', 'Undergraduate'),
    ])
    from_talent_major = fields.Char(string="Major")
    from_talent_universitas = fields.Char(string="Universitas")
    from_talent_notes = fields.Char(string="Additional Notes")
    from_talent_attachment = fields.Binary(string="Attachment File", max_file_size=1048576)

    def move_to_talent_pool(self):

        for data in self:
            attachment_data = False
            attachment_name = False
            for attachment in data.attachment_ids:
                attachment_data = attachment.datas
                attachment_name = attachment.name
            attachment_vals = {
                'name': attachment_name,
                'datas': attachment_data,
                'res_model': 'hr.applicant',  # Assuming this is the correct model
            }

            talent_data = self.env["talent.pool.data"].create({
                "nama": data.partner_name,
                "email": data.email_from,
                "posisi": data.from_talent_posisi,
                "sumber": data.from_talent_sumber,
                "degree": data.from_talent_degree,
                "major": data.from_talent_major,
                "universitas": data.from_talent_universitas,
                "notes": data.from_talent_notes,
                "attachment": attachment_data,

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

