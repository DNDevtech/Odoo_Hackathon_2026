# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EsgReportWizard(models.TransientModel):
    _name = "esg.report.wizard"
    _description = "ESG Report Wizard"

    department_id = fields.Many2one("esg.department", string="Department")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    module = fields.Selection([
        ("environmental", "Environmental"),
        ("social", "Social"),
        ("governance", "Governance"),
        ("all", "All"),
    ], string="Module", default="all")
    report_type = fields.Selection([
        ("pdf", "PDF"),
        ("excel", "Excel"),
        ("csv", "CSV"),
    ], string="Export Format", default="pdf", required=True)

    def action_generate_report(self):
        domain = []
        if self.department_id:
            domain.append(("department_id", "=", self.department_id.id))
        scores = self.env["esg.department.score"].search(domain)
        return {
            "type": "ir.actions.act_window",
            "name": "ESG Report",
            "res_model": "esg.department.score",
            "view_mode": "list,form",
            "domain": [("id", "in", scores.ids)],
        }
