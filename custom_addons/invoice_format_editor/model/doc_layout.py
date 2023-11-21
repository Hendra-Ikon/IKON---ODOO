# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Jumana Jabin MK(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
"""doc layout"""
from odoo import models, fields


class AddDocumentTemplate(models.Model):
    """Doc layout model"""
    _name = "doc.layout"
    _description = 'Adding the fields for customization'
    _rec_name = 'name'

    name = fields.Char("Name")
    base_color = fields.Char(srting="Base Color",
                             help="Background color for the invoice")
    heading_text_color = fields.Char(srting="Heading text Color",
                                     help="Heading Text color")
    text_color = fields.Char(srting="Text Color", help="Text color of items")
    customer_text_color = fields.Char(srting="Customer Text Color",
                                      help="Customer address text color")
    company_text_color = fields.Char(srting="Company Text Color",
                                     help="Company address Text color")
    logo_position = fields.Selection(selection=[('left', 'Left'), ('right', 'Right')],
                                     string="Logo Position",
                                     help="Company logo position")
    tagline_position = fields.Selection(selection=[('left', 'Left'), ('right', 'Right')],
                                        string="Tagline Position",
                                        help="Company Tagline position")
    customer_position = fields.Selection(
        selection=[('left', 'Left'), ('right', 'Right')], string="Customer position",
        help="Customer address position")
    company_position = fields.Selection(selection=[('left', 'Left'), ('right', 'Right')],
                                        string="Company Address Position",
                                        help="Company address position")
    sales_person = fields.Boolean(string='Sales person', default=True,
                                  help="Sales Person")
    description = fields.Boolean(string='Description', default=True,
                                 help="Description")
    tax_value = fields.Boolean(string='Tax', default=True, help="Tax")
    reference = fields.Boolean(string='Customer Reference', default=True,
                               help="Customer Reference")
    source = fields.Boolean(string='Source', default=False,
                            help="Source Document")
    address = fields.Boolean(string='Address', default=True,
                             help="Address")
    city = fields.Boolean(string='City', default=True,
                          help="City")
    country = fields.Boolean(string='Country', default=True,
                             help="Country")
    vat = fields.Boolean(string='VAT', default=True,
                         help='Customer vat id')
    
    spk = fields.Boolean(string='SPK No.', default=True,
                                  help="SPK No" )
    agreement_no = fields.Boolean(string="Agreement No", default=True,
                                  help="Agreement No")
    payment_for_service = fields.Boolean(string='Payment For Service',default=True,
                                  help="Payment For Service")
    payment_for = fields.Boolean(string='Payment For',default=True,
                                  help="Payment For")
    
    # project_name = fields.Boolean(string="Project Name")
    # po_fif_no = fields.Boolean(string="PO No.")
    # po_date = fields.Boolean(string="PO. Date")
    
    po_no = fields.Boolean(string="PO No.")

    period = fields.Boolean(string="Period")

    top = fields.Boolean(string="Term Of Payment")
    
    
    item_id = fields.Boolean(string="Item ID")
    item_description = fields.Boolean(string="Item Description")
    period = fields.Boolean(string="Period")



    
