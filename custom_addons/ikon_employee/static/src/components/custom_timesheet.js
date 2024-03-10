/** @odoo-module */

import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {getDefaultConfig} from "@web/views/view";
import {useService} from "@web/core/utils/hooks";
// import {useEffect} from "@web/lib/owl/owl";

const {Component, useSubEnv, useState, onMounted} = owl

export class CustomTimesheetComp extends Component {
    setup() {
        console.log("Sukses custom timesheet")
        this.state = useState({
            project_id: 0, task_id: 0, date: "2024-03-06", unit_amount: 0, name: "INI TEST BAGAS",

        })


        useSubEnv({
            config: {
                ...getDefaultConfig(), ...this.env.config,
            }
        })

        this.timesheet_service = useService("TimesheetService")
        // console.log(this.timesheet_service.timesheet_data)
        this.timesheet_data = this.timesheet_service.timesheet_data
        this.hours = this.timesheet_service.timesheet_data.hours
        console.log(this.hours[0].unit_amount)


        onMounted(() => {
            let selectedProject = document.getElementsByName('projectName')[0]
            let selectedTask = document.getElementsByName('activityProject')[0]

            selectedProject.addEventListener("change", () => {
                let val = selectedProject.options[selectedProject.selectedIndex].value;
                this.state.project_id = parseInt(val)
            });

            selectedTask.addEventListener("change", () => {
                let val = selectedTask.options[selectedTask.selectedIndex].value;
                this.state.task_id = parseInt(val)
            });
        });


        console.log("STATES", this.state)

        this.orm = useService("orm")
        this.model = "account.analytic.line"


    }


    send = async (form, hours) => {


        event.preventDefault();

        // Collect all form data from each row
        const allFormData = [];
        for (let hour of hours) {
            const formData = {...this.state};
            formData.unit_amount = parseInt(hour.unit_amount);
            allFormData.push(formData);
        }


        for (let formData of allFormData) {
            await this.orm.create(this.model, [formData]);
        }
        // await this.orm.create(this.model, new_data)
        console.log("All form data:", allFormData);


    }

    formatDate(dateString) {
        const date = moment(dateString).format("ddd D");
        return date;
    }


}

CustomTimesheetComp.template = "ikon_employee.Timesheet"
CustomTimesheetComp.components = {Layout}

registry.category("actions").add("ikon_employee.Timesheet", CustomTimesheetComp);