from odoo import models, api, fields
import logging

logger = logging.getLogger(__name__)

class CrmAccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Service',
        inverse='_inverse_product_id',
        ondelete='restrict',
    )
    price_unit = fields.Float(
        string='Unit Price',
        compute="_compute_price_unit", store=True, readonly=False, precompute=True,
        digits='Product Price',
    )

    name = fields.Char(
        string='Label',
        compute='_compute_name', store=True, readonly=False, precompute=True,
        tracking=True,
    )
    order_lines = fields.Many2many(
        comodel_name='sale.order.line',
        relation='sale_order_line_invoice_rel', column1='invoice_line_id', column2='order_line_id',
        string="order Lines",
        copy=False)
    
    item_id = fields.Char(string="Item ID")
    item_description = fields.Char(string="Item Description")
    period = fields.Date(string="Period")
    
    
    
    @api.depends('product_id', 'product_uom_id')
    def _compute_price_unit(self):
        for line in self:
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue
            if line.move_id.is_sale_document(include_receipts=True):
                document_type = 'sale'
            elif line.move_id.is_purchase_document(include_receipts=True):
                document_type = 'purchase'
            else:
                document_type = 'other'
            if line.product_id.product_tmpl_id.categ_id.complete_name != 'Payment':
                line.price_unit = line.product_id._get_tax_included_unit_price(
                    line.move_id.company_id,
                    line.move_id.currency_id,
                    line.move_id.date,
                    document_type,
                    fiscal_position=line.move_id.fiscal_position_id,
                    product_uom=line.product_uom_id,
                )
    
    @api.depends('product_id')
    def _compute_name(self):
        for line in self:
            if line.display_type == 'payment_term':
                if line.move_id.payment_reference:
                    line.name = line.move_id.payment_reference
                elif not line.name:
                    line.name = ''
                continue
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue
            if line.partner_id.lang:
                product = line.product_id.with_context(lang=line.partner_id.lang)
            else:
                product = line.product_id

            values = []
            if product.partner_ref:
                values.append(product.partner_ref)
            if line.journal_id.type == 'sale':
                if product.description_sale:
                    values.append(product.description_sale)
            elif line.journal_id.type == 'purchase':
                if product.description_purchase:
                    values.append(product.description_purchase)
            
            if line.product_id.product_tmpl_id.categ_id.complete_name == 'Payment' and line.name:
                colon_index = line.name.find(':') or 0
                result = line.name[colon_index:]
                line.name = '\n'.join(values) + result
            else:
                line.name = '\n'.join(values)
                            

    def write(self, vals):
        res = super(CrmAccountMoveLine, self).write(vals)
        if 'product_id' in vals and self.order_lines:
            self.order_lines.product_id = vals['product_id']
            self.order_lines.name = self.name
            
        if 'name' in vals and self.order_lines:
            self.order_lines.name = self.name
            
        return res
    
    