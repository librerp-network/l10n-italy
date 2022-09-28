# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2021-22 librERP enterprise network <https://www.librerp.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Gestione Cespiti',
    'version': '12.0.1.0.0_29',
    'category': 'Localization/Italy',
    'summary': "Gestione Cespiti",
    'author': 'Openforce, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/assets_management',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_cancel',
        'account_financial_report',
        'account_fiscal_year',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'security/rules.xml',
        'data/ir_cron.xml',
        'data/asset_data.xml',
        'data/asset_journal_data.xml',
        'report/layout.xml',
        'report/paperformat.xml',
        'report/templates/asset_journal.xml',
        'report/templates/asset_previsional.xml',
        'report/reports.xml',
        'views/action_client.xml',
        'views/asset_menuitems.xml',
        'views/account_invoice.xml',
        'views/account_move.xml',
        'views/asset.xml',
        'views/asset_accounting_info.xml',
        'views/asset_category.xml',
        'views/asset_depreciation.xml',
        'views/asset_depreciation_line.xml',
        'views/asset_depreciation_line_type.xml',
        'views/asset_depreciation_mode.xml',
        'views/asset_depreciation_type.xml',
        'views/asset_tag.xml',
        'wizard/account_invoice_manage_asset_view.xml',
        'wizard/account_move_manage_asset_view.xml',
        'wizard/asset_generate_depreciation_view.xml',
        'wizard/asset_journal_report_view.xml',
        'wizard/asset_previsional_report_view.xml',
        'wizard/asset_generate_warning_view.xml',
        'wizard/asset_generate_open_view.xml',

    ],
    'development_status': 'Beta',
    'installable': True,
}
