from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    if not version:
        return  # No version means it's an installation, not an upgrade

    # Execute SQL
    cr.execute("""
        ALTER TABLE res_partner DROP CONSTRAINT res_partner_rea_code_uniq;
    """)
