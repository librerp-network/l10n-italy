# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import models, api, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountRegisterPayment(models.TransientModel):
    _name = 'wizard.account.register.payment'
    _description = 'Register payment from duedates tree view'

    def _set_sezionale(self):
        bank_account = self._get_bank_account()
        return bank_account.id

    def _set_total_amount(self):
        amount = 0.0
        lines = self.env['account.move.line'].browse(
            self._context['active_ids']
        )
        for line in lines:
            amount += line.balance
        return amount

    journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Registro',
        domain=[('is_wallet', '=', False), ('type', 'in', ('bank', 'cash'))],
        default=_set_sezionale,
    )

    registration_date = fields.Date(
        string='Data di registrazione',
        default=fields.Date.today()
    )

    expenses_account = fields.Many2one(
        comodel_name='account.account',
        string='Conto spese bancarie',
    )

    expenses_amount = fields.Float(string='Importo spese')

    total_amount = fields.Float(
        string='Importo pagamento',
        default=_set_total_amount
    )

    note = fields.Text(string='Nota')

    payment_difference = fields.Float(
        string='Differenza di pagamento',
        default=0.0
    )

    payment_difference_show = fields.Float(
        string='Differenza di pagamento',
        default=0.0
    )

    payment_difference_open = fields.Boolean(
        string="Lasciare aperto",
        copy=False,
        default=True,
    )

    def _get_bank_account(self):
        bank_account = self.env['account.journal']
        lines = self.env['account.move.line'].browse(
            self._context['active_ids']
        )
        for line in lines:
            # Detect lines already reconciled
            if line.company_bank_id.id:
                bank_account = line.company_bank_id.journal_id
                break
        return bank_account
    # end _get_bank_account

    @api.onchange('total_amount')
    def _onchange_total_amount(self):
        rebates = self._get_rebates_data()
        if not rebates['rebate_delta']:
            raise UserError(
                'Delta abbuoni non impostato '
                'in configurazione contabilità.'
            )

        wizard_amount = self.total_amount
        total_amount = self._set_total_amount()

        if wizard_amount > total_amount:
            total = wizard_amount - total_amount
            if total > rebates['rebate_delta']:
                raise UserError(
                    'La differenza tra il totale e l\'importo impostato '
                    ' supera la cifra indicata in configurazione contabilità.'
                )

            self.payment_difference = total
            self.payment_difference_show = -total
        elif wizard_amount < total_amount:
            total = total_amount - wizard_amount
            self.payment_difference = total
            self.payment_difference_show = total
        else:
            self.payment_difference = 0.0

        if self.payment_difference >= rebates['rebate_delta']:
            self.payment_difference_open = True
        elif self.payment_difference < rebates['rebate_delta']:
            self.payment_difference_open = False

    @api.model
    def _get_rebates_data(self):
        rebates = {}
        company = self.env['res.company'].browse(self.env.user.company_id.id)
        rebates['rebate_active'] = company.rebate_active
        rebates['rebate_passive'] = company.rebate_passive
        rebates['rebate_delta'] = company.rebate_delta
        return rebates
    # end _get_rebates_data

    def register(self):

        def payment_reg_move_create():

            # Create the new account.move
            payment_reg_move_vals = self.env['account.move'].default_get([
                'date_effective',
                'fiscalyear_id',
                'invoice_date',
                'narration',
                'payment_term_id',
                'reverse_date',
                'tax_type_domain',
            ])

            payment_reg_move_vals.update({
                'date': self.registration_date,
                'date_apply_vat': self.registration_date,
                'journal_id': self.journal_id.id,
                'type': 'entry',
                'ref': "Registrazione pagamento ",
                'state': 'draft',
            })

            created_move = self.env['account.move'].create(payment_reg_move_vals)

            return created_move
        # end create_payment_reg_move

        def payment_reg_move_add_lines():

            # For each input line add one line to the new account.move
            for in_line in in_lines_list:

                # Create the new line with credit and debit swapped relative to the in_line
                # NOTE: Odoo ensures each account.move.line has a credit value != 0 OR a debit value !=0
                #       (that is: Odoo forbids account-move.lines with both credit and debit != 0)
                new_line = move_line_model_no_check.create({
                    'move_id': payment_reg_move.id,
                    'account_id': in_line.account_id.id,
                    'partner_id': in_line.partner_id.id,
                    'credit': in_line.debit,
                    'debit': in_line.credit,
                })

                # Reconciliation pair. The actual reconciliation will be performed
                # AFTER the confirmation (post() method call) of the new move.
                to_reconcile.append(in_line | new_line)
            # end for

            if client_payment_reg_op:

                bank_debit = in_debit_total - in_credit_total

                # Create the bank line
                bank_line = move_line_model_no_check.create({
                    'move_id': payment_reg_move.id,
                    'account_id': bank_line_account.id,
                    'credit': 0,
                    'debit': bank_debit,
                })
            elif supplier_payment_reg_op:

                bank_credit = in_credit_total - in_debit_total

                # Create the bank line
                bank_line = move_line_model_no_check.create({
                    'move_id': payment_reg_move.id,
                    'account_id': bank_line_account.id,
                    'credit': bank_credit,
                    'debit': 0,
                })
            else:

                assert False
            # end if
        # end payment_reg_move_add_lines

        def payment_reg_move_add_expenses():

            if self.expenses_account and self.expenses_account.id:

                # Riga di costo
                cost_line = move_line_model_no_check.create({
                    'move_id': payment_reg_move.id,
                    'account_id': self.expenses_account.id,
                    'credit': 0,
                    'debit': self.expenses_amount,
                })

                # Riga di banca
                bank_line = move_line_model_no_check.create({
                    'move_id': payment_reg_move.id,
                    'account_id': bank_expenses_account.id,
                    'credit': self.expenses_amount,
                    'debit': 0,
                })
            # end if
        # payment_reg_move_add_expenses

        def payment_reg_move_confirm_and_reconcile():

            # Confirm the account.move
            payment_reg_move.post()

            # Create reconciliations
            for pair in to_reconcile:
                pair.reconcile()
            # end if
        # end payment_reg_move_confirm_and_reconcile

        def payment_handle_difference():
            if self.payment_difference:
                calculated_total = self._set_total_amount()
                if self.total_amount > calculated_total:
                    rebate_vals = {
                        'move_id': payment_reg_move.id,
                        'debit': 0,
                        'credit': self.payment_difference,
                        'account_id': self.rebate_active.id,
                    }

                elif self.total_amount < calculated_total and (
                    self.payment_difference_open is False):
                    # open or close
                    rebate_vals = {
                        'move_id': payment_reg_move.id,
                        'debit': self.payment_difference,
                        'credit': 0,
                        'account_id': self.rebate_passive.id,
                    }
                # end if
                if rebate_vals:
                    move_line_model_no_check.create(rebate_vals)
            # end if

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Initial variables

        in_credit_total = 0
        in_debit_total = 0

        bank_line_account = None

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Accounting rebate
        company = self.env['res.company'].browse(self.env.user.company_id.id)
        rebate_active = company.rebate_active
        rebate_passive = company.rebate_passive
        rebate_delta = company.rebate_delta

        to_reconcile = list()

        move_line_model_no_check = self.env['account.move.line'].with_context(
            check_move_validity=False
        )

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Retrieve and validate lines

        # Get account.line objects from web UI selection
        selected_lines_ids = self._context['active_ids']
        # ordered
        in_lines_list = self.env['account.move.line'].search(
            [('id', 'in', selected_lines_ids)],
            order='date_maturity ASC',
        )

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Validate the type of operation

        # Identify the type of operation
        client_payment_reg_op = any(filter(
            lambda ln: ln.user_type_id.type == 'receivable', in_lines_list
        ))
        supplier_payment_reg_op = any(filter(
            lambda ln: ln.user_type_id.type == 'payable', in_lines_list
        ))
        assert client_payment_reg_op or supplier_payment_reg_op, (
            'Nessuna linea selezionata per l\'operazione '
            'di registrazione pagamento.'
        )

        # Ensure than there are only client OR supplier lines but NOT BOTH
        if client_payment_reg_op and supplier_payment_reg_op:
            msg = (
                'Non è possibile creare un\'unica registrazione per '
                'registrare contemporaneamente pagamenti cliente e '
                'fornitore.\nUtilizzare la funzione di compensazione.'
            )
            raise UserError(msg)
        # end if

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Validate the amount of the operation

        # Ensure we are not inverting the operation or
        # doing a pure reconciliation due to:
        #   - having mixed invoices and credit notes
        #   - total amount of credit notes >= total amount of invoices
        in_credit_total = sum([in_line.credit for in_line in in_lines_list])
        in_debit_total = sum([in_line.debit for in_line in in_lines_list])

        if client_payment_reg_op and not in_debit_total > in_credit_total:
            raise UserError(
                'L\'importo delle note di credito deve essere '
                'minore dell\'importo delle fatture cliente'
            )
        # end if

        if supplier_payment_reg_op and not in_credit_total > in_debit_total:
            raise UserError(
                'L\'importo delle note di credito deve essere '
                'minore dell\'importo delle fatture fornitore'
            )
        # end if

        # Ensure the required default account is set in the bank registry
        if client_payment_reg_op:

            bank_line_account = self.journal_id.default_debit_account_id

            if not (bank_line_account and bank_line_account.id):
                raise UserError(
                    'Conto dare di default non impostato '
                    'nel registro della banca.'
                )
            # end if

        elif supplier_payment_reg_op:

            bank_line_account = self.journal_id.default_credit_account_id

            if not(bank_line_account and bank_line_account.id):
                raise UserError(
                    'Conto avere di default non impostato '
                    'nel registro della banca.'
                )
            # end if

        # end if

        assert bank_line_account and bank_line_account.id, (
            'Non è stato possibile identificare il conto da '
            'utilizzare per creare la move.line della banca.'
        )
        # end if

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Validate expenses
        if self.expenses_account and self.expenses_account.id:

            # Importo spese
            if self.expenses_amount <= 0:
                raise UserError(
                    'L\'importo delle spese deve essere maggiore di zero'
                )
            # end if

            # Conto di registrazione delle spese nel journal della banca
            bank_expenses_account = self.journal_id.default_credit_account_id

            if not(bank_expenses_account and bank_expenses_account.id):
                raise UserError(
                    'Conto avere di default non impostato nel registro '
                    'della banca, questo conto è necessario per '
                    'registrare le spese bancarie.'
                )
            # end if
        # end if

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Create the registration

        # Payment registration move
        # ok
        payment_reg_move = payment_reg_move_create()

        # adding lines
        payment_reg_move_add_lines()
        # adding extra lines according to total
        payment_handle_difference()
        # add bank expenses
        payment_reg_move_add_expenses()

        # ??
        payment_reg_move_confirm_and_reconcile()

    # end register
# end AccountRegisterPayment
