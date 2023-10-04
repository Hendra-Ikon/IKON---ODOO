from odoo import models, api

class CrmMenu(models.Model):
    _inherit = "ir.ui.menu"
    
    @api.model
    def _uninstall_hook_menuitem(self):
        menu = self.env.ref('sale.product_menu_catalog')
        menu2 = self.env.ref('sale.menu_product_template_action')
        menu.name = 'Product'
        menu2.name = 'Product'
    