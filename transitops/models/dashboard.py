from odoo import models, fields, api


class TransitOpsDashboard(models.TransientModel):
    _name = "transitops.dashboard"
    _description = "TransitOps Dashboard"

    name = fields.Char(default="TransitOps Dashboard")
    html = fields.Html(compute="_compute_html", sanitize=False)

    def _compute_html(self):
        for rec in self:
            rec.html = self.env['ir.qweb']._render('transitops.dashboard_content', self._values())

    def _values(self):
        env = self.env
        Vehicle = env['transitops.vehicle']
        Trip = env['transitops.trip']
        Driver = env['transitops.driver']
        total_veh = Vehicle.search_count([])
        available = Vehicle.search_count([('status', '=', 'available')])
        on_trip = Vehicle.search_count([('status', '=', 'on_trip')])
        in_shop = Vehicle.search_count([('status', '=', 'in_shop')])
        active_trips = Trip.search_count([('state', '=', 'dispatched')])
        pending_trips = Trip.search_count([('state', '=', 'draft')])
        drivers_on_duty = Driver.search_count([('status', '=', 'on_trip')])
        drivers_total = Driver.search_count([])
        utilization = round(on_trip / total_veh * 100, 1) if total_veh else 0
        dist = [
            {'label': 'Available', 'count': available, 'color': '#1e9e6a'},
            {'label': 'On Trip', 'count': on_trip, 'color': '#2f80ed'},
            {'label': 'In Shop', 'count': in_shop, 'color': '#f2994a'},
            {'label': 'Retired', 'count': Vehicle.search_count([('status', '=', 'retired')]), 'color': '#eb5757'},
        ]
        max_dist = max((d['count'] for d in dist), default=1) or 1
        for d in dist:
            d['style'] = "width:%d%%; background:%s;" % (
                round(d['count'] / max_dist * 100) if max_dist else 0, d['color'])

        def act(xmlid):
            return '/web#action=%s' % env.ref(xmlid).id

        return {
            'kpis': [
                ('Available Vehicles', available, '#1e9e6a'),
                ('Active Vehicles', on_trip, '#2f80ed'),
                ('Vehicles in Maintenance', in_shop, '#f2994a'),
                ('Active Trips', active_trips, '#2f80ed'),
                ('Pending Trips', pending_trips, '#f2c94c'),
                ('Drivers on Duty', drivers_on_duty, '#1e9e6a'),
            ],
            'utilization': utilization,
            'drivers_total': drivers_total,
            'dist': dist, 'max_dist': max_dist,
            'recent_trips': Trip.search([], order='create_date desc', limit=8),
            'recent_vehicles': Vehicle.search([], order='create_date desc', limit=6),
            'links': {
                'vehicle': act('transitops.action_transitops_vehicle'),
                'trip': act('transitops.action_transitops_trip'),
                'driver': act('transitops.action_transitops_driver'),
                'fuel': act('transitops.action_transitops_fuel_log'),
                'maintenance': act('transitops.action_transitops_maintenance'),
            },
        }
