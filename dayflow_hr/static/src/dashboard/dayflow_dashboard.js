/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { EmployeeDashboard } from "@dayflow_hr/dashboard/employee_dashboard";
import { AdminDashboard } from "@dayflow_hr/dashboard/admin_dashboard";

export class DayflowDashboard extends Component {
    static template = "dayflow_hr.DayflowDashboard";
    static components = { EmployeeDashboard, AdminDashboard };
    static props = ["*"];

    setup() {
        this.user = useService("user");
        this.state = useState({ loading: true, isAdmin: false });
        onWillStart(async () => {
            this.state.isAdmin = await this.user.hasGroup("hr.group_hr_user");
            this.state.loading = false;
        });
    }
}

registry.category("actions").add("dayflow_dashboard_action", DayflowDashboard);
