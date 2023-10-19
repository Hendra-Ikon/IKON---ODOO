from odoo import models, api
import ast
import logging

loggger = logging.getLogger(__name__)

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
    
    def action_primary_channel_button(self):
        partner_id = self.env.context.get('partner_id')
        self.ensure_one()
        if self.use_opportunities:
            action = self.env['ir.actions.actions']._for_xml_id('crm.crm_case_form_view_salesteams_opportunity')
            if partner_id:
                partner = self.env['res.partner'].browse(partner_id)
                action = self.env['ir.actions.act_window']._for_xml_id('crm.crm_lead_opportunities')
                action['context'] = {
                    'active_test': False,
                    'search_default_team_id': self.id,
                    'default_team_id': self.id,
                    'default_partner_id': partner.id,
                    'default_stage_id': 1,
                    'default_type': 'opportunity'
                }
                if partner.is_company:
                    action['domain'] = [('partner_id.commercial_partner_id', '=', partner.id)]
                else:
                    action['domain'] = [('partner_id', '=', partner.id)]
                return action
            
            rcontext = {
                'team': self
            }
            action['help'] = self.env['ir.ui.view']._render_template('crm.crm_action_helper', values=rcontext)
            return action
        return super(CrmTeam,self).action_primary_channel_button()
    