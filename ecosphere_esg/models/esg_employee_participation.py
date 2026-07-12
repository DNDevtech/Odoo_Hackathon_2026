# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EsgEmployeeParticipation(models.Model):
    _name = "esg.employee.participation"
    _description = "Employee CSR Participation"
    _inherit = ["mail.thread"]
    _order = "create_date desc"

    name = fields.Char(string="Reference", copy=False, readonly=True, default=lambda self: _("New"))
    employee_id = fields.Many2one("esg.employee", string="Employee", required=True, tracking=True)
    activity_id = fields.Many2one("esg.csr.activity", string="CSR Activity", required=True, tracking=True)
    department_id = fields.Many2one("esg.department", string="Department")
    proof = fields.Binary(string="Proof")
    proof_filename = fields.Char(string="Proof Filename")
    approval_status = fields.Selection([
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ], string="Approval Status", default="pending", tracking=True, copy=False)
    points_earned = fields.Integer(string="Points Earned", default=0)
    completion_date = fields.Date(string="Completion Date")

    @api.onchange("employee_id")
    def _onchange_employee_id(self):
        for p in self:
            p.department_id = p.employee_id.department_id if p.employee_id else False

    def action_approve(self):
        for p in self:
            settings = self.env["res.config.settings"].sudo().get_param("ecosphere_esg.require_proof")
            if settings and not p.proof:
                from odoo.exceptions import UserError
                raise UserError(_("Proof file is required before approval."))
            p.write({"approval_status": "approved", "completion_date": fields.Date.context_today(self)})

    def action_reject(self):
        for p in self:
            p.write({"approval_status": "rejected"})
