# Copyright 2021 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import datetime, date
from calendar import isleap

# from odoo import fields
from odoo.tools.float_utils import float_round
from odoo.tools.safe_eval import safe_eval
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError

# from dateutil.relativedelta import relativedelta


class TestAssets(TransactionCase):
    def setUp(self):
        super().setUp()
        self.data_account_type_current_assets = self.env.ref(
            "account.data_account_type_current_assets"
        )
        self.data_account_type_current_liabilities = self.env.ref(
            "account.data_account_type_current_liabilities"
        )
        account_model = self.env["account.account"]
        self.account_fixed_assets = account_model.search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_fixed_assets").id,
                )
            ],
            limit=1,
        )[0]
        self.account_depreciation = account_model.search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_expenses").id,
                ),
                ("name", "ilike", "Expenses"),
            ],
        )[-1]
        self.account_fund = account_model.search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_non_current_assets").id,
                )
            ],
            limit=1,
        )[0]
        self.account_gain = account_model.search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_revenue").id,
                )
            ],
            limit=1,
        )[0]
        self.account_loss = account_model.search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_expenses").id,
                )
            ],
            limit=1,
        )[0]
        self.journal = self.env["account.journal"].search([("code", "=", "ADJ")])[0]

        self.asset_category_1 = self._create_category(1)
        self.asset_category_2 = self._create_category(2)
        self.asset_1 = self._create_asset(1)
        self.asset_2 = self._create_asset(2)
        for year in range(date.today().year - 2, date.today().year + 1):
            self.env["account.fiscal.year"].create(
                {
                    "name": "%s" % year,
                    "date_from": date(year, 1, 1),
                    "date_to": date(year, 12, 31),
                }
            )

    # TODO> Remove before publish final code
    def tearDown(self):
        super().tearDown()
        self.env.cr.commit()  # pylint: disable=invalid-commit

    def envtest_wizard_start_by_act_name(
        self, module, action_name, default=None, ctx=None
    ):
        """Start a wizard from an action name.
        It validates the action name from xml view file, then calls envtest_wizard_start

        Example.

        XML view file:
            <record id="action_example" model="ir.actions.act_window">
                <field name="name">Example</field>
                <field name="res_model">wizard.example</field>
                [...]
            </record>

        Python code:
            ir_action = self.envtest_wizard_start_by_act_name(
                "module_example",   # Module name
                "action_example",   # Action name from xml file
            )
        """
        act_model = "ir.actions.act_window"
        ir_action = self.env[act_model].for_xml_id(module, action_name)
        return self.envtest_wizard_start(ir_action, default=default, ctx=ctx)

    def envtest_wizard_start(self, ir_action, default=None, ctx=None):
        """Start a wizard from an action.
        This function simulates web interface wizard starting; it serves to test:
        * view names
        * wizard structure
        """
        res_model = ir_action["res_model"]
        vals = default or {}
        wizard = self.env[res_model].create(vals)
        ir_action["res_id"] = wizard.id
        if isinstance(ir_action.get("context"), str):
            ir_action["context"] = safe_eval(ir_action["context"])
        if ctx:
            if isinstance(ir_action.get("context"), dict):
                ir_action["context"].update(ctx)
            else:
                ir_action["context"] = ctx
        if ir_action.get("view_id"):
            self.env["ir.ui.view"].browse(ir_action["view_id"][0])
        return ir_action

    def envtest_wizard_edit(self, wizard, field, value, onchange=None):
        """Simulate view editing of a field.
        It called with triple (field_name, value, onchange function)
        This function is called by envtest_wizard_exec on web_changes parameter
        """
        setattr(wizard, field, value)
        if onchange:
            return getattr(wizard, onchange)()

    def envtest_wizard_exec(
        self, ir_action, button_name=None, web_changes=None, button_ctx=None
    ):
        """Simulate wizard execution from an action.
        Wizard is created by action values.
        Onchange can be called by web_changes parameter.
        At the end the <button_name> function is executed.
        It returns the wizard result or False.

        Python example:
            act_window = self.envtest_wizard_exec(
                act_window,
                button_name="do_something",
                web_changes=[
                    ("field_a_ids", [(6, 0, [value_a.id])], "onchange_field_a"),
                    ("field_b_id", self.b.id, "onchange_field_b"),
                    ("field_c", "C"),
                ],
            )
        """
        res_model = ir_action['res_model']
        ctx = safe_eval(ir_action.get('context')) if isinstance(
            ir_action.get('context'),
            str) else ir_action.get('context', {})
        if isinstance(ctx.get("active_id"), int):
            wizard = self.env[res_model].with_context(ctx).browse(ctx['active_id'])
        elif ctx.get("active_id"):
            wizard = ctx['active_id']
        elif isinstance(ir_action.get("res_id"), int):
            wizard = self.env[res_model].with_context(ctx).browse(ir_action['res_id'])
        else:
            raise (TypeError, "Invalid object/model")

        for default_value in [x for x in ctx.keys() if x.startswith("default_")]:
            field = default_value[8:]
            setattr(wizard, field, ctx[default_value])
        for field in wizard._onchange_methods.values():
            for method in field:
                getattr(wizard, method.__name__)()
        web_changes = web_changes or []
        for args in web_changes:
            method = args[2] if len(args) > 2 else None
            self.envtest_wizard_edit(wizard, args[0], args[1], method)
            if not method and args[0] in wizard._onchange_methods:
                for method in wizard._onchange_methods[args[0]]:
                    getattr(wizard, method.__name__)()
        button_name = button_name or 'process'
        if hasattr(wizard, button_name):
            act = getattr(wizard, button_name)()
            if isinstance(act, dict) and act.get('type') != '':
                act.setdefault('type', 'ir.actions.act_window_close')
                if isinstance(button_ctx, dict):
                    act.setdefault("context", button_ctx)
            return act
        return False

    def envtest_is_action(self, ir_action):
        return isinstance(ir_action, dict) and ir_action.get(
            "type", "ir.actions.act_window") in ("ir.actions.act_window",
                                                 "ir.actions.client")

    def _create_category(self, cat_nr):
        vals = {
            "name": "Asset category #%s" % cat_nr,
            "asset_account_id": self.account_fixed_assets.id,
            "depreciation_account_id": self.account_depreciation.id,
            "fund_account_id": self.account_fund.id,
            "gain_account_id": self.account_gain.id,
            "loss_account_id": self.account_loss.id,
        }
        if cat_nr == 1:
            vals["journal_id"] = self.env.ref(
                "assets_management.asset_account_journal"
            ).id
        category = self.env["asset.category"].create(vals)
        type_model = self.env["asset.category.depreciation.type"]
        for rec in type_model.search([("category_id", "=", category.id)]):
            if cat_nr == 1:
                rec.write(
                    {
                        "percentage": 25,
                        "pro_rata_temporis": False,
                        "mode_id": self.env.ref(
                            "assets_management.ad_mode_materiale"
                        ).id,
                    }
                )
            elif cat_nr == 2:
                rec.write(
                    {
                        "percentage": 24,
                        "pro_rata_temporis": True,
                        "mode_id": self.env.ref(
                            "assets_management.ad_mode_immateriale"
                        ).id,
                    }
                )
        return category

    def _create_asset(self, asset_nr):
        vals = {
            "name": "Test asset #%s" % asset_nr,
            "category_id": self.asset_category_1.id
            if asset_nr == 1
            else self.asset_category_2.id,
            "currency_id": self.env.ref("base.main_company").currency_id.id,
            "purchase_amount": 1000.0 if asset_nr == 1 else 2500,
            "purchase_date": date(date.today().year - 2, 12, 1)
            if asset_nr == 1
            else date(date.today().year - 2, 10, 1),
        }
        if asset_nr == 1:
            vals["company_id"] = self.env.ref("base.main_company").id
            vals["code"] = "One"
        return self.env["asset.asset"].create(vals)

    def day_rate(self, date_from, date_to, is_leap=None):
        return ((date_to - date_from).days + 1) / (365 if not is_leap else 366)

    def get_depreciation_lines(
        self, asset=None, move_type=None, date_from=None, date_to=None
    ):
        dep_line_model = self.env["asset.depreciation.line"]
        move_type = move_type or "depreciated"
        domain = [("move_type", "=", move_type)]
        if asset:
            domain.append(("asset_id", "=", asset.id))
        if date_from:
            if isinstance(date_from, date):
                date_from = date_from.strftime("%Y-%m-%d")
            domain.append(("date", ">=", date_from))
        if date_to:
            if isinstance(date_to, date):
                date_to = date_to.strftime("%Y-%m-%d")
            domain.append(("date", "<=", date_to))
        return dep_line_model.search(domain)

    def _test_depreciation_line(
        self, date_dep, dep, asset, amount=None, depreciation_nr=None, final=None
    ):
        if amount:
            self.assertEqual(
                float_round(dep.amount, 2),
                float_round(amount, 2),
                "Invalid depreciation amount!",
            )
        self.assertEqual(dep.asset_id, asset, "Invalid asset id!")
        self.assertEqual(dep.date, date_dep, "Invalid date!")
        if depreciation_nr:
            self.assertEqual(
                dep.depreciation_nr, depreciation_nr, "Invalid depreciation number!"
            )
        if final is not None:
            self.assertEqual(dep.final, final, "Invalid final flag!")

    def _test_all_depreciation_lines(
        self,
        date_dep,
        asset,
        amount=None,
        depreciation_nr=None,
        final=None,
        no_test_ctr=None,
    ):
        ctr = 0
        for dep in self.get_depreciation_lines(asset=asset, date_from=date_dep):
            self._test_depreciation_line(
                date_dep,
                dep,
                asset,
                amount=amount,
                depreciation_nr=depreciation_nr,
                final=final,
            )
            ctr += 1
        if not no_test_ctr:
            self.assertEqual(
                ctr, len(asset.depreciation_ids), "Missed depreciation move!"
            )

    def _test_wizard_depreciation(self, final):
        year = date.today().year - 2
        date_dep = date(year, 12, 31)
        vals = {
            "date_dep": datetime.strftime(date_dep, "%Y-%m-%d"),
            "final": final,
        }
        ir_action = self.envtest_wizard_start_by_act_name(
            "assets_management",
            "action_wizard_asset_generate_depreciation",
            default=vals,
            ctx={} if final else {"reload_window": True},
        )
        act_window = self.envtest_wizard_exec(ir_action, button_name="do_warning")
        self.assertTrue(self.envtest_is_action(act_window))
        if final:
            self.assertEqual(
                act_window["res_model"],
                "asset.generate.warning",
                "Invalid response for 'Final depreciations'"
            )
            self.envtest_wizard_exec(act_window, button_name="do_generate")
        self._test_all_depreciation_lines(
            date_dep,
            self.asset_1,
            amount=125.0,
            depreciation_nr=1,
            final=final,
        )
        depreciation_amount = 150.82 if isleap(year) else 151.23
        self._test_all_depreciation_lines(
            date_dep,
            self.asset_2,
            amount=depreciation_amount,
            depreciation_nr=1,
            final=final,
        )

    def _test_asset_1(self):
        # Basic test #1
        #
        # We test 3 years depreciations of 1000.0€ asset #1:
        # Test (setup)   : Test (A1)          | Test (A2)         | Test (A3)
        # (year-2)-10-01 : (year-2)-12-31     | (year-1)-12-31    | Today
        # start -> 1000€ : depr.50% -> 125.0€ | depr.100% -> 250€ | depr -> 0..250.0€
        #
        asset = self.asset_1
        self.assertEqual(
            asset.state, "non_depreciated", "Asset is not in non depreciated state!"
        )

        wiz_vals = asset.with_context(
            {"allow_reload_window": True}
        ).launch_wizard_generate_depreciations()
        wiz = (
            self.env["wizard.asset.generate.depreciation"]
            .with_context(wiz_vals["context"])
            .create({})
        )

        deps_amount = {}
        # (A1) Year #1: Generate 50% depreciation -> 1000.00€ * 25% * 50% = 125.0€
        year = date.today().year - 2
        wiz.date_dep = date(year, 12, 31)
        wiz.do_generate()
        self.assertEqual(
            asset.state,
            "partially_depreciated",
            "Asset is not in non depreciated state!",
        )
        self._test_all_depreciation_lines(
            wiz.date_dep, asset, amount=125.0, depreciation_nr=1, final=False
        )
        for dep in asset.depreciation_ids:
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                125.0,
                "Invalid depreciation amount!",
            )
            if dep not in deps_amount:
                deps_amount[dep] = dep.amount_depreciated

        # (A2) Year #2: Depreciation amount is 250€ (1000€ * 25%)
        year = date.today().year - 1
        wiz.date_dep = date(year, 12, 31)
        wiz.do_generate()
        self._test_all_depreciation_lines(
            wiz.date_dep, asset, amount=250.0, depreciation_nr=2, final=False
        )
        for dep in asset.depreciation_ids:
            deps_amount[dep] += 250.0
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                float_round(deps_amount[dep], 2),
                "Invalid depreciation amount!",
            )

        # (A3) Year #3: Current depreciation amount depends on today
        wiz.date_dep = date.today()
        year = wiz.date_dep.year
        rate = self.day_rate(date(year, 1, 1), wiz.date_dep, is_leap=isleap(year))
        wiz.do_generate()
        depreciation_amount = 250.0 * rate
        self._test_all_depreciation_lines(
            wiz.date_dep, asset,
            amount=depreciation_amount, depreciation_nr=3, final=False
        )
        for dep in asset.depreciation_ids:
            deps_amount[dep] += depreciation_amount
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                float_round(deps_amount[dep], 2),
                "Invalid depreciation amount!",
            )
        # (A3.b) Year #3: Repeat depreciation, prior data will be removed
        wiz.date_dep = date(date.today().year, 12, 31)
        wiz.do_generate()
        self._test_all_depreciation_lines(
            wiz.date_dep, asset, amount=250.0, depreciation_nr=3, final=False
        )
        for dep in asset.depreciation_ids:
            deps_amount[dep] -= depreciation_amount
            deps_amount[dep] += 250.0
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                float_round(deps_amount[dep], 2),
                "Invalid depreciation amount!",
            )
        # (A3.c) Year #3: Repeat depreciation
        # One day depreciation -> 1000.00€ * 25% * / 365 = 0,68€
        wiz.date_dep = date(date.today().year, 1, 1)
        wiz.do_generate()
        self._test_all_depreciation_lines(
            wiz.date_dep, asset, amount=0.68, depreciation_nr=3, final=False
        )
        for dep in asset.depreciation_ids:
            deps_amount[dep] -= 250.0
            deps_amount[dep] += 0.68
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                float_round(deps_amount[dep], 2),
                "Invalid depreciation amount!",
            )
        # (A4) Special test: cannot generate depreciation on (year-2)
        year = date.today().year - 2
        wiz.date_dep = date(year, 12, 31)
        with self.assertRaises(ValidationError):
            wiz.do_generate()

    def _test_asset_2(self):
        # Basic test #2
        #
        # We test 3 years depreciations of 2500.0€ asset #2:
        # Test (setup)   : Test (B1)         | Test (B2)         | Test (B3)
        # (year-2)-10-01 : (year-2)-12-31    | (year-1)-12-31    | Today
        # start -> 2500€ : 92/365 -> 150.82€ | depr.100% -> 600€ | depr -> 0..600.0€
        #
        asset = self.asset_2
        self.assertEqual(
            asset.state, "non_depreciated", "Asset is not in non depreciated state!"
        )

        wiz_vals = asset.with_context(
            {"allow_reload_window": True}
        ).launch_wizard_generate_depreciations()
        wiz = (
            self.env["wizard.asset.generate.depreciation"]
            .with_context(wiz_vals["context"])
            .create({})
        )

        deps_amount = {}
        # Year #1: Generate 92 days depreciation -> 2500.00€ * 24% * 92 / 365 = 151.23€
        # If year - 2 is leap depreciation value is 150.82€
        year = date.today().year - 2
        wiz.date_dep = date(year, 12, 31)
        wiz.do_generate()
        depreciation_amount = 150.82 if isleap(year) else 151.23
        self.assertEqual(
            asset.state,
            "partially_depreciated",
            "Asset is not in non depreciated state!",
        )
        self._test_all_depreciation_lines(
            wiz.date_dep, asset,
            amount=depreciation_amount, depreciation_nr=1, final=False
        )
        for dep in asset.depreciation_ids:
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                depreciation_amount,
                "Invalid depreciation amount!",
            )
            if dep not in deps_amount:
                deps_amount[dep] = dep.amount_depreciated

        # Year #2: Depreciation amount is 600€ (2500€ * 24%)
        year = date.today().year - 1
        wiz.date_dep = date(year, 12, 31)
        wiz.do_generate()
        self._test_all_depreciation_lines(
            wiz.date_dep, asset, amount=600.0, depreciation_nr=2, final=False
        )
        for dep in asset.depreciation_ids:
            deps_amount[dep] += 600.0
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                float_round(deps_amount[dep], 2),
                "Invalid depreciation amount!",
            )

        # Year #3: Current depreciation amount depends on today: value is <= 600€
        wiz.date_dep = date.today()
        year = wiz.date_dep.year
        rate = self.day_rate(date(year, 1, 1), wiz.date_dep, is_leap=isleap(year))
        wiz.do_generate()
        depreciation_amount = 600.0 * rate
        self._test_all_depreciation_lines(
            wiz.date_dep, asset,
            amount=depreciation_amount, depreciation_nr=3, final=False
        )
        for dep in asset.depreciation_ids:
            deps_amount[dep] += depreciation_amount
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                float_round(deps_amount[dep], 2),
                "Invalid depreciation amount!",
            )

    def _test_asset_3(self):
        # Out + Dismiss tests asset #1
        #
        # Current depreciable amount is 1000.0€ * 25% = 250.0€
        # Prior test (A1) | Test (C3) 90-91 days : Test (C2)      : (C4) 275 days
        # (year-2)-03-31  | (year-1)-03-31       : (year-1)-03-31 : (year-1)-12-31
        #                 | Depr.ble = 250.0€    : Depr.ble amt 275.0€ * 25% = 68.75€
        # depr. 125.0€    | depr -> 61.64€       : 'out' -> -725€ : depr -> 51.80€
        #
        # (C2) Asset #1, year #2: depreciation moves removed, then value will be reduced
        asset = self.asset_1
        year = date.today().year - 1
        self.get_depreciation_lines(asset=asset, date_from=date(year, 12, 31)).unlink()
        down_value = 725.0
        dep_line_model = self.env["asset.depreciation.line"]
        for dep in asset.depreciation_ids:
            vals = {
                "amount": down_value,
                "asset_id": asset.id,
                "depreciation_line_type_id": self.env.ref(
                    "assets_management.adpl_type_sva"
                ).id,
                "date": date(year, 3, 31).strftime("%Y-%m-%d"),
                "depreciation_id": dep.id,
                "move_type": "out",
                "type_id": dep.type_id.id,
                "name": "Asset loss",
            }
            dep_line_model.with_context(depreciated_by_line=True).create(vals)
            self.assertEqual(
                float_round(dep.amount_depreciable_updated, 2),
                float_round(1000.0 - down_value, 2),
                "Invalid asset updated value!",
            )
        # (C3) Now check for depreciation amount, 90 or 91 days (leap year)
        rate = self.day_rate(date(year, 1, 1), date(year, 3, 31), is_leap=isleap(year))
        depreciation_amount = float_round(250 * rate, 2)
        dep_residual = float_round(1000.0 - 125.0 - down_value - depreciation_amount, 2)
        ctr = 0
        for dep in self.get_depreciation_lines(
            asset=asset, date_from=date(year, 3, 31), date_to=date(year, 3, 31)
        ):
            self.assertEqual(
                float_round(dep.amount, 2),
                float_round(depreciation_amount, 2),
                "Invalid depreciation amount!",
            )
            ctr += 1
        self.assertEqual(ctr, len(asset.depreciation_ids), "Missed depreciation move!")
        ctr = 0
        for dep in self.get_depreciation_lines(
            asset=asset,
            move_type="out",
            date_from=date(year, 3, 31),
            date_to=date(year, 3, 31),
        ):
            self.assertEqual(
                float_round(dep.amount, 2), down_value, "Invalid depreciation amount!"
            )
            ctr += 1
        self.assertEqual(ctr, len(asset.depreciation_ids), "Missed depreciation move!")
        # (C4) Now we do an end of year depreciation
        wiz_vals = asset.with_context(
            {"allow_reload_window": True}
        ).launch_wizard_generate_depreciations()
        wiz = (
            self.env["wizard.asset.generate.depreciation"]
            .with_context(wiz_vals["context"])
            .create({})
        )
        wiz.date_dep = date(year, 12, 31)
        wiz.do_generate()

        depreciation_amount = float_round((1000.0 - down_value) * 0.25 * (1 - rate), 2)
        dep_residual -= depreciation_amount
        # ctr = 0
        for dep in self.get_depreciation_lines(asset=asset, date_from=wiz.date_dep):
            self.assertEqual(
                float_round(dep.amount, 2),
                float_round(depreciation_amount, 2),
                "Invalid depreciation amount!",
            )
            ctr += 1
        self.assertEqual(
            ctr, len(asset.depreciation_ids) * 2, "Missed depreciation move!"
        )
        # (C4.b) Year #3: Repeat depreciation
        # Residual value is 1000.0€ - 125.0€ (1.st depreciation) - 61.64 (2.nd depr.) -
        # 725.0 € (out) - 51.8€ (last depreciation) = 36.56€
        # So last depreciation will be reduced from 250 * 25% = 62.2 € to 36.56€
        year = date.today().year
        wiz.date_dep = date(year, 12, 31)
        wiz.do_generate()
        self._test_all_depreciation_lines(
            wiz.date_dep, asset, amount=dep_residual, depreciation_nr=4, final=False
        )
        self.assertEqual(
            asset.state, "totally_depreciated", "Asset is not in non depreciated state!"
        )
        # Now remove last depreciation lines before dismiss asset
        self.get_depreciation_lines(asset=asset, date_from=date(year, 12, 31)).unlink()
        self.assertEqual(
            asset.state,
            "partially_depreciated",
            "Asset is not in non depreciated state!",
        )
        #
        # Dismis Asset #1 price 150.0€
        # Current depreciable amount is 275.0€ * 25% = 68.75€
        # Prior test (C4) | Test (C5) 31 days : Test (C6)        : (C7)
        # (year-1)-12-31  | (year-1)-01-31    : (year-1)-01-31   : (year-1)-01-31
        # Residual 36.56€ | depr -> 5.84€     : 'out' -> -30.72€ : gain -> 119.28€
        #
        dismis_date = date(year, 1, 31)
        rate = self.day_rate(date(year, 1, 1), dismis_date, is_leap=isleap(year))
        depreciation_amount = float_round(250.0 * rate * 0.25, 2)
        vals = {
            "amount": 150.0,
            "asset_id": asset.id,
            "date": dismis_date.strftime("%Y-%m-%d"),
        }
        self.env["asset.depreciation"].generate_dismiss_line(vals)
        # (C5) Dismiss asset on 2022-01-31, depreciation amount, 31 days
        # 68.75€ * 31 / 365 * 25% = 5.84€ or 68.75€ * 31 / 366 * 25% = 5.82€
        self._test_all_depreciation_lines(
            wiz.date_dep, asset, amount=depreciation_amount, depreciation_nr=4, no_test_ctr=True
        )
        self.assertEqual(
            asset.state, "totally_depreciated", "Asset is not in non depreciated state!"
        )
        # (C6)
        dep_amount = float_round(dep_residual - depreciation_amount, 2)
        for dep in self.get_depreciation_lines(
            asset=asset, date_from=wiz.date_dep, move_type="out"
        ):
            self._test_depreciation_line(wiz, dep, asset, amount=dep_amount)
        # (C7)
        dep_amount = float_round(150.0 - depreciation_amount, 2)
        for dep in self.get_depreciation_lines(
            asset=asset, date_from=wiz.date_dep, move_type="gain"
        ):
            self._test_depreciation_line(wiz, dep, asset, amount=dep_amount)

    def _test_asset_4(self):
        # Partial Dismiss tests asset #2
        #
        # Current depreciable amount is 2500.0€ * 24% = 600.0€
        # We test 3 years depreciations of 2500.0€
        # Residual 2.500€ (initial) - 150.82€ (1.depr) - 600€ (2.nd depr) = 1749.18€
        # Prior test (B2)     | Test (D3): dismis 20% for 500€
        # (year-1)-12-31      | (year)-07-31
        # depr.100% -> 600€   | Depr.amt 600€ * 24% * 212 / 365 = 348.49€
        # Residual = 1749.18€ | Residual = 1749.18€ - 348.49€ = 1400.69€
        # Rate 20% fo dismis -> 1400.69€ * 20% = 280.14€
        # Sale price: 500€ -> Gain 500€ - 280.14€ = 219.86€
        asset = self.asset_2
        year = date.today().year
        # Delete last year depreciation lines
        self.get_depreciation_lines(asset=asset, date_from=date(year, 1, 1)).unlink()
        dep_residual = asset.depreciation_ids[0].amount_residual

        dismis_date = date(year, 7, 31)
        rate = self.day_rate(date(year, 1, 1), dismis_date, is_leap=isleap(year))
        depreciation_amount = float_round(600.0 * rate, 2)
        vals = {
            "amount": 500.0,
            "asset_id": asset.id,
            "date": dismis_date.strftime("%Y-%m-%d"),
            "partial_dismissal": True,
            "partial_dismiss_percentage": 20.0,
        }
        self.env["asset.depreciation"].generate_dismiss_line(vals)
        # (D3)
        self._test_all_depreciation_lines(
            dismis_date, asset,
            amount=depreciation_amount, depreciation_nr=3, no_test_ctr=True
        )
        dep_amount = float_round((dep_residual - depreciation_amount) * 0.2, 2)
        for dep in self.get_depreciation_lines(
            asset=asset, date_from=dismis_date, move_type="out"
        ):
            self._test_depreciation_line(dismis_date, dep, asset, amount=dep_amount)
            self.assertEqual(dep.partial_dismiss_percentage,
                             20.0,
                             "Invalid dismiss rate!")

    def _test_asset_8(self):
        # Wizard tests
        #
        # Delete all records
        self.get_depreciation_lines().unlink()

        self._test_wizard_depreciation(False)
        self._test_wizard_depreciation(True)

        # Now we search for last invoice recorded
        invs = self.env["account.invoice"].search(
            [("type", "=", "out_invoice")], order="number")
        invoice = invs[0]
        invoice.journal_id.update_posted = True     # Assure invoice cancel
        invoice.action_invoice_cancel()
        invoice.action_invoice_draft()
        for line in invoice.invoice_line_ids:
            line.account_id = self.asset_1.category_id.asset_account_id.id
            break
        year = date.today().year - 1
        invoice.date_invoice = date(year, 12, 31)
        invoice.action_invoice_open()
        act_window = invoice.open_wizard_manage_asset()
        act_window = self.envtest_wizard_start(act_window)
        self.envtest_wizard_exec(
            act_window,
            button_name="link_asset",
            button_ctx={"show_asset": 0},
            web_changes=[
                ("management_type", "dismiss"),
                ("invoice_ids", [(6, 0, [invoice.id])]),
                ("asset_id", self.asset_1.id),
            ],
        )

    def _test_asset_9(self):
        # Special final tests
        #
        # Check for journal unlink is impossible when journal use in asset
        with self.assertRaises(UserError):
            self.journal.unlink()
        self.assertEqual(
            self.journal.id,
            self.env.ref("assets_management.asset_account_journal").id,
            "Invalid asset journal",
        )

    def test_asset(self):
        # self._test_asset_1()
        # self._test_asset_2()
        # self._test_asset_3()
        # self._test_asset_4()
        self._test_asset_8()
        self._test_asset_9()
