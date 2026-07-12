# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EsgDepartment(models.Model):
    _name = "esg.department"
    _description = "Department"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char()
    head_id = fields.Many2one("res.users", string="Department Head")
    parent_id = fields.Many2one("esg.department", string="Parent Department", index=True, ondelete="cascade")
    child_ids = fields.One2many("esg.department", "parent_id", string="Sub-Departments")
    employee_count = fields.Integer(compute="_compute_employee_count", string="Employees")
    active = fields.Boolean(default=True)

    carbon_transaction_ids = fields.One2many("esg.carbon.transaction", "department_id")
    participation_ids = fields.One2many("esg.employee.participation", "department_id")
    challenge_participation_ids = fields.One2many("esg.challenge.participation", "department_id")
    score_ids = fields.One2many("esg.department.score", "department_id")

    _sql_constraints = [
        ("code_uniq", "unique(code)", "Department code must be unique."),
    ]

    def _compute_employee_count(self):
        for dept in self:
            dept.employee_count = self.env["esg.employee"].search_count([("department_id", "=", dept.id)])

    @api.constrains("parent_id")
    def _check_parent_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create a recursive department hierarchy."))
