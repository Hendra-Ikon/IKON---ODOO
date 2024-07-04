from odoo import models, api

class CrmStage(models.Model):
    _inherit = "crm.stage"
    
    @api.model
    def _uninstall_hook_stage(self):
        stage1 = self.env.ref("crm.stage_lead2")
        if stage1:
            stage1.name = 'Qualified' 
        
        stage2 = self.env.ref("crm.stage_lead3")
        if stage2:
            stage2.name = 'Proposition' 
        
        stage3 = self.env.ref("crm.stage_lead4")
        if stage3:
            stage3.name = 'Won' 
        
        