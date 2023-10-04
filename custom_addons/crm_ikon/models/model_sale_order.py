from odoo import models, fields
import logging

logger = logging.getLogger(__name__)

class CrmSaleOrder(models.Model):
    _inherit = "sale.order"
    
    attention = fields.Char(string="Attention")
    project_name = fields.Char(string="Project Name")
    po_fif_no = fields.Char(string="PO. FIF No.")
    # po_date = fields.Date(string="PO. Date")
    pr_no = fields.Char(string="PR No.")
    
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

    def _get_order_lines_to_report(self):
        down_payment_lines = self.order_line.filtered(lambda line:
            line.is_downpayment
            and not line.display_type
            and not line._get_downpayment_state()
        )

        def show_line(line):
            if not line.is_downpayment:
                return True
            elif line.display_type and down_payment_lines:
                return False  
            elif line.display_type and not down_payment_lines:
                return True
            elif line in down_payment_lines:
                return False  
            else:
                return False

        return self.order_line.filtered(show_line)