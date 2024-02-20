from odoo import models, fields, api, _ , exceptions
import logging
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Command
logger = logging.getLogger(__name__)
from itertools import groupby
from datetime import datetime
import re

YEARS = datetime.now().year
MONTH_SELECTION = [
    ('01', f'January'),
    ('02', f'February'),
    ('03', f'March'),
    ('04', f'April'),
    ('05', f'May'),
    ('06', f'June'),
    ('07', f'July'),
    ('08', f'August'),
    ('09', f'September'),
    ('10', f'October'),
    ('11', f'November'),
    ('12', f'December'),
]

YEAR_SELECTION = [(str(y), str(y)) for y in range(YEARS - 10, YEARS + 4)]

    
class CrmSaleOrder(models.Model):
    _inherit = "sale.order"
    
    
    attention = fields.Char(string="Attention")
    project_name = fields.Char(string="Project Name", required=True)

    po_no = fields.Char(string="PO No.")
    po_date = fields.Date(string="PO. Date")
    payment_for = fields.Char(string="Payment For")
    payment_for_service = fields.Char(string="Payment For Service")
    spv = fields.Many2one('res.partner', string='Signature',required=False, domain="[('is_company','=',False)]")
    agreement_no = fields.Char(string="Agreement No")
    spk_no = fields.Char(string="SPK No")
    month = fields.Selection(MONTH_SELECTION, string="Month")
    name = fields.Char(
        string="Order Reference",
        required=True, copy=False, readonly=True,
        index='trigram',
        states={'draft': [('readonly', False)],'sale': [('readonly', False)]},
        default=lambda self: _('New'))
    period_start = fields.Date(string="Period Start")
    period_end = fields.Date(string='Period End')
    year = fields.Selection(YEAR_SELECTION, string='Year', default=str(YEARS))

    # @api.onchange('id')
    # def get_period_selection(self):
    #     if self.product_id:
    #         return

    #     logger.info("order_id", self.id)
    #     # logger.info("order_id", id)
    #     record_id = self.env.context.get('#id')
    #     logger.info("record_id", record_id)


    #     periods = self.env['model.period'].search([('sale_order_id', '=', 35)])
    #     period_selection = []
    #     for period in periods:
    #         period_label = f"{period.period_start}-{period.period_end}"
    #         period_selection.append((period_label, period_label))
    #     return period_selection
    
    
    @api.constrains('name')
    def _check_duplicate_name(self):
        for record in self:
            if record.name:
                duplicate_exists = self.env['sale.order'].search_count([('name', '=', record.name)])
                if duplicate_exists > 1:
                    raise exceptions.ValidationError("Quotation number must be unique. This invoice number already exists.")


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])
            if vals.get('name', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['date_order'])
                ) if 'date_order' in vals else None
                value = CrmSaleOrder.generate_default_name(self)
                vals['name'] = value or _("New")

        return super().create(vals_list)
    def generate_default_name(self):
        # Get the sale.order.sequence
        sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'sale.order')], limit=1)
        # logger.info("new_name",new_name) 
        # Ensure the sequence exists
        if sequence:
            # Get the next value from the sequence
            sequence_value = sequence.next_by_id()

            # Extract the last three digits
            last_three_digits = sequence_value[-3:]

            # Check if the last three digits are 999
            if last_three_digits == '999':
                # Extract the last four digits
                last_four_digits = sequence_value[-4:]
                name = f"{last_four_digits}/EXT-QUOT/{current_month}/{current_year}"
            else:
                # Get the current month and year
                current_month = fields.Date.today().month
                current_year = fields.Date.today().year

                # Format the name
                name = f"{last_three_digits}/EXT-QUOT/{current_month}/{current_year}"

            return name

        return False
        
    # def generate_default_name(self):
    #     # Get the sale.order.sequence
    #     sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'sale.order')], limit=1)

    #     seq = self.env['setting.seq.custom'].sudo().search([('ref', '=', 'Quo')])

    #     if seq:
    #         formatted_data_str = seq.format_quo

    #         matches = re.findall(r"(@[A-Z]+): '([^']+)'", formatted_data_str)

    #         result_array = []

    #         for match in matches:
    #             key, value = match

    #             if key == '@SEQ':
    #                 sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'sale.order')],limit=1)
    #                 if sequence:
    #                     value = sequence.next_by_id()[-3:]
    #             elif key == '@MONTH':
    #                 value = fields.Date.today().month
    #             elif key == '@YEAR':
    #                 value = fields.Date.today().year

    #             result_array.append({'key': key, 'value': value})
    #         name = ''

    #         for item in result_array:
    #             key = item['key']
    #             value = item['value']

    #             if key == '@SEQ':
    #                 # Tambahkan nilai dari @SEQ
    #                 name += f"{value}/"
    #             else:
    #                 # Tambahkan nilai dari key dan value
    #                 name += f"{value}/"

    #         # Hapus trailing '/' jika ada
    #         name = name.rstrip('/')

    #         return name

    #     return False
    
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
    
    def _prepare_confirmation_values(self):
        """ Prepare the sales order confirmation values.

        Note: self can contain multiple records.

        :return: Sales Order confirmation values
        :rtype: dict
        """
        # logger.info(self.info)
        return {
            'state': 'sale',
            'date_order': fields.Datetime.now()
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
    
    def _create_invoices(self, grouped=False, final=False, date=None):
        """ Create invoice(s) for the given Sales Order(s).

        :param bool grouped: if True, invoices are grouped by SO id.
            If False, invoices are grouped by keys returned by :meth:`_get_invoice_grouping_keys`
        :param bool final: if True, refunds will be generated if necessary
        :param date: unused parameter
        :returns: created invoices
        :rtype: `account.move` recordset
        :raises: UserError if one of the orders has no invoiceable lines.
        """
        if not self.env['account.move'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        # 1) Create invoices.
        invoice_vals_list = []
        invoice_item_sequence = 0 # Incremental sequencing to keep the lines order on the invoice.
        for order in self:
            order = order.with_company(order.company_id).with_context(lang=order.partner_invoice_id.lang)

            invoice_vals = order._prepare_invoice()
            invoiceable_lines = order._get_invoiceable_lines(final)

            if not any(not line.display_type for line in invoiceable_lines):
                continue

            invoice_line_vals = []
            down_payment_section_added = False
            for line in invoiceable_lines:
                if not down_payment_section_added and line.is_downpayment:
                    # Create a dedicated section for the down payments
                    # (put at the end of the invoiceable_lines)
                    invoice_line_vals.append(
                        Command.create(
                            order._prepare_down_payment_section_line(sequence=invoice_item_sequence)
                        ),
                    )
                    down_payment_section_added = True
                    invoice_item_sequence += 1
                invoice_line_vals.append(
                    Command.create(
                        line._prepare_invoice_line(sequence=invoice_item_sequence)
                    ),
                )
                invoice_item_sequence += 1
            logger.info("invoice_line_vals",invoice_line_vals)

            invoice_vals['invoice_line_ids'] += invoice_line_vals
            invoice_vals_list.append(invoice_vals)
        

        if not invoice_vals_list and self._context.get('raise_if_nothing_to_invoice', True):
            raise UserError(self._nothing_to_invoice_error_message())

        # 2) Manage 'grouped' parameter: group by (partner_id, currency_id).
        if not grouped:
            new_invoice_vals_list = []
            invoice_grouping_keys = self._get_invoice_grouping_keys()
            invoice_vals_list = sorted(
                invoice_vals_list,
                key=lambda x: [
                    x.get(grouping_key) for grouping_key in invoice_grouping_keys
                ]
            )
            for _grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: [x.get(grouping_key) for grouping_key in invoice_grouping_keys]):
                origins = set()
                payment_refs = set()
                refs = set()
                ref_invoice_vals = None
                for invoice_vals in invoices:
                    if not ref_invoice_vals:
                        ref_invoice_vals = invoice_vals
                    else:
                        ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                    origins.add(invoice_vals['invoice_origin'])
                    payment_refs.add(invoice_vals['payment_reference'])
                    refs.add(invoice_vals['ref'])
                ref_invoice_vals.update({
                    'ref': ', '.join(refs)[:2000],
                    'invoice_origin': ', '.join(origins),
                    'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
                })
                new_invoice_vals_list.append(ref_invoice_vals)
            invoice_vals_list = new_invoice_vals_list

        # 3) Create invoices.

        # As part of the invoice creation, we make sure the sequence of multiple SO do not interfere
        # in a single invoice. Example:
        # SO 1:
        # - Section A (sequence: 10)
        # - Product A (sequence: 11)
        # SO 2:
        # - Section B (sequence: 10)
        # - Product B (sequence: 11)
        #
        # If SO 1 & 2 are grouped in the same invoice, the result will be:
        # - Section A (sequence: 10)
        # - Section B (sequence: 10)
        # - Product A (sequence: 11)
        # - Product B (sequence: 11)
        #
        # Resequencing should be safe, however we resequence only if there are less invoices than
        # orders, meaning a grouping might have been done. This could also mean that only a part
        # of the selected SO are invoiceable, but resequencing in this case shouldn't be an issue.
        if len(invoice_vals_list) < len(self):
            SaleOrderLine = self.env['sale.order.line']
            for invoice in invoice_vals_list:
                sequence = 1
                for line in invoice['invoice_line_ids']:
                    line[2]['sequence'] = SaleOrderLine._get_invoice_line_sequence(new=sequence, old=line[2]['sequence'])
                    sequence += 1

        # Manage the creation of invoices in sudo because a salesperson must be able to generate an invoice from a
        # sale order without "billing" access rights. However, he should not be able to create an invoice from scratch.
        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)

        # 4) Some moves might actually be refunds: convert them if the total amount is negative
        # We do this after the moves have been created since we need taxes, etc. to know if the total
        # is actually negative or not
        if final:
            moves.sudo().filtered(lambda m: m.amount_total < 0).action_switch_invoice_into_refund_credit_note()
        for move in moves:
            move.message_post_with_view(
                'mail.message_origin_link',
                values={'self': move, 'origin': move.line_ids.sale_line_ids.order_id},
                subtype_id=self.env['ir.model.data']._xmlid_to_res_id('mail.mt_note'))
        return moves
    
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()

        return {
            'ref': self.client_order_ref or '',
            'move_type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id._get_fiscal_position(self.partner_invoice_id)).id,
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_user_id': self.user_id.id,
            'payment_reference': self.name,
            'transaction_ids': [Command.set(self.transaction_ids.ids)],
            'company_id': self.company_id.id,
            'invoice_line_ids': [],
            'user_id': self.user_id.id,
            'project_name': self.project_name,
            'po_no': self.po_no,
            'po_date': self.po_date,
            'payment_for': self.payment_for,
            'payment_for_service': self.payment_for_service,
            'spv': self.spv.id,
            'spk_no': self.spk_no,
            'month': self.month,
            'year': self.year,
            'attention': self.attention,
            'period_start': self.period_start,
            'period_end': self.period_end,
            'agreement_no': self.agreement_no,

        }



 
        




   

