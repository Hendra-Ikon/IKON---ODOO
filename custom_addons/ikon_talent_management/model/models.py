import logging
from odoo import models, fields, api
import requests
from bs4 import BeautifulSoup
import re
import json
from odoo.exceptions import UserError 
from fuzzywuzzy import fuzz
from collections import Counter
import xlsxwriter
import io
import base64
from urllib.parse import unquote, urlparse


_logger = logging.getLogger(__name__)

class TalentManagement(models.Model):
    _name = 'talent.management.talent'
    _description = 'Talent Management'
    _inherit = ['mail.thread']

    REGION_SELECTION = [
        ('any', 'Any'),
        ('jabodetabek', 'Jabodetabek'),
        ('jakarta', 'Jakarta'),
        ('surabaya', 'Surabaya'),
        ('bandung', 'Bandung'),
        ('medan', 'Medan'),
        ('makassar', 'Makassar'),
        ('palembang', 'Palembang'),
        # Tambahkan kota-kota lain di sini
    ]

    position = fields.Char(string='Position', required=True, tracking=True)
    keyword = fields.Text(string='Keyword', tracking=True)
    description = fields.Text(string='Description')
    custom_search_link = fields.Char(string='Custom Search Link', compute='_compute_custom_search_link')
    custom_search_data = fields.Text(string='Custom Search Data', compute='_compute_custom_search_data', store=True)
    limit = fields.Integer(string='Limit', required=True, default=20)
    region = fields.Selection(REGION_SELECTION, string='Domicile', default='any')
    opentowork = fields.Boolean(string='OpenToWork')
    talent_ids = fields.One2many('talent.management.talent.inherit', 'talent_id', string='Talent')
    approved = fields.Boolean(string='Approved')  # A field to mark as approved
    count_talent = fields.Integer(string='Count of Talent', compute='_compute_count_talent')

    def customLogs(self):
        self.message_post(body="Hellow word")


    @api.depends('talent_ids')
    def _compute_count_talent(self):
        for record in self:
            # Menghitung jumlah bakat (talent) berdasarkan talent_id yang sama dengan self.id
            count = len(record.talent_ids)
            record.count_talent = count
    
    

    @api.depends('position', 'keyword', 'limit', 'opentowork', 'region')
    def _compute_custom_search_link(self):
        base_url = "https://www.google.com/search?q=site:linkedin.com/in/"
        
        for record in self:
            if record.position and record.keyword:
                position = f'"{record.position}"'
                keywords = record.keyword
                opentowork = "opentowork" if record.opentowork else ""
                ina = "work in indonesia"
                
                # Check if the region is set to "Any," and update it to "Indonesia"
                region = record.region if record.region != 'any' else 'indonesia'
                
                search_query = f'{position} {opentowork}  {keywords} {region} {ina}'
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

    #update
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
                        keyword = match.group(2).strip().split(' - ')[0].strip()

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

                                        # Extract the part before '%'
                                        url_before_percent = unquote(url.split('%')[0])

                                        # Check if the URL contains "google.com/imgres?imgurl"
                                        if "google.com/imgres?imgurl" not in url_before_percent:
                                            # Extract the phone number from the URL if available
                                            phone_number = None
                                            phone_match = re.search(r'(\d{4,15})', raw_url)
                                            if phone_match:
                                                phone_number = phone_match.group(0)

                                            talent_inherit = self.env['talent.management.talent.inherit'].create({
                                                'name': nama,
                                                'keyword': keyword,
                                                'url': url_before_percent,  # Use the extracted URL
                                                'no_tlp': phone_number,  # Add the phone number to the model
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
          
    def generate_report(self):
        # Ambil rekaman TalentManagementTalentInherit berdasarkan talent_id yang sesuai dengan self.id
        talent_inherit_records = self.env['talent.management.talent.inherit'].search([('talent_id', '=', self.id)])

        # Buat laporan Excel dengan XlsxWriter
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Buat format header laporan
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'fg_color': '#D7E4BC'})

        # Set kolom header
        headers = ['Name', 'Phone Number', 'Headline', 'URL Linkedin', 'Experience']

        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # Tulis data ke laporan
        for row, talent_inherit_record in enumerate(talent_inherit_records, start=1):
            worksheet.write(row, 0, talent_inherit_record.name)
            worksheet.write(row, 1, talent_inherit_record.no_tlp)
            worksheet.write(row, 2, talent_inherit_record.keyword)
            worksheet.write(row, 3, talent_inherit_record.url)
            worksheet.write(row, 4, talent_inherit_record.experience)

        # Tutup workbook untuk menyimpan laporan
        workbook.close()

        # Simpan file Excel dalam bentuk attachment
        attachment = self.env['ir.attachment'].create({
            'name': 'Talent_List_Report.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.getvalue()),
            'res_model': self._name,
            'res_id': self.id,
        })

        # Return tindakan yang memungkinkan pengguna mengunduh laporan
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}/{attachment.name}',
            'target': 'self',
        }
