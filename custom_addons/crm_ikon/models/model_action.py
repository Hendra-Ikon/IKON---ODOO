from odoo import models, api
import logging

logger = logging.getLogger(__name__)

class CrmAction(models.Model):
    _inherit = "ir.actions.actions"
    
    @api.model
    def _uninstall_hook_action_name(self):
        action = self.env.ref("sale.product_template_action")
        action.name = 'Products'