
from odoo import api, fields, models, _
from odoo.addons.mail.wizard.mail_compose_message import _reopen
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang
import logging

logger = logging.getLogger(__name__)

class CustomAccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'

    def _print_document(self):
        logger.info("test print")

        
        """ to override for each type of models that will use this composer."""
        self.ensure_one()
        action = self.invoice_ids.action_invoice_print()
        action.update({'close_on_report_download': True})
        return action