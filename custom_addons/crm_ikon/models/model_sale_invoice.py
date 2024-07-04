from odoo import models, fields, _, api
from odoo.fields import Command

import logging

logger = logging.getLogger(__name__)


class CrmSaleInvoice(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    advance_payment_method = fields.Selection(
        selection=[
            ('delivered', "Regular invoice"),
            ('percentage', "Term payment (percentage)"),
            ('fixed', "Term payment (fixed amount)"),
            ('monthly', "Monthly Payment Plan"),
        ],
        string="Create Invoice",
        default='delivered',
        required=True,
        help="A standard invoice is issued with all the order lines ready for invoicing,"
             "according to their invoicing policy (based on ordered or delivered quantity).")
    amount = fields.Float(
        string="Term Payment Amount",
        help="The percentage of amount to be invoiced in advance, taxes excluded.")
    fixed_amount = fields.Monetary(
        string="Term Payment Amount (Fixed)",
        help="The fixed amount to be invoiced in advance, taxes excluded.")
    monthly_payment_duration = fields.Selection(
        selection=[
            ('1', "1 Month"),
            ('2', "2 Month"),
            ('3', "3 Months"),
            ('4', "4 Months"),
            ('5', "5 Months"),
            ('6', "6 Months"),
            ('7', "7 Months"),
            ('8', "8 Months"),
            ('9', "9 Months"),
            ('10', "10 Months"),
            ('11', "11 Months"),
            ('12', "12 Months"),
        ],
        string="Monthly Payment Duration",
        help="Select the duration for the monthly payment plan.")
    advance_plan_payment_method = fields.Selection(
        selection=[
            ('percentage', "Term payment (percentage)"),
            ('fixed', "Term payment (fixed amount)"),
            ('monthly', "Monthly Payment Plan"),
        ])
    
    def _prepare_down_payment_product_values(self):
        self.ensure_one()
        return {
            'name': _('Term Payment'),
            'type': 'service',
            'invoice_policy': 'order',
            'company_id': False,
            'property_account_income_id': self.deposit_account_id.id,
            'categ_id': 1,
            'taxes_id': [Command.set(self.deposit_taxes_id.ids)],
        }
    

    # def _get_down_payment_description(self, order):
    #     self.ensure_one()
    #     context = {'lang': order.partner_id.lang}
    #     if self.advance_payment_method == 'percentage':
    #         name = _("Term payment: %s%% of payment", self.amount)
    #     elif self.advance_payment_method == 'fixed':
    #         name = _(f'Term payment: {self.fixed_amount} fixed amount')
    #     elif self.advance_payment_method == 'monthly':
    #         name = _("Monthly Payment Plan")
    #         if self.monthly_payment_duration:
    #             name += f" ({self.monthly_payment_duration} Months)"
    #     else:
    #         name = _("Regular Invoice")
    #     del context
    #
    #     return name

    def _get_down_payment_description(self, order, month):
        self.ensure_one()
        context = {'lang': order.partner_id.lang}
 
        if self.advance_payment_method == 'percentage':
            name = _("Down payment of %s%% - Month %s", self.amount, month)
        elif self.advance_payment_method == 'fixed':
            name = _('Down Payment - Month %s', month)
        elif self.advance_payment_method == 'monthly':
            name = _("Monthly Installment - Month %s", month)
        else:
            name = _('Down Payment')
            

        del context
        return name

    @api.onchange('advance_plan_payment_method')
    def _depend_payment(self):
        for line in self:
            if line.advance_plan_payment_method:
                line.advance_payment_method = line.advance_plan_payment_method
            if line.advance_plan_payment_method == 'monthly' and line.monthly_payment_duration:
                total_amount = line.sale_order_id.amount_total
                monthly_amount = total_amount / int(line.monthly_payment_duration)
                line.amount = monthly_amount
                line.fixed_amount = 0


    def _get_down_payment_amount(self, order):
        self.ensure_one()
        if self.advance_payment_method == 'percentage':
            advance_product_taxes = self.product_id.taxes_id.filtered(lambda tax: tax.company_id == order.company_id)
            if all(order.fiscal_position_id.map_tax(advance_product_taxes).mapped('price_include')):
                amount = order.amount_total * self.amount / 100
            else:
                amount = order.amount_untaxed * self.amount / 100
        elif self.advance_payment_method == 'fixed':
            amount = self.fixed_amount

        elif self.advance_payment_method == 'monthly':
            amount = order.amount_untaxed / int(self.monthly_payment_duration)
            return amount
        else:
            amount = 0.0
        return amount
    def _prepare_down_payment_section_values1(self, order, monthly):
        context = {'lang': order.partner_id.lang}
        so_values = {
            'name': 'Term Payments',
                    'quantity': 1.0,
                    'price_unit': 0,
                    'display_type': 'line_section',
        }

        del context
        return so_values

    def _prepare_invoice_values(self, order, so_line, month):
        self.ensure_one()
        if self.advance_payment_method == 'monthly':
            invoice_line_ids = []
            amount_per_month = self._get_down_payment_amount(order)
            line_data = self.env['sale.order.line'].search([('order_id','=', order.id)])
            
            for lines in line_data:
                
            # Check if the name contains 'Term Payments'
                if ('Monthly Payment' not in lines.name) and ('Term Payments' not in lines.name):
                    
                    invoice_line_ids.append(
                        Command.create(
                            
                            so_line._prepare_invoice_line(
                                product_id= lines.product_id.id,
                                name=lines.name,
                                quantity=1.0,
                                price_unit=amount_per_month,
                                tax_ids=lines.tax_id,
                         
                            )
                            
                        ),
                       
                    )
                    invoice_line_ids.append(Command.create(self._prepare_move_line_values(order, month)))
            logger.info("invoice_line_ids", invoice_line_ids) 
            return {
            **order._prepare_invoice(),
            'invoice_line_ids': invoice_line_ids,
        }
        else:
            return {
            **order._prepare_invoice(),
            'invoice_line_ids': [
                Command.create(
                    so_line._prepare_invoice_line(
                        name=self._get_down_payment_description(order),
                        quantity=1.0,
                        is_downpayment=False,
                    )
                )
            ],
        }
            
    # def _prepare_invoice_values(self, order, so_line, month):
    #     self.ensure_one()
    #     return {
    #         **order._prepare_invoice(),
    #         'invoice_line_ids': [
    #             Command.create(
    #                 so_line._prepare_invoice_line(
    #                     name=self._get_down_payment_description(order,month),
    #                     quantity=1.0,
    #                 )
    #             )
    #         ],
    #     }



    # def _prepare_invoice_values(self, order, so_line, month):
    #     self.ensure_one()
    #     invoice_values = order._prepare_invoice()
    
    #     # Remove original invoice line and add new lines based on the monthly payment plan
    #     # invoice_values['invoice_line_ids'] = [
    #     #     Command.unlink([line.id]) for line in invoice_values.get('invoice_line_ids', [])
    #     # ]
    
    #     for month in range(1, int(self.monthly_payment_duration) + 1):
    #         invoice_line_values = {
    #             'name': self._get_down_payment_description(order, month),
    #             'quantity': 1.0,
    #             'price_unit': self._get_down_payment_amount(order) / int(self.monthly_payment_duration),
    #             'product_id': self.product_id.id,
    #         }
    #         invoice_line_values.update(so_line._prepare_invoice_line(**invoice_line_values))
    #         invoice_values['invoice_line_ids'].append(Command.create(invoice_line_values))
    
    #     return invoice_values

# from odoo import models, fields, _, api
# from odoo.fields import Command
#
# import logging
#
# logger = logging.getLogger(__name__)
#
#
# class CrmSaleInvoice(models.TransientModel):
#     _inherit = "sale.advance.payment.inv"
#
#     advance_payment_method = fields.Selection(
#         selection=[
#             ('delivered', "Regular invoice"),
#             ('percentage', "Term payment (percentage)"),
#             ('fixed', "Term payment (fixed amount)"),
#             ('monthly', "Monthly Payment Plan"),
#         ],
#         string="Create Invoice",
#         default='delivered',
#         required=True,
#         help="A standard invoice is issued with all the order lines ready for invoicing,"
#              "according to their invoicing policy (based on ordered or delivered quantity).")
#     amount = fields.Float(
#         string="Term Payment Amount",
#         help="The percentage of amount to be invoiced in advance, taxes excluded.")
#     fixed_amount = fields.Monetary(
#         string="Term Payment Amount (Fixed)",
#         help="The fixed amount to be invoiced in advance, taxes excluded.")
#     advance_plan_payment_method = fields.Selection(
#         selection=[
#             ('percentage', "Term payment (percentage)"),
#             ('fixed', "Term payment (fixed amount)"),
#             ('monthly', "Monthly Payment Plan"),
#         ])
#
#     def _prepare_down_payment_product_values(self):
#         self.ensure_one()
#         return {
#             'name': _('Term Payment'),
#             'type': 'service',
#             'invoice_policy': 'order',
#             'company_id': False,
#             'property_account_income_id': self.deposit_account_id.id,
#             'categ_id': 1,
#             'taxes_id': [Command.set(self.deposit_taxes_id.ids)],
#         }
#
    # def _get_down_payment_description(self, order):
    #     self.ensure_one()
    #     context = {'lang': order.partner_id.lang}
    #     if self.advance_payment_method == 'percentage':
    #         name = _("Term payment: %s%% of payment", self.amount)
    #     elif self.advance_payment_method == 'fixed':
    #         name = _(f'Term payment: {self.fixed_amount} fixed amount')
    #     elif self.advance_payment_method == 'monthly':
    #         name = _("Monthly Payment Plan")
    #     else:
    #         name = _("Regular Invoice")
    #     del context

    #     return name
#
#     @api.onchange('advance_plan_payment_method')
#     def _depend_payment(self):
#         for line in self:
#             if line.advance_plan_payment_method:
#                 line.advance_payment_method = line.advance_plan_payment_method

# from odoo import models, fields, _, api
# from odoo.fields import Command
#
# import logging
#
# logger = logging.getLogger(__name__)
#
#
# class CrmSaleInvoice(models.TransientModel):
#     _inherit = "sale.advance.payment.inv"
#
#     advance_payment_method = fields.Selection(
#         selection=[
#             ('delivered', "Regular invoice"),
#             ('percentage', "Term payment (percentage)"),
#             ('fixed', "Term payment (fixed amount)"),
#         ],
#         string="Create Invoice",
#         default='delivered',
#         required=True,
#         help="A standard invoice is issued with all the order lines ready for invoicing,"
#             "according to their invoicing policy (based on ordered or delivered quantity).")
#     amount = fields.Float(
#         string="Term Payment Amount",
#         help="The percentage of amount to be invoiced in advance, taxes excluded.")
#     fixed_amount = fields.Monetary(
#         string="Term Payment Amount (Fixed)",
#         help="The fixed amount to be invoiced in advance, taxes excluded.")
#     advance_plan_payment_method = fields.Selection(
#         selection=[
#             ('percentage', "Term payment (percentage)"),
#             ('fixed', "Term payment (fixed amount)"),
#         ])
#
#     def _prepare_down_payment_product_values(self):
#         self.ensure_one()
#         return {
#             'name': _('Term Payment'),
#             'type': 'service',
#             'invoice_policy': 'order',
#             'company_id': False,
#             'property_account_income_id': self.deposit_account_id.id,
#             'categ_id': 1,
#             'taxes_id': [Command.set(self.deposit_taxes_id.ids)],
#         }
#
#     def _get_down_payment_description(self, order):
#         self.ensure_one()
#         context = {'lang': order.partner_id.lang}
#         if self.advance_payment_method == 'percentage':
#             name = _("Term payment: %s%% of payment", self.amount)
#         else:
#             name = _(f'Term payment: {self.fixed_amount} fixed amount')
#         del context
#
#         return name
#
#     @api.onchange('advance_plan_payment_method')
#     def _depend_payment(self):
#         for line in self:
#             if line.advance_plan_payment_method:
#                 line.advance_payment_method = line.advance_plan_payment_method
