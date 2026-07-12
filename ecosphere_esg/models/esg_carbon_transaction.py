# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EsgCarbonTransaction(models.Model):
    _name = "esg.carbon.transaction"
    _description = "Carbon Transaction"
    _inherit = ["mail.thread"]
    _order = "date desc"

    name = fields.Char(string="Reference", copy=False, readonly=True, default=lambda self: _("New"))
    date = fields.Date(string="Date", default=fields.Date.context_today, required=True)
    department_id = fields.Many2one("esg.department", string="Department")
    source_model = fields.Selection([
        ("purchase", "Purchase"),
        ("manufacturing", "Manufacturing"),
        ("expense", "Expense"),
        ("fleet", "Fleet"),
        ("manual", "Manual"),
    ], string="Source", default="manual", required=True)
    source_id = fields.Integer(string="Source Record ID")
    emission_factor_id = fields.Many2one("esg.emission.factor", string="Emission Factor")
    quantity = fields.Float(string="Quantity", default=1.0)
    emission_kgco2e = fields.Float(string="Emissions (kgCO2e)", compute="_compute_emission", store=True)
    notes = fields.Text()
    state = fields.Selection([
        ("draft", "Draft"),
        ("posted", "Posted"),
    ], default="draft", copy=False, tracking=True)

    @api.depends("emission_factor_id", "quantity")
    def _compute_emission(self):
        for tx in self:
            if tx.emission_factor_id:
                tx.emission_kgco2e = tx.emission_factor_id.factor_value * tx.quantity
            else:
                tx.emission_kgco2e = 0.0

    def action_post(self):
        for tx in self:
            tx.write({"state": "posted"})
