from odoo import models, fields, api
import logging
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class CustomInvoiceLayout(models.TransientModel):

    _inherit = 'sale.advance.payment.inv'
    base_layout = fields.Selection(related='company_id.base_layout',
                                   readonly=False,
                                   help="Base layout selection field inside "
                                        "document layout model")
    
    # document_layout_id = fields.Many2one(
    #     related='company_id.document_layout_id', readonly=False,
    #     help="custom document layouts")
    
    



    #=== BUSINESS METHODS ===#

    def _create_invoices(self, sale_orders):
       

            
        # logger.info("sale_data", datas)

        
        # ids = 0
        # if ids > 0:
       
        
        
        if self.advance_payment_method == 'delivered':
            return sale_orders._create_invoices(final=self.deduct_down_payments)
        else:
            self.sale_order_ids.ensure_one()
            self = self.with_company(self.company_id)
            order = self.sale_order_ids

            # Create deposit product if necessary
            if not self.product_id:
                self.product_id = self.env['product.product'].create(
                    self._prepare_down_payment_product_values()
                )
                self.env['ir.config_parameter'].sudo().set_param(
                    'sale.default_deposit_product_id', self.product_id.id)

            # Create down payment section if necessary
            if not any(line.display_type and line.is_downpayment for line in order.order_line):
                self.env['sale.order.line'].create(
                    self._prepare_down_payment_section_values(order)
                )

            down_payment_so_line = self.env['sale.order.line'].create(
                self._prepare_so_line_values(order)
            )

            invoice = self.env['account.move'].sudo().create(
                self._prepare_invoice_values(order, down_payment_so_line)
            ).with_user(self.env.uid)  # Unsudo the invoice after creation
            # ids.append(invoice.id.id)
            
             
            invoice.message_post_with_view(
                'mail.message_origin_link',
                values={'self': invoice, 'origin': order},
                subtype_id=self.env.ref('mail.mt_note').id)
        
            return invoice
        
# class CustomInvoiceMovet(models.Model):
#     _inherit = 'account.move'
    
#     @api.model_create_multi
#     def create(self, vals_list):
        

#         # Your custom logic to update company_id
#         for vals in vals_list:
#             if 'company_id' in vals:
#                 id = vals['partner_id']
        
#         # Fix typo in 'search', not 'serach'
#                 comp_id = self.env['res.company'].search([('partner_id', '=', id)])
        
#                 # Change or update the company_id value as needed
#                 vals['company_id'] = comp_id.id # Change 2 to the desired company_id

#         if any('state' in vals and vals.get('state') == 'posted' for vals in vals_list):
#             raise UserError(_('You cannot create a move already in the posted state. Please create a draft move and post it after.'))

#         container = {'records': self}
#         with self._check_balanced(container):
#             with self._sync_dynamic_lines(container):
#                 moves = super().create([self._sanitize_vals(vals) for vals in vals_list])
#                 container['records'] = moves
#             for move, vals in zip(moves, vals_list):
#                 if 'tax_totals' in vals:
#                     move.tax_totals = vals['tax_totals']
#         return moves