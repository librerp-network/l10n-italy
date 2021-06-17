# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
import odoo.addons.decimal_precision as dp
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__file__)


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    split_payment = fields.Boolean('Split Payment')


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def _compute_net_pay(self):
        for inv in self:
            inv.amount_net_pay = inv.amount_total - inv.amount_sp
        # end for

    # end _compute_net_pay

    amount_sp = fields.Float(
        string='Split Payment',
        digits=dp.get_precision('Account'),
        store=True,
        readonly=True,
        compute='_compute_amount')
    split_payment = fields.Boolean(
        'Is Split Payment',
        related='fiscal_position_id.split_payment')

    @api.one
    @api.depends(
        'invoice_line_ids.price_subtotal', 'tax_line_ids.amount',
        'tax_line_ids.amount_rounding',
        'currency_id', 'company_id', 'date_invoice', 'type'
    )
    def _compute_amount(self):
        super(AccountInvoice, self)._compute_amount()
        self.amount_sp = 0
        self.amount_total = self.amount_untaxed + self.amount_tax
        if self.fiscal_position_id.split_payment:
            self.amount_sp = self.amount_tax
            self.amount_tax = 0
        # self.amount_total = self.amount_untaxed + self.amount_tax

    def _build_debit_line(self):
        if not self.company_id.sp_account_id:
            raise UserError(
                _("Please set 'Split Payment Write-off Account' field in"
                  " accounting configuration"))
        vals = {
            'name': _('Split Payment Write Off'),
            'partner_id': self.partner_id.id,
            'account_id': self.company_id.sp_account_id.id,
            'journal_id': self.journal_id.id,
            'date': self.date_invoice,
            'debit': self.amount_sp,
            'credit': 0,
        }
        if self.type == 'out_refund':
            vals['debit'] = 0
            vals['credit'] = self.amount_sp
        return vals

    def _build_client_credit_line(self):
        vals = {
            'name': 'Iva in scissione pagamenti',
            'partner_id': self.partner_id.id,
            'account_id': self.account_id.id,
            'journal_id': self.journal_id.id,
            'date': self.date_invoice,
            'debit': 0,
            'credit': self.amount_sp,
        }
        if self.type == 'out_refund':
            vals['credit'] = 0
            vals['debit'] = self.amount_sp
        return vals

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for invoice in self:
            if invoice.split_payment:
                if invoice.type in ['in_invoice', 'in_refund']:
                    raise UserError(
                        _("Can't handle supplier invoices with split payment"))
                if invoice.move_id.state == 'posted':
                    posted = True
                    invoice.move_id.state = 'draft'

                line_model = self.env['account.move.line']

                tax_duedate = invoice.move_id.line_ids.filtered(
                    lambda x: x.account_id.id == self.account_id.id and x.debit
                              == self.amount_sp and x.partner_id.id ==
                              self.partner_id.id
                )

                transfer_line_vals = invoice._build_client_credit_line()
                transfer_line_vals['move_id'] = invoice.move_id.id
                tranfer = line_model.with_context(
                    check_move_validity=False
                ).create(transfer_line_vals)

                write_off_line_vals = invoice._build_debit_line()
                write_off_line_vals['move_id'] = invoice.move_id.id
                line_model.with_context(
                    check_move_validity=False
                ).create(write_off_line_vals)

                lines_to_rec = line_model.browse([
                    tax_duedate.id,
                    tranfer.id
                ])
                lines_to_rec.reconcile()

                if posted:
                    invoice.move_id.state = 'posted'
                invoice._compute_residual()
        return res
