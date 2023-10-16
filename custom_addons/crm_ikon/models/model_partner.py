from odoo import models, fields

class CrmPartner(models.Model):
    _inherit = "res.partner"
    
    linkedin_url = fields.Char(string="LinkedIn")
    headline = fields.Char(string="Headline")