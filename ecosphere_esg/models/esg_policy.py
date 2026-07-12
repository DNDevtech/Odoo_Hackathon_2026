# -*- coding: utf-8 -*-
from odoo import fields, models, _


class EsgPolicy(models.Model):
    _name = "esg.policy"
    _description = "ESG Policy"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, tracking=True)
    description = fields.Text()
    category = fields.Selection([
        ("environmental", "Environmental"),
        ("social", "Social"),
        ("governance", "Governance"),
    ], required=True, default="governance")
    version = fields.Char(string="Version")
    effective_date = fields.Date(required=True)
    review_date = fields.Date(string="Next Review Date")
    state = fields.Selection([
        ("draft", "Draft"),
        ("active", "Active"),
        ("archived", "Archived"),
    ], default="draft", tracking=True, copy=False)

    acknowledgement_ids = fields.One2many("esg.policy.acknowledgement", "policy_id")
    acknowledgement_required = fields.Boolean(default=True)

    def action_activate(self):
        for p in self:
            p.write({"state": "active"})

    def action_archive(self):
        for p in self:
            p.write({"state": "archived"})
