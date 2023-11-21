from odoo import models, fields, api
import logging
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Command
logger = logging.getLogger(__name__)
from itertools import groupby



class CrmSaleOrder(models.Model):
    _inherit = "sale.order"
    
    attention = fields.Char(string="Attention")
    project_name = fields.Char(string="Project Name")

    po_no = fields.Char(string="PO No.")
    po_date = fields.Date(string="PO. Date")
    payment_for = fields.Char(string="Payment For")
    period = fields.Date(string="Period")
    payment_for_service = fields.Char(string="Payment For Service")
    spv = fields.Many2one('res.partner', string='SPV', domain="[('is_company','=',True)]")
    agreement_no = fields.Char(string="Agreement No")
    spk_no = fields.Char(string="SPK No")

    month = fields.Date(string="Month")
    

    name = fields.Text(
        string="Description",
        compute='_compute_name',
        tracking=True,
        store=True, readonly=False, required=True, precompute=True)
        


    def _get_order_lines_to_report_payment(self):
        down_payment_lines = self.order_line.filtered(lambda line:
            line.is_downpayment
            and not line.display_type
        )
        
        def show_line(line):
            if line in down_payment_lines:
                return True
            else:
                return False
        
        return self.order_line.filtered(show_line)


 
        




   



    
