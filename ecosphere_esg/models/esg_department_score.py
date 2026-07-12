# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EsgDepartmentScore(models.Model):
    _name = "esg.department.score"
    _description = "Department ESG Score"
    _order = "department_id"

    name = fields.Char(compute="_compute_name")
    department_id = fields.Many2one("esg.department", string="Department", required=True, unique=True)
    period = fields.Char(string="Period", help="e.g. 2025-Q1")
    environmental_score = fields.Float(string="Environmental Score", default=0)
    social_score = fields.Float(string="Social Score", default=0)
    governance_score = fields.Float(string="Governance Score", default=0)
    total_score = fields.Float(compute="_compute_total_score", store=True, string="Total ESG Score")

    @api.depends("environmental_score", "social_score", "governance_score")
    def _compute_total_score(self):
        env_weight = float(self.env["ir.config_parameter"].sudo().get_param("ecosphere_esg.weight_environmental", "0.4"))
        soc_weight = float(self.env["ir.config_parameter"].sudo().get_param("ecosphere_esg.weight_social", "0.3"))
        gov_weight = float(self.env["ir.config_parameter"].sudo().get_param("ecosphere_esg.weight_governance", "0.3"))
        for score in self:
            score.total_score = (
                score.environmental_score * env_weight +
                score.social_score * soc_weight +
                score.governance_score * gov_weight
            )

    def _compute_name(self):
        for s in self:
            s.name = s.department_id.name or ""
