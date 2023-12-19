from odoo import models, _, fields, api, exceptions, http
from odoo.exceptions import UserError
from contextlib import contextmanager
from odoo.tools import formatLang, format_amount
from textwrap import shorten
import inflect
from collections import defaultdict
import logging
from odoo.tools import (
    date_utils,
    email_re,
    email_split,
    float_compare,
    float_is_zero,
    float_repr,
    format_amount,
    format_date,
    formatLang,
    frozendict,
    get_lang,
    is_html_empty,
    sql
)

logger = logging.getLogger(__name__)

# PAYMENT_STATE_SELECTION = [
#         ('not_paid', 'Not Paid'),
#         ('in_payment', 'In Payment'),
#         ('paid', 'Paid'),
#         ('partial', 'Partially Paid'),
#         ('reversed', 'Reversed'),
#         ('invoicing_legacy', 'Invoicing App Legacy'),
# ]
MONTH_SELECTION = [
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]
class CrmAccountMove(models.Model):
    _inherit = "account.move"

    month = fields.Selection(MONTH_SELECTION, string="Month")
    attention = fields.Char(string="Attention")
    inv_no = fields.Char(
        string='Invoice No.',
        store=True,
        copy=False,
        tracking=True,
        index='trigram',
        )
    in_word = fields.Char(string="In Word", compute="_compute_in_word", store=True)
    project_name = fields.Char(string="Project Name", required=True)
    po_no = fields.Char(string="PO No.")
    po_date = fields.Date(string="PO. Date")
    payment_for = fields.Char(string="Payment For")
    period = fields.Date(string="Period")
    # periods = fields.One2many("model.period", "account_move_id", string="Periods")
    # period = fields.Selection(selection=lambda self: self.env['account.move']._get_period_selection(), string="Period", help="Select the period for the account move line.")
    payment_for_service = fields.Char(string="Payment For Service")
    spv = fields.Many2one('res.partner', string='Signature', domain="[('is_company','=',False)]")
    agreement_no = fields.Char(string="Agreement No")
    spk_no = fields.Char(string="SPK No")
    month = fields.Selection(MONTH_SELECTION, string="Month")
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('approved', 'Approved'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default='draft',
    )
    amount_untaxed = fields.Monetary(
        string='Amount before Taxes',
        compute='_compute_amount', store=True, readonly=True,
        tracking=True,
    )
    amount_total = fields.Monetary(
        string='Amount After Taxes',
        compute='_compute_amount', store=True, readonly=True,
        inverse='_inverse_amount_total',
    )

    hide_post_button = fields.Boolean(compute='_compute_hide_post_button', readonly=True, default=True)

    payment_state = fields.Selection(
        selection=[
        ('not_paid', ''),
        ('in_payment', 'In Payment'),
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('reversed', 'Reversed'),
        ('invoicing_legacy', 'Invoicing App Legacy'),
],
        string="Payment Status",
        compute='_compute_payment_state', store=True, readonly=True,
        copy=False,
        tracking=True,
    )
    show_periods = fields.Boolean(string='Add Periods', default=False)
    
    # def add_period(self):
    #     account_move_id = self.id
    #     logger.info("account_move_id", account_move_id)
        
    #     return {
    #         'name': _('Add Period'),
    #         'view_mode': 'tree',
    #         'view_id': False,  # Set to False to allow Odoo to choose the best view
    #         'view_type': 'tree',
    #         'res_model': 'model.period',
    #         'type': 'ir.actions.act_window',
    #         'target': 'new',
    #         'context': {
    #             'search_default_account_move_id': account_move_id,
    #             'default_account_move_id': account_move_id,  # Pass account_move_id as default value
    #         },
    #     }

           

        # return True

    # def add_period(self):
    #     return {
    #         "name": "Periods",
    #         "type": "ir.actions.act_window",
    #         "res_model": "model.period",
    #         "view_mode": "tree",
    #         'view_type': 'tree',
    #         "view_id": False,  # Let Odoo choose the view automatically
    #         "domain": [("account_move_id", "=", self.id)],
    #         "context": {
    #             # Add any other context values you want to pass
    #         },
    #     }

    def _get_period_selection(self):
        request = http.request

        # Retrieve the 'id' parameter from the URL
        # id_param = request.params.get('id')
        active_ids = self.env.context.get("active_ids")
        if active_ids:
            logger.info("test",active_ids[0])
            data = self.env["sale.order"].browse(active_ids[0])

        # return self.env["account.move"]

        id_param = self._context.get('id')
        # tets = http.request.get('active_id')
        # to_param = kwargs.get( 'id' )
        # a = CrmAccountMove._get_move_id(self)
        # logger.info("id", a)
        # a = self.env.context.get('id') 
        # logger.info("tets", tets)
        logger.info("a", self.id)
     

        periods = self.env['model.period'].search([('account_move_id', '=', 187)])
        period_selection = []
        for period in periods:
            period_label = f"{period.period_start}-{period.period_end}"
            period_selection.append((period_label, period_label))
        return period_selection
    
    # @api.onchange('product_id','move_id')
    def _get_move_id(self):
        for data in self:

            logger.info("self.move_id.id",data.id)
        # # Ensure move_id is a NewId object
        # if self.move_id and hasattr(self.move_id.id, 'origin'):
        #     origin_value = getattr(self.move_id.id, 'origin', None)
        #     if origin_value is not None:
        #         numeric_value = int(origin_value)
        #         logger.info("Numeric Value:", numeric_value)
        #         return numeric_value

        return {}
    def add_period(self):
        return {
            "name": "Periods",
            "type": "ir.actions.act_window",
            "res_model": "model.period",
            "view_mode": "tree,form",
            "view_id": False,  # To let Odoo choose the most suitable view
            'domain': [('account_move_id', "=", self.id)],
            "context": {
                "default_account_move_id": self.id,  # Set default values for fields
                "form_view_ref": "crm_ikon.view_model_period_form",  # Use the correct XML ID
                "default_period_start": "2023-01-01",
                "default_period_end": "2023-01-31",
                "create": True,  # Set to False to hide the 'Create' button
                "edit": True,  # Set to True to show the 'Edit' button
            },
            "target": "save",  # Open the window in a modal dialog
        }
    # def action_add_period(self):
    #     """
    #     Opens a pop-up window to add a new period.
    #     """
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Add Period',
    #         'res_model': 'account.move',
    #          'view_id': self.env.ref('crm_ikon.view_period_form').id,
    #         'target': 'new',
    #         'view_type': 'form',
    #         'view_mode': 'form',
            
    #     }
    # def action_add_period(self):
    #     """
    #     Opens a pop-up window with a split view: form at the top, tree at the bottom.
    #     """
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': _('Add Period'),
    #         'res_model': 'account.move',
    #         'view_id' : self.env.ref('crm_ikon.view_period_form').id,
    #         'view_mode': 'form',
    #         'view_type': 'form',
            
    #         'target': 'new',
    #     }
    
    def action_add_period(self):
        # Your logic to open the popup goes here
        # This method is called when the button is clicked
        return {
            'name': _('Add Period'),
            'view_mode': 'form',
            'view_id': self.env.ref('crm_ikon.view_model_period_form').id,
            'view_type': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
   

        



    @api.constrains('inv_no')
    def _check_duplicate_inv_no(self):
        for record in self:
            if record.inv_no:
                duplicate_exists = self.env['account.move'].search_count([('inv_no', '=', record.inv_no)])
                if duplicate_exists > 1:
                    raise exceptions.ValidationError("Invoice number must be unique. This invoice number already exists.")

    @api.depends('amount_total')
    def _compute_in_word(self):
        p = inflect.engine()
        for record in self:
            if record.amount_total:
                amount_in_words = p.number_to_words(record.amount_total)
                amount_in_words = amount_in_words.replace(" and", "").replace(" point zero", " Rupiah")
                record.in_word = amount_in_words
  


    def action_approve(self):
        for move in self:
            if move.state == 'approved':
                move.write({'state': 'posted'})
            else:
                move.write({'state': 'approved'})

    @api.depends('amount_residual', 'move_type', 'state', 'company_id')
    def _compute_payment_state(self):
        stored_ids = tuple(self.ids)
        if stored_ids:
            self.env['account.partial.reconcile'].flush_model()
            self.env['account.payment'].flush_model(['is_matched'])

            queries = []
            for source_field, counterpart_field in (('debit', 'credit'), ('credit', 'debit')):
                queries.append(f'''
                        SELECT
                            source_line.id AS source_line_id,
                            source_line.move_id AS source_move_id,
                            account.account_type AS source_line_account_type,
                            ARRAY_AGG(counterpart_move.move_type) AS counterpart_move_types,
                            COALESCE(BOOL_AND(COALESCE(pay.is_matched, FALSE))
                                FILTER (WHERE counterpart_move.payment_id IS NOT NULL), TRUE) AS all_payments_matched,
                            BOOL_OR(COALESCE(BOOL(pay.id), FALSE)) as has_payment,
                            BOOL_OR(COALESCE(BOOL(counterpart_move.statement_line_id), FALSE)) as has_st_line
                        FROM account_partial_reconcile part
                        JOIN account_move_line source_line ON source_line.id = part.{source_field}_move_id
                        JOIN account_account account ON account.id = source_line.account_id
                        JOIN account_move_line counterpart_line ON counterpart_line.id = part.{counterpart_field}_move_id
                        JOIN account_move counterpart_move ON counterpart_move.id = counterpart_line.move_id
                        LEFT JOIN account_payment pay ON pay.id = counterpart_move.payment_id
                        WHERE source_line.move_id IN %s AND counterpart_line.move_id != source_line.move_id
                        GROUP BY source_line_id, source_move_id, source_line_account_type
                    ''')

            self._cr.execute(' UNION ALL '.join(queries), [stored_ids, stored_ids])

            payment_data = defaultdict(lambda: [])
            for row in self._cr.dictfetchall():
                payment_data[row['source_move_id']].append(row)
        else:
            payment_data = {}

        for invoice in self:
            if invoice.payment_state == 'invoicing_legacy':
                # invoicing_legacy state is set via SQL when setting setting field
                # invoicing_switch_threshold (defined in account_accountant).
                # The only way of going out of this state is through this setting,
                # so we don't recompute it here.
                continue

            currencies = invoice._get_lines_onchange_currency().currency_id
            currency = currencies if len(currencies) == 1 else invoice.company_id.currency_id
            reconciliation_vals = payment_data.get(invoice.id, [])
            payment_state_matters = invoice.is_invoice(True)

            # Restrict on 'receivable'/'payable' lines for invoices/expense entries.
            if payment_state_matters:
                reconciliation_vals = [x for x in reconciliation_vals if
                                       x['source_line_account_type'] in ('asset_receivable', 'liability_payable')]

            new_pmt_state = 'not_paid'
            if invoice.state == 'posted':
                new_pmt_state = 'unpaid'
                # Posted invoice/expense entry.
                if payment_state_matters:

                    if currency.is_zero(invoice.amount_residual):
                        if any(x['has_payment'] or x['has_st_line'] for x in reconciliation_vals):

                            # Check if the invoice/expense entry is fully paid or 'in_payment'.
                            if all(x['all_payments_matched'] for x in reconciliation_vals):
                                new_pmt_state = 'paid'
                            else:
                                new_pmt_state = invoice._get_invoice_in_payment_state()

                        else:
                            new_pmt_state = 'paid'

                            reverse_move_types = set()
                            for x in reconciliation_vals:
                                for move_type in x['counterpart_move_types']:
                                    reverse_move_types.add(move_type)

                            in_reverse = (invoice.move_type in ('in_invoice', 'in_receipt')
                                          and (reverse_move_types == {'in_refund'} or reverse_move_types == {
                                        'in_refund', 'entry'}))
                            out_reverse = (invoice.move_type in ('out_invoice', 'out_receipt')
                                           and (reverse_move_types == {'out_refund'} or reverse_move_types == {
                                        'out_refund', 'entry'}))
                            misc_reverse = (invoice.move_type in ('entry', 'out_refund', 'in_refund')
                                            and reverse_move_types == {'entry'})
                            if in_reverse or out_reverse or misc_reverse:
                                new_pmt_state = 'reversed'

                    elif reconciliation_vals:
                        new_pmt_state = 'partial'

            invoice.payment_state = new_pmt_state

    @api.depends('restrict_mode_hash_table', 'state')
    def _compute_show_reset_to_draft_button(self):
        for move in self:
            move.show_reset_to_draft_button = not move.restrict_mode_hash_table and move.state in (
            'posted', 'approved', 'cancel')

    
    def action_post(self):
        # validate sales order  
        for rec in self.invoice_line_ids:
            logger.info("3", rec.name)
            if rec.sale_line_ids.order_id.state == 'draft':
                raise UserError(_("You are not allowed to confirm, please confirm sale order first!"))

        # for move in self:
        #     if move.state == 'approved':
        #         move.write({'state': 'posted'})
        #     else:
        #         move.write({'state': 'approved'})

        res = super(CrmAccountMove, self).action_post()
        return res


    @api.depends(
        'invoice_line_ids.currency_rate',
        'invoice_line_ids.tax_base_amount',
        'invoice_line_ids.tax_line_id',
        'invoice_line_ids.price_total',
        'invoice_line_ids.price_subtotal',
        'invoice_payment_term_id',
        'partner_id',
        'currency_id',
    )
    def _compute_tax_totals(self):
        """ Computed field used for custom widget's rendering.
            Only set on invoices.
        """
        for move in self:
            if move.is_invoice(include_receipts=True):
                base_lines = move.invoice_line_ids.filtered(lambda line: line.display_type == 'product')
                base_line_values_list = [line._convert_to_tax_base_line_dict() for line in base_lines]
                sign = move.direction_sign
                if move.id:
                    # The invoice is stored so we can add the early payment discount lines directly to reduce the
                    # tax amount without touching the untaxed amount.
                    base_line_values_list += [
                        {
                            **line._convert_to_tax_base_line_dict(),
                            'handle_price_include': False,
                            'quantity': 1.0,
                            'price_unit': sign * line.amount_currency,
                        }
                        for line in move.line_ids.filtered(lambda line: line.display_type == 'epd')
                    ]

                kwargs = {
                    'base_lines': base_line_values_list,
                    'currency': move.currency_id or move.journal_id.currency_id or move.company_id.currency_id,
                }

                if move.id:
                    kwargs['tax_lines'] = [
                        line._convert_to_tax_line_dict()
                        for line in move.line_ids.filtered(lambda line: line.display_type == 'tax')
                    ]
                else:
                    # In case the invoice isn't yet stored, the early payment discount lines are not there. Then,
                    # we need to simulate them.
                    epd_aggregated_values = {}
                    for base_line in base_lines:
                        if not base_line.epd_needed:
                            continue
                        for grouping_dict, values in base_line.epd_needed.items():
                            epd_values = epd_aggregated_values.setdefault(grouping_dict, {'price_subtotal': 0.0})
                            epd_values['price_subtotal'] += values['price_subtotal']

                    for grouping_dict, values in epd_aggregated_values.items():
                        taxes = None
                        if grouping_dict.get('tax_ids'):
                            taxes = self.env['account.tax'].browse(grouping_dict['tax_ids'][0][2])

                        kwargs['base_lines'].append(self.env['account.tax']._convert_to_tax_base_line_dict(
                            None,
                            partner=move.partner_id,
                            currency=move.currency_id,
                            taxes=taxes,
                            price_unit=values['price_subtotal'],
                            quantity=1.0,
                            account=self.env['account.account'].browse(grouping_dict['account_id']),
                            analytic_distribution=values.get('analytic_distribution'),
                            price_subtotal=values['price_subtotal'],
                            is_refund=move.move_type in ('out_refund', 'in_refund'),
                            handle_price_include=False,
                        ))
                move.tax_totals = self.env['account.tax']._prepare_tax_totals(**kwargs)
                tax_totals = move.tax_totals


                tax_totals['amount_total'] = tax_totals['amount_total']
                tax_totals['formatted_amount_total'] = formatLang(self.env, tax_totals['amount_total'], currency_obj=move.currency_id)

                if move.invoice_cash_rounding_id:
                    rounding_amount = move.invoice_cash_rounding_id.compute_difference(move.currency_id,
                                                                                       move.tax_totals['amount_total'])
                    totals = move.tax_totals
                    totals['display_rounding'] = True
                    if rounding_amount:
                        if move.invoice_cash_rounding_id.strategy == 'add_invoice_line':
                            totals['rounding_amount'] = rounding_amount
                            totals['formatted_rounding_amount'] = formatLang(self.env, totals['rounding_amount'],
                                                                             currency_obj=move.currency_id)
                            totals['amount_total_rounded'] = totals['amount_total'] + rounding_amount
                            totals['formatted_amount_total_rounded'] = formatLang(self.env,
                                                                                  totals['amount_total_rounded'],
                                                                                  currency_obj=move.currency_id)
                        elif move.invoice_cash_rounding_id.strategy == 'biggest_tax':
                            if totals['subtotals_order']:
                                max_tax_group = max((
                                    tax_group
                                    for tax_groups in totals['groups_by_subtotal'].values()
                                    for tax_group in tax_groups
                                ), key=lambda tax_group: tax_group['tax_group_amount'])
                                max_tax_group['tax_group_amount'] += rounding_amount
                                max_tax_group['formatted_tax_group_amount'] = formatLang(self.env, max_tax_group[
                                    'tax_group_amount'], currency_obj=move.currency_id)
                                totals['amount_total'] += rounding_amount
                                totals['formatted_amount_total'] = formatLang(self.env, totals['amount_total'],
                                                                              currency_obj=move.currency_id)
            else:
                # Non-invoice moves don't support that field (because of multicurrency: all lines of the invoice share the same currency)
                move.tax_totals = None

    @contextmanager
    def _check_balanced(self, container):
        ''' Assert the move is fully balanced debit = credit.
        An error is raised if it's not the case.
        '''
        with self._disable_recursion(container, 'check_move_validity', default=True, target=False) as disabled:
            yield
            if disabled:
                return

        unbalanced_moves = self._get_unbalanced_moves(container)
        is_merge_inv = self.env.context.get("source") == 'merge_inv'

        if unbalanced_moves and not is_merge_inv:
            error_msg = _("An error has occurred.")
            for move_id, sum_debit, sum_credit in unbalanced_moves:
                move = self.browse(move_id)
                error_msg += _(
                    "\n\n"
                    "The move (%s) is not balanced.\n"
                    "The total of debits equals %s and the total of credits equals %s.\n"
                    "You might want to specify a default account on journal \"%s\" to automatically balance each move.",
                    move.display_name,
                    format_amount(self.env, sum_debit, move.company_id.currency_id),
                    format_amount(self.env, sum_credit, move.company_id.currency_id),
                    move.journal_id.name)
            raise UserError(error_msg)

    def action_merge_invoices(self):
        for move in self:
            if move.state == 'posted':
                raise UserError(_("Merge invoice only possible for draft!"))

        move_selected = self.filtered(lambda x: x.state == 'draft')
        if len(move_selected) <= 1:
            raise UserError(_("At least select 2 records draft invoice!"))

        move_header = move_selected[0]
        for line in move_selected.line_ids.filtered(lambda x: x.move_id != move_header and x.display_type == 'product'):
            line.copy(default={'move_id': move_header.id})

        header_payment = move_header.line_ids.filtered(
            lambda x: x.display_type == 'payment_term' and x.is_downpayment == False)
        header_payment.debit = sum(
            [x.credit for x in move_header.line_ids.filtered(lambda x: x.display_type == 'product')])
        header_payment.balance = sum(
            [x.credit for x in move_header.line_ids.filtered(lambda x: x.display_type == 'product')])
        header_payment.amount_currency = sum(
            [x.credit for x in move_header.line_ids.filtered(lambda x: x.display_type == 'product')])
        header_payment.amount_residual = sum(
            [x.credit for x in move_header.line_ids.filtered(lambda x: x.display_type == 'product')])
        header_payment.amount_residual_currency = sum(
            [x.credit for x in move_header.line_ids.filtered(lambda x: x.display_type == 'product')])

        fileterd_moves = move_selected.filtered(lambda x: x.id != move_header.id)
        for move in fileterd_moves:
            move.state = 'cancel'

        return True
    

    def action_post(self):
        moves_with_payments = self.filtered('payment_id')
        other_moves = self - moves_with_payments
        if moves_with_payments:
            moves_with_payments.payment_id.action_post()
        if other_moves:
            other_moves._post(soft=False)
        return False
    
    def _post(self, soft=True):
        """Post/Validate the documents.

        Posting the documents will give it a number, and check that the document is
        complete (some fields might not be required if not posted but are required
        otherwise).
        If the journal is locked with a hash table, it will be impossible to change
        some fields afterwards.

        :param soft (bool): if True, future documents are not immediately posted,
            but are set to be auto posted automatically at the set accounting date.
            Nothing will be performed on those documents before the accounting date.
        :return Model<account.move>: the documents that have been posted
        """
        if not self.env.su and not self.env.user.has_group('account.group_account_invoice'):
            raise AccessError(_("You don't have the access rights to post an invoice."))

        for invoice in self.filtered(lambda move: move.is_invoice(include_receipts=True)):
            if invoice.quick_edit_mode and invoice.quick_edit_total_amount and invoice.quick_edit_total_amount != invoice.amount_total:
                raise UserError(_(
                    "The current total is %s but the expected total is %s. In order to post the invoice/bill, "
                    "you can adjust its lines or the expected Total (tax inc.).",
                    formatLang(self.env, invoice.amount_total, currency_obj=invoice.currency_id),
                    formatLang(self.env, invoice.quick_edit_total_amount, currency_obj=invoice.currency_id),
                ))
            if invoice.partner_bank_id and not invoice.partner_bank_id.active:
                raise UserError(_(
                    "The recipient bank account linked to this invoice is archived.\n"
                    "So you cannot confirm the invoice."
                ))
            if float_compare(invoice.amount_total, 0.0, precision_rounding=invoice.currency_id.rounding) < 0:
                raise UserError(_(
                    "You cannot validate an invoice with a negative total amount. "
                    "You should create a credit note instead. "
                    "Use the action menu to transform it into a credit note or refund."
                ))

            if not invoice.partner_id:
                if invoice.is_sale_document():
                    raise UserError(_("The field 'Customer' is required, please complete it to validate the Customer Invoice."))
                elif invoice.is_purchase_document():
                    raise UserError(_("The field 'Vendor' is required, please complete it to validate the Vendor Bill."))

            # Handle case when the invoice_date is not set. In that case, the invoice_date is set at today and then,
            # lines are recomputed accordingly.
            if not invoice.invoice_date:
                if invoice.is_sale_document(include_receipts=True):
                    invoice.invoice_date = fields.Date.context_today(self)
                elif invoice.is_purchase_document(include_receipts=True):
                    raise UserError(_("The Bill/Refund date is required to validate this document."))

        for move in self:
            if move.state == 'posted':
                raise UserError(_('The entry %s (id %s) is already posted.') % (move.name, move.id))
            if not move.line_ids.filtered(lambda line: line.display_type not in ('line_section', 'line_note')):
                raise UserError(_('You need to add a line before posting.'))
            if not soft and move.auto_post != 'no' and move.date > fields.Date.context_today(self):
                date_msg = move.date.strftime(get_lang(self.env).date_format)
                raise UserError(_("This move is configured to be auto-posted on %s", date_msg))
            if not move.journal_id.active:
                raise UserError(_(
                    "You cannot post an entry in an archived journal (%(journal)s)",
                    journal=move.journal_id.display_name,
                ))
            if move.display_inactive_currency_warning:
                raise UserError(_(
                    "You cannot validate a document with an inactive currency: %s",
                    move.currency_id.name
                ))

            if move.line_ids.account_id.filtered(lambda account: account.deprecated):
                raise UserError(_("A line of this move is using a deprecated account, you cannot post it."))

        if soft:
            future_moves = self.filtered(lambda move: move.date > fields.Date.context_today(self))
            for move in future_moves:
                if move.auto_post == 'no':
                    move.auto_post = 'at_date'
                msg = _('This move will be posted at the accounting date: %(date)s', date=format_date(self.env, move.date))
                move.message_post(body=msg)
            to_post = self - future_moves
        else:
            to_post = self

        for move in to_post:
            affects_tax_report = move._affect_tax_report()
            lock_dates = move._get_violated_lock_dates(move.date, affects_tax_report)
            if lock_dates:
                move.date = move._get_accounting_date(move.invoice_date or move.date, affects_tax_report)

        # Create the analytic lines in batch is faster as it leads to less cache invalidation.
        to_post.line_ids._create_analytic_lines()

        # Trigger copying for recurring invoices
        to_post.filtered(lambda m: m.auto_post not in ('no', 'at_date'))._copy_recurring_entries()

        for invoice in to_post:
            # Fix inconsistencies that may occure if the OCR has been editing the invoice at the same time of a user. We force the
            # partner on the lines to be the same as the one on the move, because that's the only one the user can see/edit.
            wrong_lines = invoice.is_invoice() and invoice.line_ids.filtered(lambda aml:
                aml.partner_id != invoice.commercial_partner_id
                and aml.display_type not in ('line_note', 'line_section')
            )
            if wrong_lines:
                wrong_lines.write({'partner_id': invoice.commercial_partner_id.id})
        
        to_post.write({
            'state': 'posted',
            'posted_before': True,
        })
  

        for invoice in to_post:
            invoice.message_subscribe([
                p.id
                for p in [invoice.partner_id]
                if p not in invoice.sudo().message_partner_ids
            ])

         
                

            if (
                invoice.is_sale_document()
                and invoice.journal_id.sale_activity_type_id
                and (invoice.journal_id.sale_activity_user_id or invoice.invoice_user_id).id not in (self.env.ref('base.user_root').id, False)
            ):
                invoice.activity_schedule(
                    date_deadline=min((date for date in invoice.line_ids.mapped('date_maturity') if date), default=invoice.date),
                    activity_type_id=invoice.journal_id.sale_activity_type_id.id,
                    summary=invoice.journal_id.sale_activity_note,
                    user_id=invoice.journal_id.sale_activity_user_id.id or invoice.invoice_user_id.id,
                )

        customer_count, supplier_count = defaultdict(int), defaultdict(int)
        for invoice in to_post:
            if invoice.is_sale_document():
                customer_count[invoice.partner_id] += 1
            elif invoice.is_purchase_document():
                supplier_count[invoice.partner_id] += 1
            elif invoice.move_type == 'entry':
                sale_amls = invoice.line_ids.filtered(lambda line: line.partner_id and line.account_id.account_type == 'asset_receivable')
                for partner in sale_amls.mapped('partner_id'):
                    customer_count[partner] += 1
                purchase_amls = invoice.line_ids.filtered(lambda line: line.partner_id and line.account_id.account_type == 'liability_payable')
                for partner in purchase_amls.mapped('partner_id'):
                    supplier_count[partner] += 1
        for partner, count in customer_count.items():
            (partner | partner.commercial_partner_id)._increase_rank('customer_rank', count)
        for partner, count in supplier_count.items():
            (partner | partner.commercial_partner_id)._increase_rank('supplier_rank', count)

        # Trigger action for paid invoices if amount is zero
        to_post.filtered(
            lambda m: m.is_invoice(include_receipts=True) and m.currency_id.is_zero(m.amount_total)
        )._invoice_paid_hook()

        return to_post

    def generate_default_name(self,name):
            # Get the sale.order.sequence
            new_name = self.inv_no
            old_name = name
            
            # Ensure the sequence exists
            if name:
                # Get the next value from the sequence
                
                # Extract the last three digits
                last_three_digits = name[-3:]

                # Check if the last three digits are 999
                if last_three_digits == '999':
                    # Extract the last four digits
                    last_four_digits = name[-4:]
                    name = f"{last_four_digits}/EXT-QUOT/{current_month}/{current_year}"
                else:
                    # Get the current month and year
                    current_month = fields.Date.today().month
                    current_year = fields.Date.today().year

                    # Format the name
                    name = f"{last_three_digits}/CS-{current_month}/{current_year}"
                
                    if new_name:
                        return new_name
                    else:
                        return name
                    
                

            return False
    

    
    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        self = self.sorted(lambda m: (m.date, m.ref or '', m.id))

        for move in self:
            move_has_name = move.name and move.name != '/'
            if move_has_name or move.state != 'posted':
                if not move.posted_before and not move._sequence_matches_date():
                    if move._get_last_sequence(lock=False):
                        # The name does not match the date and the move is not the first in the period:
                        # Reset to draft
                        move.name = False
                        continue
                else:
                    if move_has_name and move.posted_before or not move_has_name and move._get_last_sequence(lock=False):
                        # The move either
                        # - has a name and was posted before, or
                        # - doesn't have a name, but is not the first in the period
                        # so we don't recompute the name
                        continue
            if move.date and (not move_has_name or not move._sequence_matches_date()):
                
                move._set_next_sequence()
                
            move.inv_no = CrmAccountMove.generate_default_name(self,move.name)
            
        self.filtered(lambda m: not m.name and not move.quick_edit_mode).name = '/'
        self._inverse_name()

    def action_invoice_print(self):
        logger.info("print")
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        if any(not move.is_invoice(include_receipts=True) for move in self):
            raise UserError(_("Only invoices could be printed."))

        self.filtered(lambda inv: not inv.is_move_sent).write({'is_move_sent': True})
        if self.user_has_groups('account.group_account_invoice'):
            return self.env.ref('account.account_invoices').report_action(self)
        else:
            return self.env.ref('account.account_invoices_without_payment').report_action(self)
        
    def action_send_and_print(self):
        return {
            'name': _('Send Invoice'),
            'res_model': 'account.invoice.send',
            'view_mode': 'form',
            'context': {
                'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
                'default_template_id': self.env.ref(self._get_mail_template()).id,
                'mark_invoice_as_sent': True,
                'active_model': 'account.move',
                # Setting both active_id and active_ids is required, mimicking how direct call to
                # ir.actions.act_window works
                'active_id': self.ids[0],
                'active_ids': self.ids,
                
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        
        }
    def _get_move_display_name(self, show_ref=False):
        ''' Helper to get the display name of an invoice depending of its type.
        :param show_ref:    A flag indicating of the display name must include or not the journal entry reference.
        :return:            A string representing the invoice.
        '''
        self.ensure_one()
        name = ''
        if self.state == 'draft':
            name += {
                'out_invoice': _('Draft Invoice'),
                'out_refund': _('Draft Credit Note'),
                'in_invoice': _('Draft Bill'),
                'in_refund': _('Draft Vendor Credit Note'),
                'out_receipt': _('Draft Sales Receipt'),
                'in_receipt': _('Draft Purchase Receipt'),
                'entry': _('Draft Entry'),
            }[self.move_type]
            name += ' '
        if not self.inv_no or self.inv_no == '/':
            
            name += '(* %s)' % str(self.id)
        else:
            
            # name += self.inv_no.replace('-','_')
            name += self.inv_no
            
            if self.env.context.get('input_full_display_name'):
                logger.info("inv")
                if self.partner_id:
                    name += f', {self.partner_id.name}'
                if self.date:
                    name += f', {format_date(self.env, self.date)}'
            
            return name + (f" ({shorten(self.ref, width=50)})" if show_ref and self.ref else '')
           
         

    
    # def create(self):
    #     # Implement the logic to create a new period record
    #     new_period = self.create({
    #         'account_move_id': self.account_move_id,  # Set the account move ID as needed
    #         # Add other field values as needed
    #     })
    #     return new_period

        
    

