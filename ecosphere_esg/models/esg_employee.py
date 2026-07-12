# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EsgEmployee(models.Model):
    _name = "esg.employee"
    _description = "Employee"
    _inherits = {"res.users": "user_id"}
    _order = "name"

    user_id = fields.Many2one("res.users", string="Related User", required=True, ondelete="cascade")
    department_id = fields.Many2one("esg.department", string="Department")
    job_title = fields.Char(string="Job Title")
    status = fields.Selection([
        ("active", "Active"),
        ("inactive", "Inactive"),
    ], default="active", tracking=True)

    total_xp = fields.Integer(string="Total XP", default=0, tracking=True)
    completed_challenges = fields.Integer(string="Completed Challenges", default=0)

    participation_ids = fields.One2many("esg.employee.participation", "employee_id")
    challenge_participation_ids = fields.One2many("esg.challenge.participation", "employee_id")
    badge_ids = fields.Many2many("esg.badge", string="Badges")
    policy_acknowledgement_ids = fields.One2many("esg.policy.acknowledgement", "employee_id")

    badge_count = fields.Integer(compute="_compute_badge_count")

    def _compute_badge_count(self):
        for emp in self:
            emp.badge_count = len(emp.badge_ids)

    def action_view_participations(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "CSR Participations",
            "res_model": "esg.employee.participation",
            "view_mode": "list,form",
            "domain": [("employee_id", "=", self.id)],
            "context": {"default_employee_id": self.id},
        }

    def action_view_badges(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Badges",
            "res_model": "esg.badge",
            "view_mode": "list,form",
            "domain": [("id", "in", self.badge_ids.ids)],
        }
