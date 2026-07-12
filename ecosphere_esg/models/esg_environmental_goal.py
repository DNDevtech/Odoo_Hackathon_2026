# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EsgEnvironmentalGoal(models.Model):
    _name = "esg.environmental.goal"
    _description = "Environmental Goal"
    _order = "name"

    name = fields.Char(required=True)
    description = fields.Text()
    department_id = fields.Many2one("esg.department", string="Department")
    target_value = fields.Float(string="Target (kgCO2e)", required=True)
    current_value = fields.Float(string="Current (kgCO2e)", default=0)
    unit = fields.Char(default="kgCO2e")
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("active", "Active"),
        ("achieved", "Achieved"),
        ("missed", "Missed"),
    ], default="draft", tracking=True, copy=False)

    progress = fields.Float(compute="_compute_progress", store=True, string="Progress (%)")

    @api.depends("target_value", "current_value")
    def _compute_progress(self):
        for goal in self:
            if goal.target_value:
                goal.progress = min((goal.current_value / goal.target_value) * 100, 100)
            else:
                goal.progress = 0.0

    def action_activate(self):
        for g in self:
            g.write({"state": "active"})

    def action_achieve(self):
        for g in self:
            g.write({"state": "achieved"})
