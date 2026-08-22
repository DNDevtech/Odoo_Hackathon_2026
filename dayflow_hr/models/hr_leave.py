from odoo import models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def write(self, vals):
        res = super().write(vals)
        if "state" in vals:
            day_model = self.env["dayflow.attendance.day"]
            for leave in self:
                if leave.date_from and leave.date_to:
                    day_model._dayflow_recompute(leave.employee_id, leave.date_from.date(), leave.date_to.date())
        return res
