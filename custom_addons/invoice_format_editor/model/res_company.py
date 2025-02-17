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
"""res company"""
from odoo import models, fields


class ReportCompanyTemplate(models.Model):
    """Inheriting the res company model"""
    _inherit = 'res.company'

    base_layout = fields.Selection(selection=[('default', 'Default'),
                                              ('fif', 'PT Federal International Finance'),
                                              ('stp', 'PT Solusi Tunas Pratama Tbk'),
                                              ('btpn', 'PT Bank BTPN Tbk'),
                                              ('bciv1', 'Bank Commonwealth Indonesia V1'),
                                              ('bciv2', 'Bank Commonwealth Indonesia V2'),
                                              ('bbs', 'Basis Bay Singapore'),
                                              ('dkatalis', 'Dkatalis'),
                                              ('mandiri', 'PT Bank Mandiri (Persero) Tbk'),
                                              ('bni','PT Bank Negara Indonesia Tbk'),
                                              ('aia','PT Asuransi AIA Indonesia'),
                                              ('lps','Licences / Product Sales')],
                                   required=True,
                                   string="Invoice Document Layout",
                                   help="base layout selection",
                                   default="default")
    document_layout_id = fields.Many2one("doc.layout",
                                         string="Invoice Layout Configuration",
                                         help="Invoice layout configuration")
