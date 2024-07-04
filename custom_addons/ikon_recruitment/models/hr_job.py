from odoo import models, fields, api
import base64
import io
from pdfminer.high_level import extract_text
import logging

_logger = logging.getLogger(__name__)

class HrJob(models.Model):
    _inherit = 'hr.job'

    skill_ids = fields.Many2many('custom.skill', string='Add Skill')
    matching_count = fields.Integer(string='Total Matching', compute='_compute_matching_count')

    hr_applicant_count = fields.Integer(string='Total HR Applicants', compute='_compute_hr_applicant_count')
    hr_applicant_unmatched_count = fields.Integer(string='Total HR Applicants', compute='_compute_unmatched_count')
    
    def _compute_unmatched_count(self):
        match = self.env['hr.job.matching']
        for job in self:
            unmatched_count = self.env['hr.applicant'].search_count([('job_id', '=', job.id)])
            matching_count = match.search_count([('job_id', '=', job.id)])
            job.hr_applicant_unmatched_count = max(unmatched_count - matching_count, 0)

    def _compute_hr_applicant_count(self):
        for job in self:
            job.hr_applicant_count = self.env['hr.applicant'].search_count([('job_id', '=', job.id)])

    def _compute_matching_count(self):
        matching_model = self.env['hr.job.matching']
        for job in self:
            job.matching_count = matching_model.search_count([('job_id', '=', job.id)])

   
    def perform_matching(self):
        # Models job.matching
        matching_model = self.env['hr.job.matching']
        job_id = self.ids[0]
        required_skills_by_job = []

        # hr.applicant Where job_id
        applicant_records = self.env['hr.applicant'].sudo().search([
            ('job_id', "=", job_id)
        ])

        for applicant in applicant_records:
            if applicant.job_id.id == job_id:  # Check if the applicant has the same job ID as the current job
                # Get data attachment where message_main_attachment_id
                attachment_records = self.env['ir.attachment'].sudo().search([
                    ('res_model', '=', 'hr.applicant'),
                    ('mimetype', '=', 'application/pdf'),
                    ('id', '=', applicant.message_main_attachment_id.id)
                ])

                matching_skills = []
                matching_skill_names = []
                required_skills = set(self.skill_ids.mapped('name'))

                for skill in required_skills:
                    skill_found = False

                    for attachment in attachment_records:
                        extracted_text = self.extract_text_from_attachment(attachment)
                        if skill.lower() in extracted_text.lower():
                            skill_found = True
                            matching_skills.append(1)  # Skill found, assign a score of 1
                            matching_skill_names.append(skill)

                        else:
                            matching_skills.append(0)  # Skill not found, assign a score of 0

                matching_skill_count = sum(matching_skills)  # Count of matching skills
                total_required_skills = len(required_skills)
                result = f"{matching_skill_count}/{total_required_skills}"

                applicant_id = applicant.id

                existing_result = applicant.result  # Get the existing result from the hr.applicant

                # Check if the result exists and update it, otherwise create it

                if matching_skill_names:
                    listToStr = ', '.join(map(str, matching_skill_names))
                    applicant_records.write({
                            'custom_skill': listToStr
                        })
                if existing_result:
                    applicant.write({
                        'result': result
                    })
                else:
                    applicant.write({
                        'result': result
                    })

                checkdata = matching_model.search([
                    ("applicant_id", "=", applicant_id)
                ])
                _logger.info(checkdata)
                if not checkdata:
                    matching_model.create({
                        'result': result,
                        'job_id': job_id,
                        'applicant_id': applicant_id,
                        'status': True,
                        'matching_name': self.name,
                    })
                else:
                    for data in checkdata:
                        data.write({
                            'result': result,  # Update the 'result' field with the new result
                            'job_id': job_id,
                            'applicant_id': applicant_id,
                            'status': True,
                            'matching_name': self.name,
                        })

        # Notification message
        message = "HR Matching completed successfully."
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

    def extract_text_from_attachment(self, attachment):
        pdf_data = base64.b64decode(attachment.datas)
        with io.BytesIO(pdf_data) as pdf_file:
            text = extract_text(pdf_file)
        return text
