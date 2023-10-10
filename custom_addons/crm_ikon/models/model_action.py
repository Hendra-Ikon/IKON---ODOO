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