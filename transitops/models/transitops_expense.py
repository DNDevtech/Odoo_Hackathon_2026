# -*- coding: utf-8 -*-
from odoo import models, fields


class TransitopsExpense(models.Model):
    _name = 'transitops.expense'
    _description = 'Vehicle Expense'
    _rec_name = 'vehicle_id'
    _order = 'date desc'

    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True)
    expense_type = fields.Selection([
        ('toll', 'Toll'),
        ('parking', 'Parking'),
        ('fine', 'Fine'),
        ('other', 'Other'),
    ], string='Expense Type', default='toll', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    amount = fields.Float(string='Amount', required=True)
    description = fields.Char(string='Description')
