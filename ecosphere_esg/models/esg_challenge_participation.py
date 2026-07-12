# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EsgChallengeParticipation(models.Model):
    _name = "esg.challenge.participation"
    _description = "Challenge Participation"
    _inherit = ["mail.thread"]
    _order = "create_date desc"

    name = fields.Char(string="Reference", copy=False, readonly=True, default=lambda self: _("New"))
    challenge_id = fields.Many2one("esg.challenge", string="Challenge", required=True, tracking=True)
    employee_id = fields.Many2one("esg.employee", string="Employee", required=True, tracking=True)
    progress = fields.Selection([
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("submitted", "Submitted"),
        ("completed", "Completed"),
    ], default="not_started", tracking=True, copy=False)
    proof = fields.Binary(string="Evidence")
    proof_filename = fields.Char(string="Evidence Filename")
    approval = fields.Selection([
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ], default="pending", tracking=True, copy=False)
    xp_awarded = fields.Integer(string="XP Awarded", default=0)

    def action_submit(self):
        for p in self:
            p.write({"progress": "submitted"})

    def action_approve(self):
        for p in self:
            settings = self.env["res.config.settings"].sudo().get_param("ecosphere_esg.require_proof")
            if settings and not p.proof:
                raise UserError(_("Evidence file is required before approval."))
            p.write({"approval": "approved", "progress": "completed", "xp_awarded": p.challenge_id.xp_reward})
            employee = p.employee_id
            employee.write({"total_xp": employee.total_xp + p.challenge_id.xp_reward,
                            "completed_challenges": employee.completed_challenges + 1})
            self.env["esg.badge"].sudo()._check_auto_award(employee)

    def action_reject(self):
        for p in self:
            p.write({"approval": "rejected"})
