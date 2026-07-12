# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TransitopsVehicle(models.Model):
    _name = 'transitops.vehicle'
    _description = 'Vehicle'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(
        string='Registration Number', required=True, copy=False,
        tracking=True, index=True,
        help='Unique registration number of the vehicle, e.g. Van-05')
    model_name = fields.Char(string='Vehicle Name / Model', tracking=True)
    vehicle_type = fields.Selection([
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('car', 'Car'),
        ('bus', 'Bus'),
        ('other', 'Other'),
    ], string='Type', default='van', required=True, tracking=True)
    region = fields.Char(string='Region')
    max_load_capacity = fields.Float(string='Max Load Capacity (kg)', required=True)
    odometer = fields.Float(string='Odometer (km)')
    acquisition_cost = fields.Float(string='Acquisition Cost')
    total_revenue = fields.Float(
        string='Total Revenue',
        help='Revenue attributed to this vehicle. Used for ROI computation: '
             '(Revenue - (Maintenance + Fuel)) / Acquisition Cost. '
             'Enter manually or update from your invoicing/billing process, '
             'since TransitOps does not manage invoicing.')
    status = fields.Selection([
        ('available', 'Available'),
        ('on_trip', 'On Trip'),
        ('in_shop', 'In Shop'),
        ('retired', 'Retired'),
    ], string='Status', default='available', required=True, tracking=True)
    active = fields.Boolean(default=True)

    trip_ids = fields.One2many('transitops.trip', 'vehicle_id', string='Trips')
    maintenance_ids = fields.One2many('transitops.maintenance', 'vehicle_id', string='Maintenance Records')
    fuel_log_ids = fields.One2many('transitops.fuel.log', 'vehicle_id', string='Fuel Logs')
    expense_ids = fields.One2many('transitops.expense', 'vehicle_id', string='Expenses')

    trip_count = fields.Integer(compute='_compute_counts')
    maintenance_count = fields.Integer(compute='_compute_counts')

    total_fuel_cost = fields.Float(compute='_compute_costs', store=True, string='Total Fuel Cost')
    total_fuel_liters = fields.Float(compute='_compute_costs', store=True, string='Total Fuel (L)')
    total_maintenance_cost = fields.Float(compute='_compute_costs', store=True, string='Total Maintenance Cost')
    total_expense_cost = fields.Float(compute='_compute_costs', store=True, string='Total Other Expenses')
    total_operational_cost = fields.Float(compute='_compute_costs', store=True, string='Total Operational Cost')
    total_distance = fields.Float(compute='_compute_costs', store=True, string='Total Distance (Completed Trips)')
    fuel_efficiency = fields.Float(compute='_compute_costs', store=True, string='Fuel Efficiency (km/l)')
    vehicle_roi = fields.Float(compute='_compute_costs', store=True, string='ROI (%)')

    _sql_constraints = [
        ('registration_number_uniq', 'unique(name)',
         'The vehicle registration number must be unique!'),
    ]

    def _compute_counts(self):
        for vehicle in self:
            vehicle.trip_count = len(vehicle.trip_ids)
            vehicle.maintenance_count = len(vehicle.maintenance_ids)

    @api.depends(
        'fuel_log_ids.cost', 'fuel_log_ids.liters',
        'maintenance_ids.cost', 'maintenance_ids.state',
        'expense_ids.amount',
        'trip_ids.state', 'trip_ids.actual_distance', 'trip_ids.planned_distance',
        'acquisition_cost', 'total_revenue',
    )
    def _compute_costs(self):
        for vehicle in self:
            fuel_cost = sum(vehicle.fuel_log_ids.mapped('cost'))
            fuel_liters = sum(vehicle.fuel_log_ids.mapped('liters'))
            maintenance_cost = sum(
                vehicle.maintenance_ids.filtered(lambda m: m.state != 'draft').mapped('cost')
            )
            expense_cost = sum(vehicle.expense_ids.mapped('amount'))
            completed_trips = vehicle.trip_ids.filtered(lambda t: t.state == 'completed')
            distance = sum(
                (t.actual_distance or t.planned_distance) for t in completed_trips
            )

            vehicle.total_fuel_cost = fuel_cost
            vehicle.total_fuel_liters = fuel_liters
            vehicle.total_maintenance_cost = maintenance_cost
            vehicle.total_expense_cost = expense_cost
            vehicle.total_operational_cost = fuel_cost + maintenance_cost + expense_cost
            vehicle.total_distance = distance
            vehicle.fuel_efficiency = (distance / fuel_liters) if fuel_liters else 0.0
            vehicle.vehicle_roi = (
                ((vehicle.total_revenue - (maintenance_cost + fuel_cost)) / vehicle.acquisition_cost) * 100
                if vehicle.acquisition_cost else 0.0
            )

    @api.constrains('max_load_capacity')
    def _check_capacity(self):
        for vehicle in self:
            if vehicle.max_load_capacity <= 0:
                raise ValidationError(_('Max Load Capacity must be greater than zero.'))

    def action_view_trips(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Trips'),
            'res_model': 'transitops.trip',
            'view_mode': 'list,form',
            'domain': [('vehicle_id', '=', self.id)],
            'context': {'default_vehicle_id': self.id},
        }

    def action_view_maintenance(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Maintenance'),
            'res_model': 'transitops.maintenance',
            'view_mode': 'list,form',
            'domain': [('vehicle_id', '=', self.id)],
            'context': {'default_vehicle_id': self.id},
        }
