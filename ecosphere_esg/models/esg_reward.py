# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EsgReward(models.Model):
    _name = "esg.reward"
    _description = "Reward"
    _order = "name"

    name = fields.Char(required=True)
    description = fields.Text()
    points_required = fields.Integer(string="Points Required", required=True)
    stock = fields.Integer(string="Stock", default=0)
    state = fields.Selection([
        ("available", "Available"),
        ("out_of_stock", "Out of Stock"),
    ], default="available", copy=False)
    image = fields.Binary(string="Image")
    redemption_ids = fields.One2many("esg.reward.redemption", "reward_id")

    def action_redeem(self):
        employee = self.env["esg.employee"].search([("user_id", "=", self.env.uid)], limit=1)
        if not employee:
            raise UserError(_("No employee profile found for the current user."))
        if self.stock <= 0:
            raise UserError(_("This reward is out of stock."))
        if employee.total_xp < self.points_required:
            raise UserError(_(
                "Insufficient XP. You have %(xp)s but need %(required)s.",
                xp=employee.total_xp, required=self.points_required
            ))
        employee.write({"total_xp": employee.total_xp - self.points_required})
        self.write({"stock": self.stock - 1})
        self.env["esg.reward.redemption"].create({
            "employee_id": employee.id,
            "reward_id": self.id,
            "points_spent": self.points_required,
        })


class EsgRewardRedemption(models.Model):
    _name = "esg.reward.redemption"
    _description = "Reward Redemption"
    _order = "create_date desc"

    employee_id = fields.Many2one("esg.employee", string="Employee", required=True)
    reward_id = fields.Many2one("esg.reward", string="Reward", required=True)
    points_spent = fields.Integer(string="Points Spent", required=True)
    redemption_date = fields.Datetime(string="Redemption Date", default=fields.Datetime.now)
    state = fields.Selection([
        ("pending", "Pending"),
        ("delivered", "Delivered"),
    ], default="pending", copy=False)

    def action_deliver(self):
        for r in self:
            r.write({"state": "delivered"})
