# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class TransitopsTrip(models.Model):
    _name = 'transitops.trip'
    _description = 'Trip'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'create_date desc'

    name = fields.Char(string='Trip Reference', required=True, copy=False,
                        readonly=True, default=lambda self: _('New'))
    source = fields.Char(string='Source', required=True)
    destination = fields.Char(string='Destination', required=True)
    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True,
                                  tracking=True,
                                  domain="[('status', '=', 'available')]")
    driver_id = fields.Many2one('transitops.driver', string='Driver', required=True,
                                 tracking=True,
                                 domain="[('status', '=', 'available')]")
    cargo_weight = fields.Float(string='Cargo Weight (kg)', required=True)
    planned_distance = fields.Float(string='Planned Distance (km)', required=True)
    actual_distance = fields.Float(string='Actual Distance (km)')
    fuel_consumed = fields.Float(string='Fuel Consumed (L)')
    final_odometer = fields.Float(string='Final Odometer (km)')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('dispatched', 'Dispatched'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True, copy=False)
    dispatch_date = fields.Datetime(string='Dispatch Date', readonly=True)
    complete_date = fields.Datetime(string='Completion Date', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('transitops.trip') or _('New')
        return super().create(vals_list)

    @api.constrains('cargo_weight', 'vehicle_id')
    def _check_cargo_weight(self):
        for trip in self:
            if trip.vehicle_id and trip.cargo_weight > trip.vehicle_id.max_load_capacity:
                raise ValidationError(_(
                    "Cargo Weight (%(weight)s kg) exceeds vehicle %(vehicle)s's "
                    "maximum load capacity (%(capacity)s kg).",
                    weight=trip.cargo_weight,
                    vehicle=trip.vehicle_id.name,
                    capacity=trip.vehicle_id.max_load_capacity,
                ))

    def action_dispatch(self):
        for trip in self:
            if trip.state != 'draft':
                raise UserError(_('Only Draft trips can be dispatched.'))

            vehicle = trip.vehicle_id
            driver = trip.driver_id

            if vehicle.status in ('retired', 'in_shop'):
                raise UserError(_(
                    "Vehicle %s is %s and cannot be dispatched.",
                    vehicle.name, dict(vehicle._fields['status'].selection).get(vehicle.status)
                ))
            if vehicle.status == 'on_trip':
                raise UserError(_("Vehicle %s is already On Trip.", vehicle.name))

            if driver.status == 'suspended':
                raise UserError(_("Driver %s is Suspended and cannot be assigned to a trip.", driver.name))
            if driver.status == 'on_trip':
                raise UserError(_("Driver %s is already On Trip.", driver.name))
            if driver.is_license_expired:
                raise UserError(_(
                    "Driver %s's license expired on %s and cannot be assigned to a trip.",
                    driver.name, driver.license_expiry_date
                ))

            if trip.cargo_weight > vehicle.max_load_capacity:
                raise UserError(_(
                    "Cargo Weight exceeds vehicle %s's maximum load capacity.", vehicle.name
                ))

            trip.write({
                'state': 'dispatched',
                'dispatch_date': fields.Datetime.now(),
            })
            vehicle.write({'status': 'on_trip'})
            driver.write({'status': 'on_trip'})

    def action_complete(self):
        for trip in self:
            if trip.state != 'dispatched':
                raise UserError(_('Only Dispatched trips can be completed.'))

            trip.write({
                'state': 'completed',
                'complete_date': fields.Datetime.now(),
                'actual_distance': trip.actual_distance or trip.planned_distance,
            })
            if trip.final_odometer:
                trip.vehicle_id.write({'odometer': trip.final_odometer})
            trip.vehicle_id.write({'status': 'available'})
            trip.driver_id.write({'status': 'available'})

    def action_cancel(self):
        for trip in self:
            if trip.state not in ('draft', 'dispatched'):
                raise UserError(_('Only Draft or Dispatched trips can be cancelled.'))
            was_dispatched = trip.state == 'dispatched'
            trip.write({'state': 'cancelled'})
            if was_dispatched:
                trip.vehicle_id.write({'status': 'available'})
                trip.driver_id.write({'status': 'available'})

    def action_reset_to_draft(self):
        for trip in self:
            if trip.state != 'cancelled':
                raise UserError(_('Only Cancelled trips can be reset to Draft.'))
            trip.write({'state': 'draft'})
