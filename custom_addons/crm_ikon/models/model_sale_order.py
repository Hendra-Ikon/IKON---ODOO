from odoo import models, fields, api
import logging
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Command
logger = logging.getLogger(__name__)
from itertools import groupby



class CrmSaleOrder(models.Model):
    _inherit = "sale.order"
    
    attention = fields.Char(string="Attention")
    project_name = fields.Char(string="Project Name")

    po_no = fields.Char(string="PO No.")
    po_date = fields.Date(string="PO. Date")
    payment_for = fields.Char(string="Payment For")
    period = fields.Date(string="Period")
    payment_for_service = fields.Char(string="Payment For Service")
    spv = fields.Many2one('res.partner', string='SPV', domain="[('is_company','=',True)]")
    agreement_no = fields.Char(string="Agreement No")
    spk_no = fields.Char(string="SPK No")

    month = fields.Date(string="Month")
    

    name = fields.Text(
        string="Description",
        compute='_compute_name',
        tracking=True,
        store=True, readonly=False, required=True, precompute=True)
    
    def _get_mail_template(self):
        """
        :return: the correct mail template based on the current move type
        """
        return (
           'account.email_template_edi_invoice'
        )
    def action_quotation_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()
        self.order_line._validate_analytic_distribution()
        lang = self.env.context.get('lang')
        mail_template = self._find_mail_template()
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        
        # template = self.env.ref(self._get_mail_template(), raise_if_not_found=False)
        
       
        # ctx = dict(
        #     default_model='account.move',
        #     default_res_id=self.id,
        #     # For the sake of consistency we need a default_res_model if
        #     # default_res_id is set. Not renaming default_model as it can
        #     # create many side-effects.
        #     default_res_model='account.move',
        #     default_use_template=bool(template),
        #     default_template_id=template and template.id or False,
        #     default_composition_mode='comment',
        #     mark_invoice_as_sent=True,
        #     default_email_layout_xmlid="mail.mail_notification_layout_with_responsible_signature",
        #     model_description=self.with_context(lang=lang).type_name,
        #     force_email=True,
        #     active_ids=self.ids,
        # )
        logger.info("test",mail_template.id)
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.id,
            'default_use_template': bool(mail_template),
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        # ctx = {}
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
        


    def _get_order_lines_to_report_payment(self):
        down_payment_lines = self.order_line.filtered(lambda line:
            line.is_downpayment
            and not line.display_type
        )
        
        def show_line(line):
            if line in down_payment_lines:
                return True
            else:
                return False
        
        return self.order_line.filtered(show_line)


 
        




   



    
