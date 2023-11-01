from odoo import models, fields, api
import base64
import io
from pdfminer.high_level import extract_text
import logging

_logger = logging.getLogger(__name__)

class HrJobMatching(models.Model):
    _name = 'hr.job.matching'
    _description = 'Job Matching'

    score = fields.Float('Score')
    applicant_id = fields.Integer(string='applicant_id')
    job_id = fields.Many2one('hr.job', 'Job')
    result = fields.Text(string='Matching Result', readonly=True)
    status = fields.Boolean(string='Status', readonly=True)
    matching_name = fields.Text(string='Matching Result', readonly=True)
    

  