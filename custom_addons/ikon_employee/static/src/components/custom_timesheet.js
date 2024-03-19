/** @odoo-module */

import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {getDefaultConfig} from "@web/views/view";
import {useService} from "@web/core/utils/hooks";

var Dialog = require('web.Dialog');

const {Component, useSubEnv, useState, onMounted, reactive} = owl

export class CustomTimesheetComp extends Component {
    setup() {
        this.state = useState({
            id: 0, project_id: 0, task_id: 0, date: "2024-03-06", unit_amount: 0, name: "Description task",

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
        this.selected_date_index = useState({
            dateIndex: 0
        })
        this.toggleData = useState({
            weekLeft: false
        })


        // Parse dates and sort the array
        const sortedData = this.timesheet_data.tes.map(item => ({
            ...item,
            date: new Date(item.date)
        })).sort((a, b) => a.date - b.date);

        // Group the sorted array into weeks
        const weeks = [];
        let currentWeek = [];
        let previousDayOfWeek = -1;

        sortedData.forEach(item => {
            const dayOfWeek = item.date.getDay();
            if (dayOfWeek === 1 && previousDayOfWeek !== 1 && currentWeek.length > 0) {
                weeks.push([...currentWeek]);
                currentWeek = [];
            }
            currentWeek.push(item);
            previousDayOfWeek = dayOfWeek;
        });

        // Add the last week
        if (currentWeek.length > 0) {
            weeks.push([...currentWeek]);
        }

        // Create weekData array with range and data
        const weekData = weeks.map(week => {
            const startDate = week[0].date;
            const endDate = week[week.length - 1].date;
            const dataInRange = week.map(item => ({
                id: item.id,
                unit_amount: item.unit_amount,
                name: item.name,
                date: item.date.toDateString(),
            }));
            return {
                range: `${startDate.toDateString()} to ${endDate.toDateString()}`,
                data: dataInRange
            };
        });


        weekData.sort(function (a, b) {
            return weekData.indexOf(b) - weekData.indexOf(a);
        })
        this.weekData = weekData

        this.usedData = reactive(weekData[this.selected_date_index.dateIndex].data)

        this.timesheet_date_header = weekData[this.selected_date_index.dateIndex].range

        console.log(this.timesheet_date_header)


        onMounted(() => {
            let selectedProject = document.getElementsByName('projectName')[0]
            let selectedTask = document.getElementsByName('activityProject')[0]
            let startDate = document.getElementsByName('startDates')[0]

            if (selectedProject) {

                selectedProject.addEventListener("change", () => {
                    let val = selectedProject.options[selectedProject.selectedIndex].value;
                    this.state.project_id = parseInt(val)
                });
            }

            if (selectedTask) {

                selectedTask.addEventListener("change", () => {
                    let val = selectedTask.options[selectedTask.selectedIndex].value;
                    this.state.task_id = parseInt(val)
                });
            }

            if (startDate) {
                startDate.addEventListener("change", async () => {
                    let val = await startDate.selectedIndex
                    this.selected_date_index.dateIndex = await val
                    this.usedData = await reactive(weekData[val].data)
                    this.timesheet_date_header = weekData[val].range

                    console.log("usedData : ", this.usedData);
                    console.log(this.selected_date_index.dateIndex)

                });

            }


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

        console.log(this.formatDateForForm("Tue Mar 26 2024"))

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
                formData.date = this.formatDateForForm(hour.date);
                formData.name = hour.name;
                allFormData.push(formData);
                // console.log("Form :", formData)
            }
            for (let formData of allFormData) {

                await this.orm.write(this.model, [formData.id], formData);
            }
            this.notification.add("Successfully add new timesheet", {title: "Success", type: "info"});
        }


    }

    edit = async () => {
        if (this.toggleData.weekLeft === false) {

            this.toggleData.weekLeft = true
        }
    }

    cancel = async () => {
        if (this.toggleData.weekLeft === true) {

            this.toggleData.weekLeft = false
        }


        this.usedData = reactive(this.weekData[0].data)
        location.reload()

        // this.usedData = await reactive(this.weekData[1].data)

    }

    saveDescription = async (hours) => {
        event.preventDefault();
        const newDescription = document.getElementById(`description${hours.id}`).value;

        hours.name = newDescription

        const modalId = `exampleModal${hours.id}`;
        const modalElement = document.querySelector(`#${modalId}`);
        console.log(modalElement)
        if (modalElement) {
            modalElement.classList.remove("show")
        }
        this.notification.add("Successfully add new task", {title: "Success", type: "info"});

    }

    formatDate(dateString) {
        const date = moment(dateString).format("ddd D");
        return date;
    }

    formatDateheader(dateString) {
        let day = dateString.substring(0, 3)
        let date = dateString.substring(8, 10)
        return day + " " + date
    }

    formatDateForForm(stringDATA) {


        let dateObject = new Date(stringDATA);

        let year = dateObject.getFullYear();
        let month = String(dateObject.getMonth() + 1).padStart(2, '0');
        let day = String(dateObject.getDate()).padStart(2, '0');

        let formattedDate = `${year}-${month}-${day}`;
        return formattedDate

    }


}


CustomTimesheetComp.template = "ikon_employee.Timesheet"
CustomTimesheetComp.components = {Layout}

registry.category("actions").add("ikon_employee.Timesheet", CustomTimesheetComp);