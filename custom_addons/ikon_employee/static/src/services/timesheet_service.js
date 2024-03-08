/** @odoo-module */

import { registry } from "@web/core/registry";
const { reactive } = owl

export const TimesheetService = {

    dependencies:["rpc"],
    async start(env, { rpc }){
        // let timesheet_data = reactive({})
        let timesheet_data = await rpc("/ikon_employee/timesheet_data/")
        console.log(timesheet_data)
        return {
            timesheet_data,
            sendData: async (newData) => {
                console.log("Sending data to server:", newData);
                await rpc("/ikon_employee/timesheet_form", newData); // Replace "/your_rpc_endpoint" with your actual RPC endpoint
            },
        }
    }
}

registry.category("services").add("TimesheetService", TimesheetService)