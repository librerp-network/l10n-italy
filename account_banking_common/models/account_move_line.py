# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from collections import defaultdict
from odoo import models, api, fields
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

from ..utils import validate_selection


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # INSOLUTO
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @api.multi
    def open_wizard_insoluto(self):

        # Retrieve the records
        lines = self.env["account.move.line"].browse(self._context["active_ids"])

        # Perform validations
        validate_selection.insoluto(lines)

        # Open the wizard
        wiz_view = self.env.ref(
            "account_banking_common.wizard_account_banking_common_insoluto"
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Registra Insoluto",
            "res_model": "wizard.account.banking.common.insoluto",
            "view_type": "form",
            "view_mode": "form",
            "view_id": wiz_view.id,
            "target": "new",
            "res_id": False,
            "binding_model_id": "account_banking_common.model_account_move_line",
            "context": {"active_ids": self._context["active_ids"]},
        }

    # end validate_selection

    @api.multi
    def registra_insoluto(self):

        # The payment method of the selected lines
        p_method = self.get_payment_method()

        raise UserError(
            f"Procedura di registrazione insoluto non definita "
            f"per il metodo di pagamento {p_method.name}"
        )

    # end registra_insoluto

    @api.multi
    def registra_insoluto_standard(self):

        # NB: no need to perform checks on the selected lines, the checks have
        #     already been performed by the method:
        #
        #         account.move.line.open_wizard_insoluto()
        #
        #     which gets called by the server action that opens the wizard.

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Variables
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # Sum of insoluti
        amount_insoluti = 0

        # Modify invoice reconciliation
        # True if the move line reconciliation must be removed
        # and a new one registered
        new_reconcile_needed = False

        # Amount of bank expenses to be charged to the client
        # Initially set to zero, if needed will be computed later
        charge_client_for = [0] * len(self)

        # 'account.move.line' model with context to
        # disable move validity checks
        move_line_model_no_check = self.env["account.move.line"].with_context(
            check_move_validity=False
        )

        # "Normal mode" 'account.move.line.model'
        move_line_model = self.env["account.move.line"]

        # Precision to be used in rounding
        float_precision = dp.get_precision("Account")(self.env.cr)[1]

        # - - - - - - - - - - - - - - - - -
        # Data from wizard
        # - - - - - - - - - - - - - - - - -
        expenses_account_id = self._context["expenses_account_id"]
        expenses_amount = self._context["expenses_amount"]
        charge_client = self._context["charge_client"]

        # - - - - - - - - - - - - - - - - -
        # Data from payment order
        # - - - - - - - - - - - - - - - - -

        # NB: since the lines are required to belong to the same
        #     payment order and this constraint has already been
        #     verified we can pick the payment order of the first
        #     record in self

        pol = self[0].payment_line_ids[0]  # Payment order line
        po = pol.order_id  # Payment order

        # pol_partner = pol.partner_id  # Partner for this duedate
        po_journal = po.journal_id  # Journal selected in the po

        # - - - - - - - - - - - -
        # Accounts configuration
        # - - - - - - - - - - - -

        # account.account -> Bank
        # but check on wallet
        if po_journal.is_wallet:
            acct_acct_bank_credit = (
                po_journal.main_bank_account_id.default_credit_account_id
            )
        else:
            acct_acct_bank_credit = po_journal.default_credit_account_id
        # end if

        if not acct_acct_bank_credit:
            raise UserError(
                f'Conto "avere" non configurato per non configurato per '
                f"sezionale di banca "
                f"{po_journal.display_name} ({po_journal.code})"
            )
        # end if

        # account.account -> Expenses
        acct_acct_expe = self.env["account.account"].browse(expenses_account_id)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Creazione registrazione contabile (account.move)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # La registrazione contabile viene creata una modalità che
        # permette squadrature durante la sua manipolazione.
        # L'utilizzo di questa modalità è necessario per facilitare
        # la procedura di creazione di una nuova riconciliazione
        new_move = self.env["account.move"].create(
            {
                "type": "entry",
                "date": fields.Date.today(),
                "journal_id": po_journal.id,
                "state": "draft",
                "ref": "Insoluto",
            }
        )

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Eventuali costi bancari
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if expenses_account_id and expenses_amount > 0:

            if charge_client:
                # Spread expenses amount equally among the lines.
                # Avoid rounding problem by adjusting the amount
                # of the last line processed
                per_client_amount = round(expenses_amount / len(self), float_precision)
                charge_client_for = [per_client_amount] * len(self)

                # Manage the difference between rounded spread costs
                # and original cost
                charge_client_for_sum = round(
                    per_client_amount * len(self), float_precision
                )
                remain = round(expenses_amount - charge_client_for_sum, float_precision)
                charge_client_for[-1] = round(
                    charge_client_for[-1] + remain, float_precision
                )

            else:
                # Client is not charged for expenses,
                # just add two new move lines

                # Line reconcile must be changed
                new_reconcile_needed = True

                # Banca c/c
                # bank_account_line =

                move_line_model_no_check.create(
                    {
                        "move_id": new_move.id,
                        "account_id": acct_acct_bank_credit.id,
                        "debit": 0,
                        "credit": expenses_amount,
                    }
                )

                # Spese bancarie
                # expenses_account_line =

                move_line_model.create(
                    {
                        "move_id": new_move.id,
                        "account_id": acct_acct_expe.id,
                        "debit": expenses_amount,
                        "credit": 0,
                    }
                )
            # end if
        else:
            new_reconcile_needed = True
        # end if

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Clienti e nuova riconciliazione
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        for move_line, expenses_charged in zip(self, charge_client_for):

            # Update the total amount of insoluti
            amount_insoluti = amount_insoluti + move_line.amount_into_payment_line

            # Increase the unpaid counter for this line
            move_line.unpaid_ctr = move_line.unpaid_ctr + 1

            # account.account -> Partner
            acct_acct_partner = move_line.account_id

            # New move line for the client
            my_invoice = move_line.invoice_id

            insoluto_move_line = move_line_model_no_check.create(
                {
                    "move_id": new_move.id,
                    "account_id": acct_acct_partner.id,
                    "partner_id": my_invoice.partner_id.id,
                    "debit": move_line.amount_into_payment_line + expenses_charged,
                    "credit": 0,
                    "name": str(
                        f"Scadenza {move_line.date_maturity}"
                        " - "
                        f'Fattura {my_invoice.name or my_invoice.number}'
                    ),
                }
            )

            # - - - - - - - - - - - - - - - - - - - - - - - -
            # Modify invoices reconciliation if needed
            # - - - - - - - - - - - - - - - - - - - - - - - -
            if new_reconcile_needed:

                # Ottenimento riga riconciliata con move_line
                reconcile_line_list = move_line.full_reconcile_id.reconciled_line_ids

                # Eliminazione riconciliazione
                move_line.remove_move_reconcile()

                # se tra i movimenti non più riconciliati ne trovo ancora
                if len(reconcile_line_list) > 2:
                    reconcile_line_list = reconcile_line_list.filtered(
                        lambda x: x.reconciled is False
                    )

                if reconcile_line_list:
                    if reconcile_line_list[0].id != move_line.id:
                        reconcile_line = reconcile_line_list[0]
                    else:
                        reconcile_line = reconcile_line_list[1]
                    # end if

                    # Creeazione recordset con righe da riconciliare
                    self.browse([insoluto_move_line.id, reconcile_line.id]).reconcile()
            # end if
        # end for

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Totale in Banca c/c
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        registered_expenses_amount = round(sum(charge_client_for), float_precision)

        # This time let's use the "normal" account.move.line model so the
        # program can automatically verify the account.move is balanced
        move_line_model.create(
            {
                "move_id": new_move.id,
                "account_id": acct_acct_bank_credit.id,
                "debit": 0,
                "credit": amount_insoluti + registered_expenses_amount,
            }
        )

        lines = self.env["account.move.line"].browse(self._context["active_ids"])
        # reset flag
        lines.write(
            {
                "incasso_effettuato": False,
            }
        )

    # end registra_insoluto_standard

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PAYMENT CONFIRM
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @api.multi
    def open_wizard_payment_confirm(self):

        # Retrieve the lines
        lines = self.env["account.move.line"].browse(self._context["active_ids"])

        # Controlli
        validate_selection.payment_confirm(lines)

        # Apertura wizard
        return {
            "type": "ir.actions.act_window",
            "name": "Conferma pagamento",
            "res_model": "wizard.payment.order.confirm",
            "view_type": "form",
            "view_mode": "form",
            "view_id": self.env.ref(
                "account_banking_common.wizard_payment_order_confirm"
            ).id,
            "target": "new",
            "res_id": False,
            "context": {"active_ids": self._context["active_ids"]},
            "binding_model_id": "account.model_account_move_line",
        }

    # end validate_payment_confirm

    @api.multi
    def registra_incasso(self):

        # The payment method of the selected lines
        p_method = self.get_payment_method()

        raise UserError(
            f"Procedura di registrazione d'incasso non definita "
            f"per il metodo di pagamento {p_method.name}"
        )

    # end registra_incasso

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Metodi di utilità
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @api.multi
    def get_payment_method(self):
        return validate_selection.same_payment_method(self)

    # end get_payment_method_code

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ORDER GENERATE
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @api.multi
    def open_wizard_payment_order_generate(self):

        # Retrieve the records
        lines = self.env["account.move.line"].browse(self._context["active_ids"])
        # Perform validations
        payment_method = False

        if len(lines) > 0:
            for line in lines:
                payment_method = line.payment_method
                break
        if payment_method:
            if payment_method.code == "invoice_financing":
                banks = defaultdict(lambda: {"count": 0, "name": None})
                msg = (
                    "ATTENZIONE!\nSono state selezionate righe di scadenze"
                    " che non hanno lo stesso conto per "
                    "la banca aziendale.\n\n "
                )

                for line in lines:
                    if line.move_id.company_bank_id.id:
                        invoice_bank_id = line.move_id.company_bank_id.id
                        invoice_bank_name = line.move_id.company_bank_id.bank_name

                        banks[invoice_bank_id]["count"] += 1
                        banks[invoice_bank_id]["name"] = invoice_bank_name
                    else:
                        fattura = line.stored_invoice_id.number
                        raise UserError(
                            "ATTENZIONE!\nConto bancario aziendale "
                            "nella testata di registrazione "
                            "{fattura} non impostato.".format(fattura=fattura)
                        )
                    # end if

                # end for

                error_banks = len(banks) > 1
                if error_banks:
                    raise UserError(msg)
                # end if
            # end if
        # end if

        # Open the wizard
        model = "account_banking_common"
        wiz_view = self.env.ref(model + ".wizard_account_payment_generate")
        return {
            "type": "ir.actions.act_window",
            "name": "Genera Distinta",
            "res_model": "wizard.account.payment.generate",
            "view_type": "form",
            "view_mode": "form",
            "view_id": wiz_view.id,
            "target": "new",
            "res_id": False,
            "binding_model_id": model + ".model_account_move_line",
            "context": {"active_ids": self._context["active_ids"]},
        }

    # end open_wizard_payment_order_generate

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ADD LINES TO ORDER
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @api.multi
    def open_wizard_payment_order_add_move_lines(self):

        # Retrieve the records
        lines = self.env["account.move.line"].browse(self._context["active_ids"])

        # Perform validations
        payment_method = False

        if len(lines) > 0:
            for line in lines:
                payment_method = line.payment_method
                break
        if payment_method:
            if payment_method.code == "invoice_financing":
                banks = defaultdict(lambda: {"count": 0, "name": None})
                msg = (
                    "ATTENZIONE!\nSono state selezionate righe di fatture"
                    " che non hanno la stessa banca.\n\n "
                )

                for line in lines:
                    if line.move_id.company_bank_id.id:
                        invoice_bank_id = line.move_id.company_bank_id.id
                        invoice_bank_name = line.move_id.company_bank_id.bank_name

                        banks[invoice_bank_id]["count"] += 1
                        banks[invoice_bank_id]["name"] = invoice_bank_name
                    else:
                        fattura = line.stored_invoice_id.number
                        raise UserError(
                            "ATTENZIONE!\nConto bancario aziendale "
                            "nella fattura {fattura} non "
                            "impostato.".format(fattura=fattura)
                        )
                    # end if

                # end for
                error_banks = len(banks) > 1
                if error_banks:
                    raise UserError(msg)
                # end if

            # end if
        # end if

        # Open the wizard
        model = "account_banking_common"
        wiz_view = self.env.ref(model + ".wizard_account_payment_add_move_line")
        return {
            "type": "ir.actions.act_window",
            "name": "Aggiungi a distinta",
            "res_model": "wizard.account.payment.add.move.lines",
            "view_type": "form",
            "view_mode": "form",
            "view_id": wiz_view.id,
            "target": "new",
            "res_id": False,
            "binding_model_id": model + ".model_account_move_line",
            "context": {"active_ids": self._context["active_ids"]},
        }

    # end open_wizard_payment_order_generate

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # UPDATE PAYMENT METHOD
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @api.multi
    def open_wizard_set_payment_method(self):
        busy_lines = []
        # Retrieve the records
        lines = self.env["account.move.line"].browse(self._context["active_ids"])

        if len(lines) > 0:
            for line in lines:
                # Detect lines already assigned to a payment order
                if line.payment_line_ids:
                    busy_lines.append(line)

            error_busy = len(busy_lines) > 0
            if error_busy:
                msg = (
                    "ATTENZIONE!\nLe seguenti righe "
                    "sono già parte di una distinta:\n\n - "
                )

                msg += "\n - ".join(
                    map(
                        lambda x: x.invoice_id.number + "    " + str(x.date_maturity),
                        busy_lines,
                    )
                )
                raise UserError(msg)
            # end if

        # Open the wizard
        model = "account_banking_common"
        wiz_view = self.env.ref(model + ".wizard_set_payment_method")
        return {
            "type": "ir.actions.act_window",
            "name": "Aggiorna metodi di pagamento",
            "res_model": "wizard.set.payment.method",
            "view_type": "form",
            "view_mode": "form",
            "view_id": wiz_view.id,
            "target": "new",
            "res_id": False,
            "binding_model_id": model + ".model_account_move_line",
            "context": {"active_ids": self._context["active_ids"]},
        }

    # end open_wizard_set_payment_method

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # DUEDATES COMPENSATE
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    @api.multi
    def open_wizard_duedate_compensate(self):
        # Retrieve the records
        lines = self.env["account.move.line"].browse(self._context["active_ids"])

        # at least 2 records
        if len(lines) < 2:
            raise UserError("Per la compensazione selezionare almeno " "due scadenze.")

        # free duedates
        busy_lines = list()
        if len(lines) > 0:
            for line in lines:
                # Detect lines already assigned to a payment order
                if line.payment_line_ids:
                    busy_lines.append(line)

            error_busy = len(busy_lines) > 0
            if error_busy:
                msg = (
                    "ATTENZIONE!\nLe seguenti scadenze "
                    "sono già parte di una distinta:\n\n - "
                )

                msg += "\n - ".join(
                    map(
                        lambda x: x.invoice_id.number + "    " + str(x.date_maturity),
                        busy_lines,
                    )
                )
                raise UserError(msg)

        # not reconciled duedates
        recon_lines = list()
        if len(lines) > 0:
            for line in lines:
                # Detect lines already reconciled
                if line.reconciled:
                    recon_lines.append(line)

            error_recon = len(recon_lines) > 0
            if error_recon:
                msg = (
                    "ATTENZIONE!\nLe seguenti scadenze "
                    "sono state riconciliate:\n\n - "
                )

                msg += "\n - ".join(
                    map(
                        lambda x: x.invoice_id.number + "    " + str(x.date_maturity),
                        recon_lines,
                    )
                )
                raise UserError(msg)

        # same partner
        partners = list()
        accounts = list()
        debit_amount = 0
        credit_amount = 0

        for line in lines:
            if line.partner_id:
                if line.partner_id.id not in partners:
                    partners.append(line.partner_id.id)
                # end if
            # end if

            if line.account_id:
                if line.account_id.id not in accounts:
                    accounts.append(line.account_id.id)

                if line.account_id.user_type_id.type not in ("payable", "receivable"):
                    raise UserError(
                        "Sono compensabili solo i conti di " "debito/credito!"
                    )
                # end if
            # end if
            debit_amount += line.debit
            credit_amount += line.credit
        # end for

        if len(partners) > 1:
            raise UserError(
                "Per la compensazione le scadenze devono avere " "lo stesso partner."
            )

        # difference between credit and debit
        if debit_amount == 0 or credit_amount == 0:
            raise UserError("Non sono state selezonate partite di storno!")

        ctx = dict()
        ctx["active_ids"] = self._context["active_ids"]
        ctx["same_account"] = True if len(accounts) < 2 else False

        # Open the wizard
        model = "account_banking_common"
        wiz_view = self.env.ref(model + ".wizard_account_compensation_generate")
        return {
            "type": "ir.actions.act_window",
            "name": "Compensazione",
            "res_model": "wizard.account.compensation.generate",
            "view_type": "form",
            "view_mode": "form",
            "view_id": wiz_view.id,
            "target": "new",
            "res_id": False,
            "binding_model_id": model + ".model_account_move_line",
            "context": ctx,
        }

    # end open_wizard_duedate_compensate

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PAYMENT REGISTER
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    @api.multi
    def open_wizard_register_payment(self):
        # Retrieve the records
        lines = self.env["account.move.line"].browse(self._context["active_ids"])

        # free duedates
        busy_lines = list()
        if len(lines) > 0:
            for line in lines:
                # Detect lines already assigned to a payment order
                if line.payment_line_ids:
                    busy_lines.append(line)

            error_busy = len(busy_lines) > 0
            if error_busy:
                msg = (
                    "ATTENZIONE!\nLe seguenti scadenze "
                    "sono già parte di una distinta:\n\n - "
                )

                msg += "\n - ".join(
                    map(
                        lambda x: x.invoice_id.number + "    " + str(x.date_maturity),
                        busy_lines,
                    )
                )
                raise UserError(msg)

        # not reconciled duedates
        recon_lines = list()
        if len(lines) > 0:
            for line in lines:
                # Detect lines already reconciled
                if line.reconciled:
                    recon_lines.append(line)

            error_recon = len(recon_lines) > 0
            if error_recon:
                msg = (
                    "ATTENZIONE!\nLe seguenti scadenze "
                    "sono state riconciliate:\n\n - "
                )

                for ln in recon_lines:
                    if ln.invoice_id:
                        msg += ln.invoice_id.number + " "
                    else:
                        msg += ln.display_name + " "

                    if ln.date_maturity:
                        msg += str(ln.date_maturity)
                    msg += "\n - "

                raise UserError(msg)

        # same company bank account
        bank_lines = list()
        bank_ids = list()
        if len(lines) > 0:
            for line in lines:
                # Detect lines already reconciled
                if line.company_bank_id.id:
                    if line.company_bank_id.id not in bank_ids:
                        bank_ids.append(line.company_bank_id.id)
                        bank_lines.append(line)

            error_bank = len(bank_ids) > 1
            if error_bank:
                msg = (
                    "ATTENZIONE!\nLe seguenti scadenze "
                    "hanno conti bancari diversi:\n\n - "
                )

                msg += "\n - ".join(
                    map(
                        lambda x: x.invoice_id.number + "    " + str(x.date_maturity),
                        bank_lines,
                    )
                )
                raise UserError(msg)

        bank_lines = list()
        if len(lines) > 0:
            for line in lines:
                # Detect lines already reconciled
                if line.company_bank_id.id:
                    if line.company_bank_id.bank_is_wallet is True:
                        bank_lines.append(line)
                    # end if
                # end if
            # end for
            error_bank = len(bank_lines) > 0
            if error_bank:
                msg = (
                    "ATTENZIONE!\nLe seguenti scadenze "
                    "hanno conti bancari di portafoglio:\n\n - "
                )

                msg += "\n - ".join(
                    map(
                        lambda x: x.invoice_id.number + "    " + str(x.date_maturity),
                        bank_lines,
                    )
                )
                raise UserError(msg)

        partner_lines = list()
        partner_ids = list()
        if len(lines) > 0:

            for line in lines:
                # Detect lines already reconciled
                if (
                    line.partner_id
                    and line.partner_id.id
                    and (line.partner_id.id not in partner_ids)
                ):
                    partner_ids.append(line.partner_id.id)
                    partner_lines.append(line)
                # end if
            # end for
            error_partner = len(partner_ids) > 1
            if error_partner:
                msg = (
                    "ATTENZIONE!\nLe seguenti scadenze " "hanno partner diversi:\n\n - "
                )

                msg += "\n - ".join(
                    map(
                        lambda x: x.invoice_id.number + "    " + str(x.date_maturity),
                        partner_lines,
                    )
                )
                raise UserError(msg)
        # Open the wizard
        model = "account_banking_common"
        wiz_view = self.env.ref(model + ".wizard_account_register_payment")
        return {
            "type": "ir.actions.act_window",
            "name": "Registra pagamento",
            "res_model": "wizard.account.register.payment",
            "view_type": "form",
            "view_mode": "form",
            "view_id": wiz_view.id,
            "target": "new",
            "res_id": False,
            "binding_model_id": model + ".model_account_move_line",
            "context": {"active_ids": self._context["active_ids"]},
        }

    # end open_wizard_register_payment
