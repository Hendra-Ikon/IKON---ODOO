from odoo import models, api, _, fields
from odoo.tools import float_is_zero, float_compare
import logging
import re
from odoo.fields import Command

logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # price_unit = fields.Float('Unit Price', tracking=True, required=True, digits='Product Price', default=0.0, track_visibility = 'always')
    invoice_count = fields.Integer(related='order_id.invoice_count')
    item_id = fields.Char(string="Item ID")
    item_description = fields.Char(string="Item Description")
    period = fields.Date(string="Period")
    po_number = fields.Char(string="PO")
    # monthly_rate = fields.Integer(string="Monthly Rate (IDR)")
    # monthly_rate = fields.Float(
    #     string="Monthly Rate (IDR)",
    #     compute='_compute_monthly_rate',
    #     digits='Product Price',
    #     store=True, readonly=False, required=True, precompute=True)
 

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
    
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax']
        

            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': amount_untaxed + amount_tax,
            })
    # @api.depends('monthly_rate', 'product_uom_qty','price_subtotal','tax_id','price_total','order_id')
    # def _compute_monthly_rate(self):      
    #     for line in self:
    #         tax_id_str = str(line.tax_id.id)
    #         order_ids = str(line.order_id.id)
    #         match_orderID = re.search(r'_(\d+)', tax_id_str)
    #         match = re.search(r'_(\d+)', tax_id_str)
    #         if match:
    #             tax_id = int(match.group(1))
    #             order_id = int(match_orderID.group(1))
    #             tax = self.env['account.tax'].browse(tax_id)

            
    #             if line.monthly_rate:
    #                 line.price_subtotal = line.product_uom_qty * line.monthly_rate
    #                 line.price_tax = (line.price_subtotal * tax.amount) / 100
    #                 line.price_total = line.price_subtotal + line.price_tax

    #                 price_subtotal = line.price_subtotal
    #                 price_tax = line.price_tax
    #                 price_total = line.price_total
    #                 # line.update({
    #                 #     'price_subtotal': price_subtotal,
    #                 #     'price_tax': price_tax,
    #                 #     'price_total': price_total 
    #                 # })
    #                 sale_order_line = self.env['sale.order.line'].search([('order_id', '=', order_id)])  # Sesuaikan dengan kriteria pencarian yang sesuai
    #                 sale_order_line.write({
    #                     'price_subtotal': price_subtotal,
    #                     'price_tax': price_tax,
    #                     'price_total': price_total,
    #                 })
    #                 logger.info("test",sale_order_line)

    def _prepare_invoice_line(self, **optional_values):
        """Prepare the values to create the new invoice line for a sales order line.

        :param optional_values: any parameter that should be added to the returned invoice line
        :rtype: dict
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type or 'product',
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [Command.set(self.tax_id.ids)],
            'sale_line_ids': [Command.link(self.id)],
            'is_downpayment': self.is_downpayment,
            'item_id': self.item_id,
            'item_description': self.item_description,
            'period': self.period,
            'po_number': self.po_number,
        }
        analytic_account_id = self.order_id.analytic_account_id.id
        if self.analytic_distribution and not self.display_type:
            res['analytic_distribution'] = self.analytic_distribution
        if analytic_account_id and not self.display_type:
            analytic_account_id = str(analytic_account_id)
            if 'analytic_distribution' in res:
                res['analytic_distribution'][analytic_account_id] = res['analytic_distribution'].get(analytic_account_id, 0) + 100
            else:
                res['analytic_distribution'] = {analytic_account_id: 100}
        if optional_values:
            res.update(optional_values)
        if self.display_type:
            res['account_id'] = False
        return res


    


