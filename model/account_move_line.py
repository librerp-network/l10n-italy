#
# Copyright 2020 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#


import logging
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _set_default_due_dc(self):
        if self.account_id:
            account_type = self.env['account.account.type'].search(
                [('id', '=', self.account_id.user_type_id.id)])
            if account_type:
                if account_type.type == 'payable':
                    self.due_dc = 'D'
                elif account_type.type == 'receivable':
                    self.due_dc = 'C'
                else:
                    self.due_dc = ''

    @api.depends('due_dc')
    def _value_amount_due(self):
        for record in self:
            if record:
                if record.due_dc == 'C':
                    record.amount_due = record.debit - record.credit
                elif record.due_dc == 'D':
                    record.amount_due = record.credit - record.debit
                else:
                    record.amount_due = 0.0

    @api.onchange('credit', 'debit')
    def onchange_debit_credit(self):
        self._value_amount_due()

    @api.onchange('account_id')
    def onchange_account_id(self):
        domain = []
        if self.account_id:
            account_type = self.env['account.account.type'].search(
                [('id', '=', self.account_id.user_type_id.id)])
            if account_type:
                if account_type.type == 'payable':
                    self.due_dc = 'D'
                    domain = [('payment_type', '=', 'outbound')]
                elif account_type.type == 'receivable':
                    self.due_dc = 'C'
                    domain = [('payment_type', '=', 'inbound')]
                else:
                    self.due_dc = ''
        return {'domain': {'payment_method': domain}}

    # Puntatore alla registrazione contabile a cui si riferisce la scadenza:
    #
    # - se è None/False la riga NON è una scadenza
    # - se punta ad un account.move la riga E' una SCADENZA
    #
    # Se questo campo punta ad un account move allora deve puntare allo stesso
    # record a cui punta il campo move_id
    move_id_duedate = fields.Many2one(
        string='Registrazione contabile',
        comodel_name='account.move',
    )

    due_dc = fields.Selection(
        string="Scadenza debito/credito",
        selection=[('C', 'Credito'), ('D', 'Debito')],
        default=_set_default_due_dc,
        # required=True,
    )
    amount_due = fields.Float(string="Importo scadenza",
                              compute='_value_amount_due',
                              digits=dp.get_precision('Account'))

    payment_method = fields.Many2one('account.payment.method',
                                     string="Metodo di pagamento")

    calculate_field = fields.Char(string='Domain test', compute='_domain_test')

    is_duedate = fields.Boolean(
        string='Riga di scadenza',
        compute='_compute_is_dudate'
    )

    duedate_line_id = fields.Many2one(
        'account.duedate_plus.line',
        string='Riferimento riga scadenza',
        indexed=True,
    )

    @api.model
    def _compute_is_dudate(self):
        for line in self:

            not_vat_line = (not line.tax_ids) and (not line.tax_line_id)
            credit_or_debit = line.account_id.user_type_id.type in (
                'payable', 'receivable'
            )

            line.is_duedate = not_vat_line and credit_or_debit
        # end for
    # end _compute_is_dudate

    def _domain_test(self):
        for rec in self:
            if rec.account_id:
                account_type = self.env['account.account.type'].search(
                    [('id', '=', rec.account_id.user_type_id.id)])
                if account_type:
                    if account_type.type == 'payable':
                        rec.calculate_field = 'outbound'
                    elif account_type.type == 'receivable':
                        rec.calculate_field = 'inbound'


    @api.model
    def create(self, values):

        # Create the new record
        res = super().create(values)

        # Identify due dates rows, if the line is a duedate set the
        # move_id_duedate field so the line will be accessible using the
        # one2many field "duedates" of the "move" objects
        if res.is_duedate:
            res.move_id_duedate = res.move_id
        # end if

        return res
    # end create

# end AccountMoveLine
