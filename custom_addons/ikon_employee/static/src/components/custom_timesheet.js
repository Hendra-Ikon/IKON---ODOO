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
            id: 0, project_id: 0, task_id: 0, date: "2024-03-06", unit_amount: 0, name: "INI TEST BAGAS",

        })


        useSubEnv({
            config: {
                ...getDefaultConfig(), ...this.env.config,
            }
        })

        this.timesheet_service = useService("TimesheetService")
        this.timesheet_data = this.timesheet_service.timesheet_data
        this.hours = this.timesheet_service.timesheet_data.hours


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
            formData.id = parseInt(hour.id);
            formData.date = hour.date;
            allFormData.push(formData);
            ids.push(parseInt(hour.id));
        }
        for (let formData of allFormData) {

            await this.orm.write(this.model, [formData.id], formData);
        }
        // console.log("ID :", [allFormData[0].id], "FormData : ", allFormData[0])
        // await this.orm.write(this.model, [allFormData[0].id], allFormData[0]);


    }

    saveDescription = async (hours) => {
        event.preventDefault();
        console.log("Edited Description : ", hours);
    }

    formatDate(dateString) {
        const date = moment(dateString).format("ddd D");
        return date;
    }


}

export class CustomNoteTimesheet extends Component {

    setup() {

    }

}

CustomTimesheetComp.template = "ikon_employee.Timesheet"
CustomTimesheetComp.components = {Layout}

registry.category("actions").add("ikon_employee.Timesheet", CustomTimesheetComp);