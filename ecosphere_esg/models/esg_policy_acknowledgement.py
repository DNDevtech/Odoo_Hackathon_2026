# -*- coding: utf-8 -*-
from odoo import fields, models, _


class EsgPolicyAcknowledgement(models.Model):
    _name = "esg.policy.acknowledgement"
    _description = "Policy Acknowledgement"
    _order = "create_date desc"

    name = fields.Char(string="Reference", copy=False, readonly=True, default=lambda self: _("New"))
    policy_id = fields.Many2one("esg.policy", string="Policy", required=True)
    employee_id = fields.Many2one("esg.employee", string="Employee", required=True)
    acknowledged_date = fields.Datetime(string="Acknowledgement Date", default=fields.Datetime.now)
    state = fields.Selection([
        ("pending", "Pending"),
        ("acknowledged", "Acknowledged"),
    ], default="pending", copy=False)

    def action_acknowledge(self):
        for r in self:
            r.write({"state": "acknowledged", "acknowledged_date": fields.Datetime.now()})
