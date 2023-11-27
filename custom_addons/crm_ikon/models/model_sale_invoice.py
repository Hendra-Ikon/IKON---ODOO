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
            ('3', "3 Months"),
            ('6', "6 Months"),
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

    def _get_down_payment_description(self, order):
        self.ensure_one()
        context = {'lang': order.partner_id.lang}
        if self.advance_payment_method == 'percentage':
            name = _("Term payment: %s%% of payment", self.amount)
        elif self.advance_payment_method == 'fixed':
            name = _(f'Term payment: {self.fixed_amount} fixed amount')
        elif self.advance_payment_method == 'monthly':
            name = _("Monthly Payment Plan")
            if self.monthly_payment_duration:
                name += f" ({self.monthly_payment_duration} Months)"
        else:
            name = _("Regular Invoice")
        del context

        return name

    @api.onchange('advance_plan_payment_method')
    def _depend_payment(self):
        for line in self:
            if line.advance_plan_payment_method:
                line.advance_payment_method = line.advance_plan_payment_method

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
#     def _get_down_payment_description(self, order):
#         self.ensure_one()
#         context = {'lang': order.partner_id.lang}
#         if self.advance_payment_method == 'percentage':
#             name = _("Term payment: %s%% of payment", self.amount)
#         elif self.advance_payment_method == 'fixed':
#             name = _(f'Term payment: {self.fixed_amount} fixed amount')
#         elif self.advance_payment_method == 'monthly':
#             name = _("Monthly Payment Plan")
#         else:
#             name = _("Regular Invoice")
#         del context
#
#         return name
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