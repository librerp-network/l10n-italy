# Copyright 2016 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl
# Copyright 2021 Antonio M. Vigliotti - SHS-Av srl
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from odoo import fields, models


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    # rc_type_id = fields.Many2one('account.rc.type', 'RC Type')

    rc_type = fields.Selection(
        selection=[
            ('', 'No RC'),
            ('local', 'RC locale'),
            ('self', 'RC con autofattura'),
        ],
        string='Reverse charge',
        default='',
    )

    partner_type = fields.Selection(
        selection=[
            ('supplier', 'Fornitore'),
            ('other', 'Altro')
        ],
        string='Tipo di Partner',
        default='',
    )

    rc_sale_tax_id = fields.Many2one(
        comodel_name='account.tax',
        string='Conto RC di vendita',
        domain=[('type_tax_use', '=', 'sale')],
    )
