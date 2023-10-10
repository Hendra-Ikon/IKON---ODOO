from odoo import models, api

class CrmTeam(models.Model):
    _inherit = "crm.team"
    
    @api.model
    def _uninstall_hook_team(self):
        team1 = self.env.ref("sales_team.team_sales_department")
        team2 = self.env.ref("sales_team.crm_team_1")
        
        if team1:
            team1.name = 'Sales'
            
        if team2:
            team2.name = 'Pre-Sales'
    