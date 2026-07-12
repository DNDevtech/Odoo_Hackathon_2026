# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EsgComplianceIssue(models.Model):
    _name = "esg.compliance.issue"
    _description = "Compliance Issue"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(string="Issue Title", required=True, tracking=True)
    description = fields.Text()
    audit_id = fields.Many2one("esg.audit", string="Audit")
    severity = fields.Selection([
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ], required=True, default="medium", tracking=True)
    owner_id = fields.Many2one("esg.employee", string="Owner", required=True, tracking=True)
    due_date = fields.Date(string="Due Date", required=True, tracking=True)
    state = fields.Selection([
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ], default="open", tracking=True, copy=False)
    is_overdue = fields.Boolean(compute="_compute_is_overdue", store=True)

    @api.depends("due_date", "state")
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for issue in self:
            issue.is_overdue = bool(
                issue.due_date and issue.due_date < today and issue.state in ("open", "in_progress")
            )

    def action_start(self):
        for i in self:
            i.write({"state": "in_progress"})

    def action_resolve(self):
        for i in self:
            i.write({"state": "resolved"})

    def action_close(self):
        for i in self:
            i.write({"state": "closed"})

    def _flag_overdue(self):
        today = fields.Date.context_today(self)
        overdue = self.search([
            ("due_date", "<", today),
            ("state", "in", ("open", "in_progress")),
        ])
        for issue in overdue:
            issue.message_post(body="This compliance issue is overdue!")
