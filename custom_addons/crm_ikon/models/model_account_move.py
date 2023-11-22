from odoo import models, _, fields, api
from odoo.exceptions import UserError
from contextlib import contextmanager
from odoo.tools import formatLang, format_amount
import inflect
import logging

logger = logging.getLogger(__name__)

class CrmAccountMove(models.Model):
    _inherit = "account.move"

    attention = fields.Char(string="Attention")
    inv_no = fields.Char(string='Invoice No.')
    pph = fields.Float(string='PPH Invoice', default=0.00)
    pph_price = fields.Float(compute="_compute_pph_price", default=0.00)
    in_word = fields.Char(string="In Word", compute="_compute_in_word", store=True)

    @api.depends('amount_total')
    def _compute_in_word(self):
        p = inflect.engine()
        for record in self:
            if record.amount_total:
                amount_in_words = p.number_to_words(record.amount_total)
                
                amount_in_words = amount_in_words.replace(" and", "").replace(" point zero", " Rupiah")
                logger.info("1", amount_in_words)
                record.in_word = amount_in_words
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

    hide_post_button = fields.Boolean(compute='_compute_hide_post_button', readonly=True, default=True)

    def action_approve(self):
        for move in self:
            if move.state == 'approved':
                move.write({'state': 'posted'})
            else:
                move.write({'state': 'approved'})

    @api.depends('restrict_mode_hash_table', 'state')
    def _compute_show_reset_to_draft_button(self):
        for move in self:
            move.show_reset_to_draft_button = not move.restrict_mode_hash_table and move.state in ('posted', 'approved', 'cancel')





    def action_post(self):
        # validate sales order  
        for rec in self.invoice_line_ids:
            if rec.sale_line_ids.order_id.state == 'draft':
                raise UserError(_("You are not allowed to confirm, please confirm sale order first!"))

        # for move in self:
        #     if move.state == 'approved':
        #         move.write({'state': 'posted'})
        #     else:
        #         move.write({'state': 'approved'})

        res = super(CrmAccountMove, self).action_post()
        return res



    @api.depends('pph', 'amount_total')
    def _compute_pph_price(self):
        for rec in self:
            rec.pph_price = -1 * (rec.pph * 0.01 * rec.amount_total)

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

                tax_totals['amount_total'] = tax_totals['amount_total'] + move.pph_price
                tax_totals['formatted_amount_total'] = formatLang(self.env, tax_totals['amount_total'], currency_obj=move.currency_id)
                if move.invoice_cash_rounding_id:
                    rounding_amount = move.invoice_cash_rounding_id.compute_difference(move.currency_id, move.tax_totals['amount_total'])
                    totals = move.tax_totals
                    totals['display_rounding'] = True
                    if rounding_amount:
                        if move.invoice_cash_rounding_id.strategy == 'add_invoice_line':
                            totals['rounding_amount'] = rounding_amount
                            totals['formatted_rounding_amount'] = formatLang(self.env, totals['rounding_amount'], currency_obj=move.currency_id)
                            totals['amount_total_rounded'] = totals['amount_total'] + rounding_amount
                            totals['formatted_amount_total_rounded'] = formatLang(self.env, totals['amount_total_rounded'], currency_obj=move.currency_id)
                        elif move.invoice_cash_rounding_id.strategy == 'biggest_tax':
                            if totals['subtotals_order']:
                                max_tax_group = max((
                                    tax_group
                                    for tax_groups in totals['groups_by_subtotal'].values()
                                    for tax_group in tax_groups
                                ), key=lambda tax_group: tax_group['tax_group_amount'])
                                max_tax_group['tax_group_amount'] += rounding_amount
                                max_tax_group['formatted_tax_group_amount'] = formatLang(self.env, max_tax_group['tax_group_amount'], currency_obj=move.currency_id)
                                totals['amount_total'] += rounding_amount
                                totals['formatted_amount_total'] = formatLang(self.env, totals['amount_total'], currency_obj=move.currency_id)
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

        header_payment = move_header.line_ids.filtered(lambda x: x.display_type == 'payment_term' and x.is_downpayment == False)
        header_payment.debit = sum([x.credit for x in move_header.line_ids.filtered(lambda x: x.display_type=='product')])
        header_payment.balance = sum([x.credit for x in move_header.line_ids.filtered(lambda x: x.display_type=='product')])
        header_payment.amount_currency = sum([x.credit for x in move_header.line_ids.filtered(lambda x: x.display_type=='product')])
        header_payment.amount_residual = sum([x.credit for x in move_header.line_ids.filtered(lambda x: x.display_type=='product')])
        header_payment.amount_residual_currency = sum([x.credit for x in move_header.line_ids.filtered(lambda x: x.display_type=='product')])

        fileterd_moves = move_selected.filtered(lambda x: x.id != move_header.id)
        for move in fileterd_moves:
            move.state = 'cancel'

        return True

