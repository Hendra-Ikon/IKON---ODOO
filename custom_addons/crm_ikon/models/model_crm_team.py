from odoo import models, api, fields
import ast
import logging

logger = logging.getLogger(__name__)

class CrmTeam(models.Model):
    _inherit = "crm.team"
    
    opportunities_total = fields.Char(string="Opportunities Ammount", compute="_compute_opportunity_total", store=True)
    quotations_total = fields.Char(string="Quotations Ammount", compute="_compute_quotations_total", store=True)
    
    @api.model
    def _uninstall_hook_team(self):
        team1 = self.env.ref("sales_team.team_sales_department")
        team2 = self.env.ref("sales_team.crm_team_1")
        
        if team1:
            team1.name = 'Sales'
            
        if team2:
            team2.name = 'Pre-Sales'
            
    def _compute_opportunity_total(self):
        opportunity_data = self.env['crm.lead']._read_group([
            ('team_id', 'in', self.ids),
            ('probability', '<', 100),
            ('type', '=', 'opportunity'),
        ], ['expected_revenue:sum', 'team_id'], ['team_id'])
        amounts = {datum['team_id'][0]: datum['expected_revenue'] for datum in opportunity_data}
        for team in self:
            amount = amounts.get(team.id, 0)
            if amount >= 100000000.0:
                team.opportunities_total = str(round(amount / 1000000,2)) + "M"
            elif amount >= 1000000000.0:
                team.opportunities_total = str(round(amount / 1000000000,2)) + "B"
            else: 
                team.opportunities_total = str(amount)
    
    def _compute_quotations_total(self):
        query = self.env['sale.order']._where_calc([
            ('team_id', 'in', self.ids),
            ('state', 'in', ['draft', 'sent']),
        ])
        self.env['sale.order']._apply_ir_rules(query, 'read')
        _, where_clause, where_clause_args = query.get_sql()
        select_query = """
            SELECT team_id, count(*), sum(amount_total /
                CASE COALESCE(currency_rate, 0)
                WHEN 0 THEN 1.0
                ELSE currency_rate
                END
            ) as amount_total
            FROM sale_order
            WHERE %s
            GROUP BY team_id
        """ % where_clause
        self.env.cr.execute(select_query, where_clause_args)
        quotation_data = self.env.cr.dictfetchall()
        for datum in quotation_data:
            team = self.browse(datum['team_id'])
            amount = datum['amount_total']
            if amount >= 100000000.0:
                team.quotations_total = str(round(amount / 1000000,2)) + "M"
            elif amount >= 1000000000.0:
                team.quotations_total = str(round(amount / 1000000000,2)) + "B"
            else: 
                team.quotations_total = str(amount)
    
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

    