#
# Copyright (c) 2020
#
import logging
from odoo import api, fields, models
# from odoo.exceptions import UserError, Warning

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _get_default_invoice_date_13(self):
        return fields.Date.today() if self._context.get(
            'default_type', 'entry') in (
            'in_invoice', 'in_refund', 'in_receipt') else False

    @api.multi
    @api.depends('line_ids')
    def count_line_ids(self):
        for rec in self:
            rec.lines_count = len(rec.line_ids)
        # end for
    # end def

    fiscalyear_id = fields.Many2one('account.fiscal.year',
                                    string="Esercizio contabile")
    # Naming of 13.0 differs from account.invoice.date_invoice
    invoice_date_13 = fields.Date(
        string='Data documento',
        readonly=True, index=True, copy=False,
        states={'draft': [('readonly', False)]},
        default=_get_default_invoice_date_13,
        help="Keep empty to use the current date",
        oldname='invoice_date'
    )
    # Naming of 13.0 same as account.invoice.type
    type_13 = fields.Selection(
        [
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            # ('out_receipt', 'Sales Receipt'),
            # ('in_receipt', 'Purchase Receipt'),
        ],
        readonly=True,
        states={'draft': [('readonly', False)]},
        index=True,
        change_default=True,
        default='entry',
        track_visibility='always',
        required=True,
    )
    type_zz = fields.Selection(
        [
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            # ('out_receipt', 'Sales Receipt'),
            # ('in_receipt', 'Purchase Receipt'),
        ],
        readonly=True,
        states={'draft': [('readonly', False)]},
        index=True,
        change_default=True,
        default='entry',
        track_visibility='always',
        required=True,
    )
    date_apply_balance = fields.Date(
        string='Data competenza',
        # readonly=True,
        # states={'draft': [('readonly', False)]},
        # index=True,
        # help="Keep empty to use the current date",
        # copy=False
    )

    lines_count = fields.Integer(compute='count_line_ids')

    payment_term_id_13 = fields.Many2one(
        comodel_name='account.payment.term',
        string='Termine di pagamento',
        oldname='payment_term_id'
    )
