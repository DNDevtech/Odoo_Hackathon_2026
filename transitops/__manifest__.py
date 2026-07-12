{
    'name': 'TransitOps - Smart Transport Operations Platform',
    'version': '18.0.1.0.0',
    'category': 'Operations/Fleet',
    'summary': 'End-to-end transport operations: vehicles, drivers, trips, maintenance, fuel & expenses, dashboard and analytics.',
    'description': """
TransitOps
==========
Digitizes vehicle, driver, dispatch, maintenance, fuel and expense management
for transport / logistics organizations, enforcing all mandatory business
rules from the TransitOps specification:

* Vehicle Registry (unique registration number, status lifecycle)
* Driver Management (license validity, safety score, status lifecycle)
* Trip Management with dispatch/complete/cancel workflow and validations
  (capacity check, availability check, license/suspension check)
* Maintenance workflow that automatically flips vehicle status
* Fuel & Expense logging with automatic operational cost computation
* Dashboard KPIs and Reports (Fuel Efficiency, Fleet Utilization,
  Operational Cost, Vehicle ROI)
* Role Based Access Control: Fleet Manager, Driver, Safety Officer,
  Financial Analyst
""",
    'author': 'kaushik jasoliya',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/transitops_security.xml',
        'security/ir.model.access.csv',
        'data/transitops_sequence.xml',
        'data/transitops_demo_data.xml',
        'views/vehicle_views.xml',
        'views/driver_views.xml',
        'views/trip_views.xml',
        'views/maintenance_views.xml',
        'views/fuel_log_views.xml',
        'views/expense_views.xml',
        'views/dashboard_views.xml',
        'views/dashboard_templates.xml',
        'views/transitops_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
