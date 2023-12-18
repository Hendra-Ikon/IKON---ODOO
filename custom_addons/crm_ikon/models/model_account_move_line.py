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
    # period = fields.Selection([], string="Period", compute="_onchange_account_id")
    po_number = fields.Char(string="PO")
    # period = fields.One2many("model.period", "account_move_id", string="Periods")
    period = fields.Selection(selection=lambda self: self.env['account.move']._get_period_selection(), string="Period", help="Select the period for the account move line.")
    # period = fields.Selection(selection=lambda self: self._get_period_selection(), string="Period", help="Select the period for the account move line.")
    move_id = fields.Many2one(
        comodel_name='account.move',
        auto_join=True,
        string='Journal Entry', required=True, readonly=True, ondelete='cascade',
        check_company=True)
    

    # @api.depends('period','move_id')
    # def _get_period_selection(self):
        
    #     for data in self:
    #         logger.info("1", data.move_id.id)
    #     id = CrmAccountMoveLine._get_move_id(self)
    #     logger.info("id", id)
    #     logger.info("move", self)
    #     periods = self.env['model.period'].search([('account_move_id', '=', 187)])
    #     period_selection = []
    #     for period in periods:
    #         period_label = f"{period.period_start}-{period.period_end}"
    #         period_selection.append((period_label, period_label))
    #     return period_selection
    
    # # @api.onchange('product_id','move_id')
    # def _get_move_id(self):
    #     logger.info("self.move_id.id",self.move_id.id)
    #     # Ensure move_id is a NewId object
    #     if self.move_id and hasattr(self.move_id.id, 'origin'):
    #         origin_value = getattr(self.move_id.id, 'origin', None)
    #         if origin_value is not None:
    #             numeric_value = int(origin_value)
    #             logger.info("Numeric Value:", numeric_value)
    #             return numeric_value

    #     return {}
    


    # @api.onchange('move_id')
    # def _get_period_selection(self):
    #     """
    #     Returns a list of tuples representing the period selection options.

    #     Returns:
    #         list: A list of tuples with the format `(period_string,)`.
    #     """
    #     self.period = period_selections = []
    #     # Use the provided move_id in the domain
    #     periods = self.env['model.period'].search([('account_move_id', '=', self.move_id.id)])

    #     # Create a list of tuples for the selection field
        
    #     for period in periods:
    #         logger.info("period", period)
    #         period_string = f"{period.period_start} - {period.period_end}"
    #         period_selections.append((period_string,))

    #     return period_selections

    
    
    
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
    
    