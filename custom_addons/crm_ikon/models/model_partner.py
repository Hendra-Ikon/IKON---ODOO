from odoo import models, fields

class CrmPartner(models.Model):
    _inherit = "res.partner"
    
    linkedin_url = fields.Char(string="LinkedIn")
    headline = fields.Char(string="Headline")
    
    def action_view_opportunity(self):
        '''
        This function returns an action that displays the opportunities from partner.
        '''
        # if self.opportunity_count > 0:
        #     action = self.env['ir.actions.act_window']._for_xml_id('crm.crm_lead_opportunities')
        #     action['context'] = {'active_test': False}
        #     if self.is_company:
        #         action['domain'] = [('partner_id.commercial_partner_id', '=', self.id)]
        #     else:
        #         action['domain'] = [('partner_id', '=', self.id)]
        #     return action
        
        action = self.env['ir.actions.act_window']._for_xml_id('sales_team.crm_team_action_pipeline')
        action['context'] = {
            'active_test': False,
            'self' : self.id
        }
        return action