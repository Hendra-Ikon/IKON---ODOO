from odoo import models, fields, api
import logging
from odoo.exceptions import UserError 
_logger = logging.getLogger(__name__)

class TalentManagementTalentInherit(models.Model):
    _name = 'talent.management.talent.inherit'
    _description = 'Inherited Talent Management'

    name = fields.Char(string='Name', required=True)
    no_tlp = fields.Char(string='Phone Number')
    skill = fields.Char(string='Headline', required=True)
    talent_id = fields.Many2one('talent.management.talent', string='Talent')
    url = fields.Char(string='URL Linkedin')
    experience = fields.Char(string='Experience')

    name_url_set = fields.Char(compute='_compute_name_url_set')
    job_id = fields.Many2one('hr.job', string='Job Name')
    
    

    def _compute_name_url_set(self):
        for record in self:
            # Combine name and URL to create a unique identifier
            name_url_set = f"{record.name}|{record.url}"
            record.name_url_set = name_url_set

    def toggle_approved(self):
         for record in self:
            # Mendapatkan nama pekerjaan dari hr.job
            job_name = record.job_id.name if record.job_id else ''

            # Menggabungkan nama pekerjaan dengan nama talent
            applicant_name = f"{record.name} - {job_name}"

            # Create a new HR Applicant record based on the data from the talent record
            hr_applicant = self.env['hr.applicant'].create({
                'name': applicant_name,
                'partner_name': record.name,
                'partner_mobile': record.no_tlp,
                'job_id': record.job_id.id,
                # 'cover_letter': record.skill,
                'linkedin_profile': record.url,
                'description': record.experience,
            })
            _logger.info(f"HR Applicant created: {hr_applicant.name}")

            # Tampilkan pesan informasi
            message = "HR Applicant created successfully."
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










    