# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TransitopsDriver(models.Model):
    _name = 'transitops.driver'
    _description = 'Driver'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Name', required=True, tracking=True)
    license_number = fields.Char(string='License Number', required=True, copy=False, tracking=True)
    license_category = fields.Char(string='License Category')
    license_expiry_date = fields.Date(string='License Expiry Date', required=True, tracking=True)
    contact_number = fields.Char(string='Contact Number')
    safety_score = fields.Float(string='Safety Score', default=100.0, tracking=True,
                                 help='0-100 safety score based on incidents / compliance.')
    status = fields.Selection([
        ('available', 'Available'),
        ('on_trip', 'On Trip'),
        ('off_duty', 'Off Duty'),
        ('suspended', 'Suspended'),
    ], string='Status', default='available', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Linked User Account')
    active = fields.Boolean(default=True)

    trip_ids = fields.One2many('transitops.trip', 'driver_id', string='Trips')
    trip_count = fields.Integer(compute='_compute_trip_count')

    is_license_expired = fields.Boolean(compute='_compute_is_license_expired', store=True,
                                         string='License Expired')

    _sql_constraints = [
        ('license_number_uniq', 'unique(license_number)',
         'The license number must be unique!'),
    ]

    @api.depends('license_expiry_date')
    def _compute_is_license_expired(self):
        today = fields.Date.context_today(self)
        for driver in self:
            driver.is_license_expired = bool(
                driver.license_expiry_date and driver.license_expiry_date < today
            )

    def _compute_trip_count(self):
        for driver in self:
            driver.trip_count = len(driver.trip_ids)

    @api.constrains('safety_score')
    def _check_safety_score(self):
        for driver in self:
            if not (0 <= driver.safety_score <= 100):
                raise ValidationError(_('Safety Score must be between 0 and 100.'))

    def action_view_trips(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Trips'),
            'res_model': 'transitops.trip',
            'view_mode': 'list,form',
            'domain': [('driver_id', '=', self.id)],
            'context': {'default_driver_id': self.id},
        }
