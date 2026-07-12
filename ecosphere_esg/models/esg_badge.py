# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EsgBadge(models.Model):
    _name = "esg.badge"
    _description = "Badge"
    _order = "name"

    name = fields.Char(required=True)
    description = fields.Text()
    unlock_rule_type = fields.Selection([
        ("xp", "Total XP"),
        ("challenges_completed", "Completed Challenges"),
    ], required=True, default="xp", string="Unlock Rule Type")
    unlock_rule_value = fields.Integer(string="Unlock Rule Value", required=True, help="Threshold to unlock this badge")
    icon = fields.Binary(string="Icon")
    color = fields.Char(string="Color", default="#007bff")
    employee_ids = fields.Many2many("esg.employee", string="Earned By")

    def _check_auto_award(self, employee):
        auto = self.env["ir.config_parameter"].sudo().get_param("ecosphere_esg.badge_auto_award", "True")
        if auto != "True":
            return
        badges = self.search([
            ("id", "not in", employee.badge_ids.ids),
        ])
        for badge in badges:
            if badge.unlock_rule_type == "xp" and employee.total_xp >= badge.unlock_rule_value:
                employee.write({"badge_ids": [(4, badge.id)]})
            elif badge.unlock_rule_type == "challenges_completed" and employee.completed_challenges >= badge.unlock_rule_value:
                employee.write({"badge_ids": [(4, badge.id)]})
