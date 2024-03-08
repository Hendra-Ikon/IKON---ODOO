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
            project_id: 3,
            task_id: 7,
            date: "2024-03-06",
            unit_amount: 0,
            name: "INI TEST BAGAS",

        })


        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            }
        })

        this.timesheet_service = useService("TimesheetService")
        // console.log(this.timesheet_service.timesheet_data)
        this.timesheet_data = this.timesheet_service.timesheet_data


        onMounted(() => {
            let selectedProject = document.getElementsByName('projectName')[0]

            selectedProject.addEventListener("change", selectProject);


            // console.log(selectedProject)

            function selectProject() {
                let val = selectedProject.options[selectedProject.selectedIndex].value;
                // console.log(value);
                // self.activityName = value
            }

            selectProject();


        })

        // Forms



        console.log("STATE LAMA", this.state)

        this.orm = useService("orm")
        this.model = "account.analytic.line"


    }


    send = async (form) =>  {

        this.state.unit_amount = form.unit_amount

        console.log("Halooooooooooooo", form)
        // this.state.workHours = form.workHours
        const new_data = {
            project_id: form.project_id,
            task_id: form.task_id,
            date: form.date,
            unit_amount: form.unit_amount,
            name: form.name,
        }
        //
        await this.orm.create(this.model, [new_data])

        // await this.timesheet_service.sendData(new_data).then(response => {
        //     console.log("Response from server:", response);
        //
        // }).catch(error => {
        //     console.error("Error:", error);
        // });

    }


}

CustomTimesheetComp.template = "ikon_employee.Timesheet"
CustomTimesheetComp.components = {Layout}

registry.category("actions").add("ikon_employee.Timesheet", CustomTimesheetComp);