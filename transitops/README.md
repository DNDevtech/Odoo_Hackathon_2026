# TransitOps — Smart Transport Operations Platform (Odoo 18)

A custom Odoo 18 module implementing the TransitOps functional spec: vehicle
registry, driver management, trip dispatch workflow, maintenance workflow,
fuel & expense tracking, RBAC, dashboard and cost/ROI analytics.

## Installation

1. Copy the `transitops` folder into your Odoo 18 `addons` path, e.g.:
   ```
   /opt/odoo18/addons/transitops
   ```
2. Restart the Odoo service (or start Odoo pointing `--addons-path` at the
   folder containing `transitops`).
3. Activate developer mode, go to **Apps**, click **Update Apps List**.
4. Search for "TransitOps" and click **Install**.

No extra Python dependencies are required — only Odoo's built-in `base` and
`mail` modules.

## Assigning Roles (RBAC)

Go to **Settings → Users & Companies → Users**, open a user, and under the
**TransitOps** section of the "Other" tab (or the access rights table) tick
one or more of:
- **Fleet Manager** — full control of Vehicles, Maintenance, Trips, Drivers
- **Driver** — creates/dispatches trips, logs fuel, read-only on vehicles/drivers
- **Safety Officer** — manages driver compliance (license, status, safety score)
- **Financial Analyst** — reviews costs, manages Expenses

(Fleet Manager implies Driver-level trip access.)

## Data Model

| Model | Purpose |
|---|---|
| `transitops.vehicle` | Vehicle registry, lifecycle status, computed cost/ROI/efficiency |
| `transitops.driver` | Driver profile, license validity, safety score, status |
| `transitops.trip` | Draft → Dispatched → Completed/Cancelled trip workflow |
| `transitops.maintenance` | Draft → In Progress → Done maintenance workflow |
| `transitops.fuel.log` | Fuel entries (liters, cost, date) per vehicle/trip |
| `transitops.expense` | Toll/parking/fine/other expenses per vehicle |

## Business Rules Implemented

- Registration number and license number are unique (SQL constraints).
- A trip can only be **dispatched** if:
  - vehicle status is `available` (not retired/in_shop/on_trip)
  - driver status is `available` (not suspended/on_trip) and license not expired
  - cargo weight ≤ vehicle max load capacity
- **Dispatch** flips vehicle & driver to `on_trip`; **Complete** and
  **Cancel** (from dispatched) revert both to `available`.
- Starting a **Maintenance** record flips the vehicle to `in_shop` and blocks
  it from trip domains (only `available` vehicles are selectable on trips);
  closing it restores `available` (unless the vehicle is `retired`).
- Vehicle costs, fuel efficiency (km/l) and ROI
  `(Revenue - (Maintenance + Fuel)) / Acquisition Cost` are computed fields,
  stored and visible on the vehicle form and in the Cost & ROI Analysis
  pivot/graph. `total_revenue` is a manually maintained field since
  TransitOps does not manage invoicing.

## Reports & Analytics

- **Dashboard** menu: Kanban of vehicles grouped by status (Available / On
  Trip / In Shop / Retired) — mirrors the spec's KPI cards.
- **Reports → Trip Analysis**: pivot/graph by trip state, vehicle, distance.
- **Reports → Cost & ROI Analysis**: pivot/graph of fuel/maintenance/expense
  costs, fuel efficiency and ROI per vehicle.
- Every list view supports Odoo's native **Export** (CSV/XLSX) — satisfies
  the "Support CSV export" requirement out of the box.

## Notes / Suggested Next Steps

- The Excalidraw mockup link in the brief is an interactive canvas app with
  no static/scrapeable content, so the UI here follows standard Odoo 18
  form/list/kanban/pivot conventions rather than a pixel-for-picture copy.
  If you can export the mockup as PNG/PDF, I can adjust field grouping,
  ordering, and labels to match it exactly.
- Bonus items not yet built (flagged as optional in the spec): PDF export,
  email reminders for expiring licenses, vehicle document attachments
  management screen, dark mode. Happy to add any of these next.
