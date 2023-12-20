from odoo import models, api
import logging

logger = logging.getLogger(__name__)

class CrmAction(models.Model):
    _inherit = "ir.actions.actions"
    
    @api.model
    def _uninstall_hook_action_name(self):
        action1 = self.env.ref("sale.product_template_action")
        if action1: 
            action1.name = 'Products'
        
        action2 = self.env.ref("sales_team.crm_team_action_pipeline")
        if action2:
            action2.name = 'Teams'
            
        action3 = self.env.ref("sales_team.crm_team_action_config")
        if action3:
            action3.name = 'Sales Teams'

# class AccountTaxCustom(models.Model):
#     _inherit = 'account.tax'

#     @api.model
#     def _convert_to_tax_base_line_dict(
#             self, base_line, monthly_rate=None,
#             partner=None, currency=None, product=None, taxes=None, price_unit=None, quantity=None,
#             discount=None, account=None, analytic_distribution=None, price_subtotal=None,
#             is_refund=False, rate=None,
#             handle_price_include=True,
#             extra_context=None,
#     ):
#         return {
#             'record': base_line,
#             'partner': partner or self.env['res.partner'],
#             'currency': currency or self.env['res.currency'],
#             'product': product or self.env['product.product'],
#             'taxes': taxes or self.env['account.tax'],
#             'price_unit': price_unit or 0.0,
#             'monthly_rate': monthly_rate or 0.0,
#             'quantity': quantity or 0.0,
#             'discount': discount or 0.0,
#             'account': account or self.env['account.account'],
#             'analytic_distribution': analytic_distribution,
#             'price_subtotal': price_subtotal or 0.0,
#             'is_refund': is_refund,
#             'rate': rate or 1.0,
#             'handle_price_include': handle_price_include,
#             'extra_context': extra_context or {},
#         }

