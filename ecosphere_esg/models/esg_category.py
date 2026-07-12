# -*- coding: utf-8 -*-
from odoo import fields, models


class EsgCategory(models.Model):
    _name = "esg.category"
    _description = "ESG Category"
    _order = "name"

    name = fields.Char(required=True)
    type = fields.Selection([
        ("csr_activity", "CSR Activity"),
        ("challenge", "Challenge"),
    ], required=True, default="csr_activity")
    active = fields.Boolean(default=True)
