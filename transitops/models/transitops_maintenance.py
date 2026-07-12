# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TransitopsMaintenance(models.Model):
    _name = 'transitops.maintenance'
    _description = 'Maintenance Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'date desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                        readonly=True, default=lambda self: _('New'))
    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True, tracking=True)
    description = fields.Char(string='Description', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    cost = fields.Float(string='Cost')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True, tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('transitops.maintenance') or _('New')
        return super().create(vals_list)

    def action_start(self):
        """Adding a vehicle to an active Maintenance Log switches it to 'In Shop',
        removing it from the driver's selection pool."""
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Only Draft maintenance records can be started.'))
            if record.vehicle_id.status == 'on_trip':
                raise UserError(_(
                    "Vehicle %s is currently On Trip and cannot be sent to maintenance.",
                    record.vehicle_id.name
                ))
            record.write({'state': 'in_progress'})
            record.vehicle_id.write({'status': 'in_shop'})

    def action_close(self):
        """Closing maintenance restores the vehicle to Available (unless retired)."""
        for record in self:
            if record.state != 'in_progress':
                raise UserError(_('Only In Progress maintenance records can be closed.'))
            record.write({'state': 'done'})
            if record.vehicle_id.status != 'retired':
                record.vehicle_id.write({'status': 'available'})

    def action_reset_to_draft(self):
        for record in self:
            record.write({'state': 'draft'})
