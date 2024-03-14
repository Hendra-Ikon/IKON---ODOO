/** @odoo-module */

import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {getDefaultConfig} from "@web/views/view";
import {useService} from "@web/core/utils/hooks";

var Dialog = require('web.Dialog');

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

        this.notification = useService("notification")
        this.timesheet_service = useService("TimesheetService")
        this.timesheet_data = this.timesheet_service.timesheet_data
        this.hours = this.timesheet_service.timesheet_data.hours
        this.toogle_project = false
        this.selected_project = 0
        this.selected_task = 0

        console.log("Normal Activity", this.timesheet_data.activity)
        console.log("Selected Task", this.selected_task)
        //
        // let test_data = this.timesheet_data.activity.filter(data => {
        //     if(data.project_id[0] === 4) this.selected_task = data.project_id[0]
        //     // this.selected_task = data.project_id[0] === 4
        // })


        //
        // console.log(this.timesheet_data.activity)


        onMounted(() => {
            let selectedProject = document.getElementsByName('projectName')[0]
            let selectedTask = document.getElementsByName('activityProject')[0]
            // console.log("Selected Project", selectedProject)

            selectedProject.addEventListener("change", () => {
                let val = selectedProject.options[selectedProject.selectedIndex].value;
                this.toogle_project = true
                this.selected_project = val
                this.state.project_id = parseInt(val)
            });

            selectedTask.addEventListener("change", () => {
                let val = selectedTask.options[selectedTask.selectedIndex].value;
                this.state.task_id = parseInt(val)
            });

            // this.timesheet_data.activity.filter(select => {
            //         if (select.project_id[0] === 4) {
            //             this.selected_task = useState(select)
            //             console.log(select)
            //         }
            //     });

            // if (this.selected_project !== 0) {
            //     this.timesheet_data.activity.filter(select => {
            //         if (select.project_id[0] === 4) {
            //             this.selected_task = useState(select)
            //             console.log(select)
            //         }
            //     });
            // } else {
            //     // Handle the case where this.timesheet_data.activity is not defined or not an array
            //     console.error("this.toogle_project", this.toogle_project);
            //     console.error("this.selected_project", this.selected_project);
            // }
        });


        this.orm = useService("orm")
        this.model = "account.analytic.line"


    }


    send = async (form, hours) => {


        event.preventDefault();


        if (form.project_id === 0 || form.task_id === 0) {
            Dialog.alert(this, "Please select Project and Activity", {
                title: "Validation Error",
                size: 'medium',
                buttons: [{
                    text: "Ok",
                    close: true,
                    style: "background-color: darkorange; color: white;",
                }]
            });

        } else {
            const allFormData = [];

            for (let hour of hours) {
                const formData = {...this.state};
                formData.unit_amount = parseInt(hour.unit_amount);
                formData.id = parseInt(hour.id);
                formData.date = hour.date;
                formData.name = hour.name;
                allFormData.push(formData);
                // console.log("Form :", formData)
            }
            for (let formData of allFormData) {

                await this.orm.write(this.model, [formData.id], formData);
            }
            this.notification.add("Successfully add new timesheet", {title: "Success", type: "info"});
        }


        // Collect all form data from each row


    }

    saveDescription = async (hours) => {
        event.preventDefault();
        const newDescription = document.getElementById(`description${hours.id}`).value;

        hours.name = newDescription
    }

    formatDate(dateString) {
        const date = moment(dateString).format("ddd D");
        return date;
    }


}


CustomTimesheetComp.template = "ikon_employee.Timesheet"
CustomTimesheetComp.components = {Layout}

registry.category("actions").add("ikon_employee.Timesheet", CustomTimesheetComp);