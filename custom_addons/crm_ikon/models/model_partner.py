from odoo import models, fields, api
import json
import logging
from odoo.exceptions import ValidationError

logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError

class CrmPartner(models.Model):
    _inherit = "res.partner"
    
    linkedin_url = fields.Char(string="LinkedIn")
    headline = fields.Char(string="Headline")
    
    # layout_id = fields.Many2one(comodel_name='base.document.layout',string="Layout",help="Account used for deposits")
    document_layout_ids = fields.Many2many('base.document.layout', string='Document Layouts')
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

    
    # def action_view_layout(self):
    #     print(self)
  
    def action_open_base_document_layout(self, action_ref=None):
        context = self._context
        company_id = context.get('default_company_id', False)
        logger.info("company_id",company_id)
        if not action_ref:
            logger.info("tests",self)
            action_ref = 'web.action_base_document_layout_configurator'
        res = self.env["ir.actions.actions"]._for_xml_id(action_ref)
        self.env[res["res_model"]].check_access_rights('write')
        return res
    
    def action_view_layout(self, docids=None, data=None, config=True):
        """Return an action of type ir.actions.report.

        :param docids: id/ids/browse record of the records to print (if not used, pass an empty list)
        :param data:
        :param bool config:
        :rtype: bytes
        """
        context = self.env.context
        if docids:
            if isinstance(docids, models.Model):
                active_ids = docids.ids
            elif isinstance(docids, int):
                active_ids = [docids]
            elif isinstance(docids, list):
                active_ids = docids
            context = dict(self.env.context, active_ids=active_ids)
        report_actions = self.env['ir.actions.report']
        report_action = {
            'context': context,
            'data': data,
            'type': 'ir.actions.report',
            'report_name': report_actions.report_name,
            'report_type': report_actions.report_type,
            'report_file': report_actions.report_file,
            'name': report_actions.name,
        }

        discard_logo_check = self.env.context.get('discard_logo_check')
        if self.env.is_admin() and not self.env.company.external_report_layout_id and config and not discard_logo_check:
            return self._action_configure_external_report_layout(report_action)

        return report_action

    def _action_configure_external_report_layout(self, report_action):
        action = self.env["ir.actions.actions"]._for_xml_id("web.action_base_document_layout_configurator")
        py_ctx = json.loads(action.get('context', {}))
        report_action['close_on_report_download'] = True
        py_ctx['report_action'] = report_action
        action['context'] = py_ctx
        return action


    @api.constrains('email')
    def _check_duplicate_email(self):
        for partner in self:
            if partner.email:
                domain = [('id', '!=', partner.id), ('email', '=', partner.email)]
                if self.search_count(domain) > 0:
                    raise ValidationError("A contact with this email already exists.")
            else:
                raise ValidationError("Email cannot be empty.")


# class CustomeResPertner(models.TransientModel):

#     _inherit = 'res.partner'

#     layout_id = fields.Many2one(comodel_name='base.document.layout',string="Layout",help="Account used for deposits")

