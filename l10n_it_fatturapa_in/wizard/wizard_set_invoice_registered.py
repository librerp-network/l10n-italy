# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class WizardSetInvoiceRegistered(models.TransientModel):
    _name = "wizard.set.invoice.registered"

    @api.multi
    def set_registered(self):
        for row_id in self.env.context.get('active_ids', []):
            self.env['fatturapa.attachment.in'].browse(row_id).registered = True
