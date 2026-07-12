# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EsgAudit(models.Model):
    _name = "esg.audit"
    _description = "Governance Audit"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(string="Audit Title", required=True, tracking=True)
    description = fields.Text()
    department_id = fields.Many2one("esg.department", string="Department")
    auditor_id = fields.Many2one("esg.employee", string="Auditor")
    audit_date = fields.Date(string="Audit Date", default=fields.Date.context_today)
    state = fields.Selection([
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ], default="planned", tracking=True, copy=False)

    compliance_issue_ids = fields.One2many("esg.compliance.issue", "audit_id")
    issue_count = fields.Integer(compute="_compute_issue_count")

    def _compute_issue_count(self):
        for a in self:
            a.issue_count = len(a.compliance_issue_ids)

    def action_start(self):
        for a in self:
            a.write({"state": "in_progress"})

    def action_complete(self):
        for a in self:
            a.write({"state": "completed"})

    def action_cancel(self):
        for a in self:
            a.write({"state": "cancelled"})
