# -*- coding: utf-8 -*-
from odoo import fields, models


class EsgEmissionFactor(models.Model):
    _name = "esg.emission.factor"
    _description = "Emission Factor"
    _order = "name"

    name = fields.Char(required=True)
    category = fields.Selection([
        ("electricity", "Electricity"),
        ("fuel", "Fuel"),
        ("transport", "Transport"),
        ("waste", "Waste"),
        ("water", "Water"),
        ("other", "Other"),
    ], required=True, default="electricity")
    factor_value = fields.Float(string="Factor (kgCO2e per unit)", required=True)
    unit = fields.Char(string="Unit", help="e.g. kWh, litre, km")
    description = fields.Text()
    active = fields.Boolean(default=True)
