from odoo import models, api, _, fields
from odoo.tools import float_is_zero, float_compare
import logging

logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_unit = fields.Float('Unit Price', tracking=True, required=True, digits='Product Price', default=0.0, track_visibility = 'always')
    
    invoice_count = fields.Integer(related='order_id.invoice_count')
    

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('display_type') or self.default_get(['display_type']).get('display_type'):
                vals['product_uom_qty'] = 0.0
           
            if vals['name'] == 'Down Payments' and vals['display_type'] == 'line_section' and vals['is_downpayment']:
                vals['name'] = 'Term Payments'
                continue 
            if 'product_id' in vals and 'is_downpayment' in vals:
                vals['name'] = vals['name'].replace('Down', 'Term')
                continue
           
        lines = super().create(vals_list)
        for line in lines:
            if line.product_id and line.state == 'sale':
                msg = _("Extra line with %s", line.product_id.display_name)
                line.order_id.message_post(body=msg)
                # create an analytic account if at least an expense product
                if line.product_id.expense_policy not in [False, 'no'] and not line.order_id.analytic_account_id:
                    line.order_id._create_analytic_account()
        return lines
    
    def unlink(self):
        for line in self:
            if line.is_downpayment and line.display_type == False:
                data_price = self.search([('order_id', '=', line.order_id.id),('is_downpayment', '=', False)])
                total_price = sum(x.price_total for x in data_price)
                term_payment = self.search([('order_id', '=', line.order_id.id), ('is_downpayment', '=', True)])
                total_payment  = sum(x.price_reduce for x in term_payment if x.id != line.id)
                if total_payment < total_price:
                    for x in self.search([('order_id', '=', line.order_id.id)]):
                        x.invoice_status = 'to invoice'
        return super().unlink()
    
    @api.depends('state', 'product_uom_qty', 'qty_delivered', 'qty_to_invoice', 'qty_invoiced', 'price_reduce', 'name')
    def _compute_invoice_status(self):
        """
        Compute the invoice status of a SO line. Possible statuses:
        - no: if the SO is not in status 'sale' or 'done', we consider that there is nothing to
          invoice. This is also the default value if the conditions of no other status is met.
        - to invoice: we refer to the quantity to invoice of the line. Refer to method
          `_compute_qty_to_invoice()` for more information on how this quantity is calculated.
        - upselling: this is possible only for a product invoiced on ordered quantities for which
          we delivered more than expected. The could arise if, for example, a project took more
          time than expected but we decided not to invoice the extra cost to the client. This
          occurs only in state 'sale', so that when a SO is set to done, the upselling opportunity
          is removed from the list.
        - invoiced: the quantity invoiced is larger or equal to the quantity ordered.
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for line in self:
            if line.state not in ('sale', 'done'):
                line.invoice_status = 'no'
            elif line.is_downpayment and line.display_type == False:
                data_price = self.search([('order_id', '=', line.order_id.id),('is_downpayment', '=', False)])
                total_price = sum(x.price_total for x in data_price)
                term_payment = self.search([('order_id', '=', line.order_id.id),('is_downpayment', '=', True)])
                total_payment  = sum(x.price_reduce for x in term_payment)
                if total_payment >= total_price and line.invoice_lines.move_id.state == 'posted':
                    for x in self.search([('order_id', '=', line.order_id.id)]):
                        x.invoice_status = 'invoiced'
                else:
                    for x in self.search([('order_id', '=', line.order_id.id)]):
                        x.invoice_status = 'to invoice'
            elif line.is_downpayment and line.untaxed_amount_to_invoice == 0:
                line.invoice_status = 'invoiced'
            elif not float_is_zero(line.qty_to_invoice, precision_digits=precision):
                line.invoice_status = 'to invoice'
            elif line.state == 'sale' and line.product_id.invoice_policy == 'order' and\
                    line.product_uom_qty >= 0.0 and\
                    float_compare(line.qty_delivered, line.product_uom_qty, precision_digits=precision) == 1:
                line.invoice_status = 'upselling'
            elif float_compare(line.qty_invoiced, line.product_uom_qty, precision_digits=precision) >= 0:
                line.invoice_status = 'invoiced'
            else:
                line.invoice_status = 'no'
        
    @api.depends('display_type', 'product_id', 'product_packaging_qty')
    def _compute_product_uom_qty(self):
        for line in self:
            if line.display_type:
                line.product_uom_qty = 0.0
                continue
            
            if not line.product_packaging_id:
                continue
            packaging_uom = line.product_packaging_id.product_uom_id
            qty_per_packaging = line.product_packaging_id.qty
            product_uom_qty = packaging_uom._compute_quantity(
                line.product_packaging_qty * qty_per_packaging, line.product_uom)
            if float_compare(product_uom_qty, line.product_uom_qty, precision_rounding=line.product_uom.rounding) != 0:
                line.product_uom_qty = product_uom_qty


class LogDetailSale(models.Model):
    _name = 'log.detail.sale'
    _description = 'Log Detail Sale'

    name = fields.Char(string='Name', required=True)
    price_old = fields.Float(string='Old Price')
    price_new = fields.Float(string='New Price')
    change_date = fields.Datetime(string='Change Date')
