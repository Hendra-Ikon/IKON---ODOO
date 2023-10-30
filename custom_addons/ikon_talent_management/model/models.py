import logging
from odoo import models, fields, api
import requests
from bs4 import BeautifulSoup
import re
import json
from odoo.exceptions import UserError 
from fuzzywuzzy import fuzz
from collections import Counter

_logger = logging.getLogger(__name__)

class TalentManagement(models.Model):
    _name = 'talent.management.talent'
    _description = 'Talent Management'

    position = fields.Char(string='Position', required=True)
    skill_ids = fields.Many2many('hr.skill', string='Add Skill')
    description = fields.Text(string='Description')
    custom_search_link = fields.Char(string='Custom Search Link', compute='_compute_custom_search_link')
    custom_search_data = fields.Text(string='Custom Search Data', compute='_compute_custom_search_data', store=True)
    limit = fields.Integer(string='Limit', required=True)
    opentowork = fields.Boolean(string='OpenToWork')
    talent_ids = fields.One2many('talent.management.talent.inherit', 'talent_id', string='Talent')
    approved = fields.Boolean(string='Approved')  # A field to mark as approved
    
    
    def toggle_approved(self):
        # Toggle the 'approved' field value.
        for record in self:
            record.write({'approved': not record.approved})

    @api.depends('position', 'skill_ids', 'limit', 'opentowork')
    def _compute_custom_search_link(self):
        base_url = "https://www.google.com/search?q=site:linkedin.com/in/"
        for record in self:
            if record.position and record.skill_ids:
                position = f'"{record.position}"'
                skills = ' '.join(f'"{skill.name}"' for skill in record.skill_ids)
                opentowork = "opentowork" if record.opentowork else ""
                ina = "in indonesia"
                search_query = f'{position} {skills} {opentowork} {ina}'
                custom_search_url = f"{base_url}+{search_query}"
                record.custom_search_link = custom_search_url
                _logger.info(custom_search_url)
            else:
                record.custom_search_link = False

    @api.depends('custom_search_link', 'limit')
    def _compute_custom_search_data(self):
        for record in self:
            if record.custom_search_link:
                limit = record.limit
                self._get_custom_search_data(record, limit)

    # Your existing function
    # Your existing function
    def _get_custom_search_data(self, record, limit):
        try:
            response = requests.get(record.custom_search_link)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                name_elements = soup.find_all('div', {'class': 'BNeawe vvjwJb AP7Wnd'})

                existing_names = self.talent_ids.mapped('name')  # Get existing names

                for name_element in name_elements[:limit]:
                    text = name_element.text.strip()
                    match = re.match(r'(.+?)\s*-\s*(.+)', text)
                    if match:
                        nama = match.group(1).strip()
                        skills = match.group(2).strip().split(' - ')[0].strip()

                        # Check if the name already exists in the talent_ids
                        if nama not in existing_names:
                            # Find all <a> elements within the current name_element
                            a_tags = soup.find_all('a')
                            for a_tag in a_tags:
                                # Get the href attribute directly from the <a> tag
                                raw_url = a_tag.get('href')
                                
                                # Check if URL matches name using fuzzywuzzy
                                name_parts = nama.split()
                                url_parts = raw_url.split('/')
                                ratio = fuzz.token_set_ratio(name_parts, url_parts)
                                if ratio > 90:  # You can adjust the threshold as needed
                                    # Parse the URL to extract the relevant part
                                    match = re.search(r'https://[^\s&]+', raw_url)
                                    if match:
                                        url = match.group(0)
                                        talent_inherit = self.env['talent.management.talent.inherit'].create({
                                            'name': nama,
                                            'skill': skills,
                                            'url': url,
                                        })
                                        talent_inherit.talent_id = record.id
                                        existing_names.append(nama)  # Add to existing names

                _logger.info(f"Data successfully retrieved: {len(name_elements)} records created")
            else:
                error_message = "Failed to download the web page. Status code: %d" % response.status_code
                raise UserError(error_message)
        except Exception as e:
            error_message = "An error occurred while downloading the web page: %s" % str(e)
            raise UserError(error_message)

    
