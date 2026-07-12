# -*- coding: utf-8 -*-
from odoo import fields, models


class EsgProductProfile(models.Model):
    _name = "esg.product.profile"
    _description = "Product ESG Profile"
    _order = "name"

    name = fields.Char(required=True)
    product_id = fields.Many2one("product.template", string="Product")
    carbon_footprint = fields.Float(string="Carbon Footprint (kgCO2e)")
    recyclable = fields.Boolean(default=False)
    sustainable_material = fields.Boolean(default=False)
    notes = fields.Text()
    active = fields.Boolean(default=True)
