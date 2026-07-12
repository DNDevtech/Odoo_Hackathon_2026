# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EsgChallenge(models.Model):
    _name = "esg.challenge"
    _description = "Challenge"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(string="Title", required=True, tracking=True)
    category_id = fields.Many2one("esg.category", string="Category",
                                  domain=[("type", "=", "challenge")])
    description = fields.Text()
    xp_reward = fields.Integer(string="XP Reward", required=True, default=10)
    difficulty = fields.Selection([
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ], default="medium", required=True)
    evidence_required = fields.Boolean(string="Evidence Required", default=True)
    deadline = fields.Date(string="Deadline")
    state = fields.Selection([
        ("draft", "Draft"),
        ("active", "Active"),
        ("under_review", "Under Review"),
        ("completed", "Completed"),
        ("archived", "Archived"),
    ], default="draft", tracking=True, copy=False)

    participation_ids = fields.One2many("esg.challenge.participation", "challenge_id")
    participation_count = fields.Integer(compute="_compute_participation_count")

    def _compute_participation_count(self):
        for ch in self:
            ch.participation_count = len(ch.participation_ids)

    def action_activate(self):
        for ch in self:
            ch.write({"state": "active"})

    def action_review(self):
        for ch in self:
            ch.write({"state": "under_review"})

    def action_complete(self):
        for ch in self:
            ch.write({"state": "completed"})

    def action_archive(self):
        for ch in self:
            ch.write({"state": "archived"})
