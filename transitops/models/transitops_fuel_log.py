# -*- coding: utf-8 -*-
from odoo import models, fields


class TransitopsFuelLog(models.Model):
    _name = 'transitops.fuel.log'
    _description = 'Fuel Log'
    _rec_name = 'vehicle_id'
    _order = 'date desc'

    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True)
    trip_id = fields.Many2one('transitops.trip', string='Related Trip')
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    liters = fields.Float(string='Liters', required=True)
    cost = fields.Float(string='Cost', required=True)
