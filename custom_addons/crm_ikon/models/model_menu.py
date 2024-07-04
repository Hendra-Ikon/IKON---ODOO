from odoo import models, api

class CrmMenu(models.Model):
    _inherit = "ir.ui.menu"
    
    @api.model
    def _uninstall_hook_menuitem(self):
        menu1 = self.env.ref('sale.product_menu_catalog')
        if menu1:
            menu1.name = 'Product'
                
        menu2 = self.env.ref('sale.menu_product_template_action')
        if menu2: 
            menu2.name = 'Product'
            
        menu3 = self.env.ref("crm.sales_team_menu_team_pipeline")
        if menu3:
            menu3.name = 'Teams'
            
        menu4 = self.env.ref("crm.crm_team_config")
        if menu4:
            menu4.name = 'Sales Teams'
            
        menu5 = self.env.ref("sale.sales_team_config")
        if menu5:
            menu5.name = 'Sales Teams'
            
        menu6 = self.env.ref("crm.crm_menu_root")
        if menu6:
            menu6.action = None
            
    @api.model
    def _install_hook_menuitem(self):
        menu1 = self.env.ref("sale.sales_team_config")
        if menu1:
            menu1.name = 'Categories'
        
    