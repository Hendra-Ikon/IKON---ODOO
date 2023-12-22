from odoo import models, fields, api, _
import logging
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
import time

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
        invoice = None  # Initializing the variable outside the loop

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
            
            if self.advance_payment_method == 'monthly':
                for i in range(1, int(self.monthly_payment_duration) + 1):
                        month = i
                        down_payment_so_line = self.env['sale.order.line'].create(
                        self._prepare_so_line_values(order, month)
                    ) 
                        invoice_values = self._prepare_invoice_values(order, down_payment_so_line, month)
                        invoice = self.env['account.move'].sudo().create(invoice_values).with_user(self.env.uid) 
                
                return invoice.message_post_with_view(
                        'mail.message_origin_link',
                        values={'self': invoice, 'origin': order},
                        subtype_id=self.env.ref('mail.mt_note').id)
            else:
                down_payment_so_line = self.env['sale.order.line'].create(
                self._prepare_so_line_values(order, month=0)
            )

                invoice = self.env['account.move'].sudo().create(
                    self._prepare_invoice_values(order, down_payment_so_line, month=0)
                ).with_user(self.env.uid)  # Unsudo the invoice after creation

                invoice.message_post_with_view(
                    'mail.message_origin_link',
                    values={'self': invoice, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id)
        return invoice
        
    
            
    def _prepare_so_line_values(self, order, month):
        self.ensure_one()
        analytic_distribution = {}
        amount_total = sum(order.order_line.mapped("price_total"))
        if not float_is_zero(amount_total, precision_rounding=self.currency_id.rounding):
            for line in order.order_line:
                distrib_dict = line.analytic_distribution or {}
                for account, distribution in distrib_dict.items():
                    analytic_distribution[account] = distribution * line.price_total + analytic_distribution.get(account, 0)
            for account, distribution_amount in analytic_distribution.items():
                analytic_distribution[account] = distribution_amount/amount_total
        context = {'lang': order.partner_id.lang}
        if month != 0:
            name = _('Monthly Payment %s: %s') % (int(month), time.strftime('%m %Y'))
            logger.info("1")
        else:
            name = _('Down Payment: %s ', time.strftime('%m %Y'))
            logger.info("2")
        so_values = {
            'name': name,
            'price_unit': self._get_down_payment_amount(order),
            'product_uom_qty': 0.0,
            'order_id': order.id,
            'discount': 0.0,
            'product_id': self.product_id.id,
            'analytic_distribution': analytic_distribution,
            'is_downpayment': True,
            'sequence': order.order_line and order.order_line[-1].sequence + 1 or 10,
        }
        del context
        return so_values
        
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