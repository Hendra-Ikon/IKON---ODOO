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
"""Inherit account move model"""
from odoo import models, fields, api


class TemplateInvoice(models.Model):
    """Inheriting the account move model and added the base layout model and
    a relational field to doc layout model"""
    _inherit = 'account.move'

    base_layout = fields.Selection(selection=[
                                              ('old', 'Old Standard'),
                                              ('fif', 'Fif'),
                                              ('stp', 'Solusi Tunas Pratama'),
                                              ('btpn', 'BTPN'),
                                              ('bciv1', 'Bank Commonwealth Indonesia V1'),
                                              ('bciv2', 'Bank Commonwealth Indonesia V2'),
                                              ('bbs', 'Basis Bay Singapore'),
                                              ('dkatalis', 'Dkatalis'),
                                              ('mandiri', 'Mandiri'),
                                              ('bni','BNI'),
                                              ('aia','AIA'),
                                              ('lps','Licences / Product Sales')],
                                   required=True,
                                   string="Invoice Document Layout",
                                   default="default")
    theme_id = fields.Many2one('doc.layout',
                               related='company_id.document_layout_id')
    # spk = fields.Char(string='SPK No.')
    # agreement_no = fields.Char(string="Agreement No")
    # payment_for_service = fields.Char(string='Payment For Service')
    # payment_for = fields.Char(string='Payment For')
    # project_name = fields.Boolean(string="Project Name")
    # po_fif_no = fields.Boolean(string="PO No.")
    # po_date = fields.Boolean(string="PO. Date")
    
    # pr_no = fields.Boolean(string="PR No.")

    





