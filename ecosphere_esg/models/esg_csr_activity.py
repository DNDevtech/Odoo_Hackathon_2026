# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EsgCsrActivity(models.Model):
    _name = "esg.csr.activity"
    _description = "CSR Activity"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(required=True, tracking=True)
    description = fields.Text()
    category_id = fields.Many2one("esg.category", string="Category",
                                  domain=[("type", "=", "csr_activity")])
    department_id = fields.Many2one("esg.department", string="Department")
    activity_date = fields.Date(string="Activity Date", default=fields.Date.context_today)
    state = fields.Selection([
        ("draft", "Draft"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ], default="draft", tracking=True, copy=False)

    participation_ids = fields.One2many("esg.employee.participation", "activity_id")
    participation_count = fields.Integer(compute="_compute_participation_count")

    def _compute_participation_count(self):
        for act in self:
            act.participation_count = len(act.participation_ids)

    def action_activate(self):
        for a in self:
            a.write({"state": "active"})

    def action_complete(self):
        for a in self:
            a.write({"state": "completed"})

    def action_cancel(self):
        for a in self:
            a.write({"state": "cancelled"})
