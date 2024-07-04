from odoo import models, api
import logging

logger = logging.getLogger(__name__)

class CrmGroups(models.Model):
    _inherit = "res.groups"
    
    @api.model
    def _post_hook_groups(self):
        groups = [self.env.ref('product.group_product_variant'), self.env.ref('product.group_product_pricelist'), 
                  self.env.ref('sales_team.group_sale_manager')] 
        for group in groups:
            menu_filter = group.menu_access.filtered(lambda x: x.name != 'Product Variants' and x.name != 'Pricelists' and x.name != 'Sales Teams')
            group.menu_access = menu_filter
    
    @api.model
    def _uninstall_hook_groups(self):
        add_menu = [self.env.ref('sale.menu_products'), self.env.ref('sale.menu_product_pricelist_main'), 
                    self.env.ref('sale.report_sales_team')]
        groups = [self.env.ref('product.group_product_variant'), self.env.ref('product.group_product_pricelist'), 
                  self.env.ref('sales_team.group_sale_manager')] 
        for group in groups:
            all_menu = self.env['ir.ui.menu'].browse([x.id for x in group.menu_access] + [x.id for x in add_menu])
            group.menu_access = all_menu
        