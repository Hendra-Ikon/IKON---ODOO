/** @odoo-module */

import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { getDefaultConfig } from "@web/views/view";
import { useService } from "@web/core/utils/hooks";

var Dialog = require('web.Dialog');

const { Component, useSubEnv, useState, onMounted, reactive, onPatched } = owl;

export class CustomTimesheetComp extends Component {
    setup() {
        this.state = useState({
            id: 0, project_id: 0, task_id: 0, date: "2024-03-06", unit_amount: 0, name: "Description task",
        });

        useSubEnv({
            config: {
                ...getDefaultConfig(), ...this.env.config,
            }
        });

        this.orm = useService("orm");
        this.model = "account.analytic.line";
        this.notification = useService("notification");
        this.timesheet_service = useService("TimesheetService");
        this.timesheet_data = this.timesheet_service.timesheet_data;
        this.hours = this.timesheet_service.timesheet_data.hours;
        this.selected_date_index = useState({
            dateIndex: 0
        });
        this.toggleData = useState({
            weekLeft: false
        });
        this.selected_project = 0;
        this.select_activity = useState([]);

        const sortedData = this.timesheet_data.tes.map(item => ({
            ...item,
            date: new Date(item.date)
        })).sort((a, b) => a.date - b.date);

        const formatWeek = function (week) {
            const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            const formattedDays = [];
        
            for (let date of week.dates) {
                const currentDate = new Date(date);
                const dayIndex = (currentDate.getDay() + 6) % 7;
                const day = days[dayIndex];
                const formattedDate = currentDate.toDateString();
                formattedDays.push({ date: formattedDate, id: currentDate.getDate(), name: day, unit_amount: 0 });
            }
        
            return formattedDays;
        };
        
        const getWeeksInYear = function (year) {
            const weeks = [];
            let currentWeek = [];
            let startDate = new Date(year, 0, 1);
        
            if (startDate.getDay() !== 1) {
                startDate.setDate(startDate.getDate() - (startDate.getDay() === 0 ? 6 : startDate.getDay() - 1));
            }
        
            while (startDate.getFullYear() <= year) {
                currentWeek.push(new Date(startDate));
        
                if (startDate.getDay() === 0) {
                    weeks.push({ dates: currentWeek });
                    currentWeek = [];
                }
        
                startDate.setDate(startDate.getDate() + 1);
            }
        
            if (currentWeek.length) {
                weeks.push({ dates: currentWeek });
            }
        
            return weeks;
        };
        
        const currentYear = new Date().getFullYear();
        const allWeeks = getWeeksInYear(currentYear);
        
        const weekData = allWeeks.map(week => {
            const startDate = week.dates[0];
            const endDate = week.dates[week.dates.length - 1];
            const range = `${startDate.toDateString()} to ${endDate.toDateString()}`;
            const data = formatWeek(week);
            return { range, data };
        });
        
        weekData.sort((a, b) => weekData.indexOf(b) - weekData.indexOf(a));
        
        this.weekData = weekData;
        this.usedData = reactive(weekData[this.selected_date_index.dateIndex].data);
        this.timesheet_date_header = weekData[this.selected_date_index.dateIndex].range;

        onMounted(() => {
            let selectedProject = document.getElementsByName('projectSearch')[0];
            let selectedTask = document.getElementsByName('activityProject')[0];
            let startDate = document.getElementsByName('startDates')[0];

            if (selectedProject) {
                selectedProject.addEventListener("change", () => {
                    let val = selectedProject.options[selectedProject.selectedIndex].value;
                    this.state.project_id = parseInt(val);
                });
            }

            if (selectedTask) {
                selectedTask.addEventListener("change", () => {
                    let val = selectedTask.options[selectedTask.selectedIndex].value;
                    console.log("FROM TASK", val);
                    this.state.task_id = parseInt(val);
                });
            }

            if (startDate) {
                startDate.addEventListener("change", async () => {
                    let val = await startDate.selectedIndex;
                    this.selected_date_index.dateIndex = await val;
                    this.usedData = await reactive(weekData[val].data);
                    this.timesheet_date_header = weekData[val].range;

                    console.log("usedData: ", this.usedData);
                    console.log(this.selected_date_index.dateIndex);
                    console.log("test");
                });
            }
        });

        onPatched(() => {
            if (this.toggleData.weekLeft === true) {
                let projectSearchInput = document.getElementById('projectSearch');
                const projectList = document.querySelector('.list-group');
                const activitySelect = document.getElementById('initialRows_0_projectActivityName');
                const hiddenInput = document.getElementById('initialRows_0_projectActivityId');
        
                if (projectSearchInput) {
                    projectSearchInput.addEventListener("input", filterList);
        
                    function filterList() {
                        const filter = projectSearchInput.value.toLowerCase();
                        const items = document.querySelectorAll(".list-group-item");
        
                        items.forEach(item => {
                            let text = item.textContent.toLowerCase();
                            if (text.includes(filter)) {
                                item.style.display = "block";
                            } else {
                                item.style.display = "none";
                            }
                        });
                    }
                }
        
                if (projectList) {
                    projectList.addEventListener('click', (event) => {
                        if (event.target && event.target.classList.contains('list-group-item')) {
                            const projectId = event.target.getAttribute('value');
                            const projectName = event.target.textContent;
        
                            this.selected_project = parseInt(projectId);
                            console.log("Selected Project ID:", this.selected_project);
        
                            projectSearchInput.value = projectName;
        
                            const selectedProjectData = this.timesheet_data.activity.filter(data => data.project_id[0] === this.selected_project);
                            if (selectedProjectData) {
                                this.select_activity = reactive(selectedProjectData);
                                console.log("Selected Project Data:", this.select_activity);
        
                                updateActivitySelect(selectedProjectData);
                            }
        
                            const items = document.querySelectorAll(".list-group-item");
                            items.forEach(item => {
                                item.style.display = "none";
                            });
                        }
                    });
                }
        
                function updateActivitySelect(activities) {
                    activitySelect.innerHTML = '<option value="-1">-- Select --</option>';
                    
                    activities.forEach(activity => {
                        let option = document.createElement('option');
                        option.value = activity.id;
                        option.textContent = activity.name;
                        activitySelect.appendChild(option);
                    });
                }
        
                activitySelect.addEventListener('change', (event) => {
                    const selectedActivityId = event.target.value;
                    console.log("Selected Activity ID:", selectedActivityId);
        
                    hiddenInput.value = selectedActivityId;
                });
            }
        });
    }

    send = async (form, hours) => {
        event.preventDefault();

        const formDataArray = [];
        const formElement = document.getElementById('timesheetForm');
        
        // Get form data
        const formData = new FormData(formElement);

        // Extract form data into an array of objects
        for (let hour of hours) {
            const descriptionInput = document.getElementById(`description${hour.id}`);
            console.log("descriptionInput", descriptionInput)
            const name = descriptionInput.value;

            const formDataEntry = {
                ...this.state,
                unit_amount: parseInt(hour.unit_amount),
                product_uom_id:4,
                account_id:2,
                user_id:1,
                company_id:1,
                employee_id:1,
                department_id:1,
                timesheet_invoice_type:"non_billable",

                date: this.formatDateForForm(hour.date),
                name: name,
                project_id: this.selected_project,
                task_id: parseInt(formData.get('activityProject'))
            };

            formDataArray.push(formDataEntry);
        }

        console.log("formDataArray",formDataArray)

        if (this.state.project_id === 1 || this.state.task_id === 1) {
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
            for (let formDataEntry of formDataArray) {

                await this.orm.create(this.model, [formDataEntry]);
            }
            this.notification.add("Successfully add new timesheet", { title: "Success", type: "info" });
        }
    }

    edit = async () => {
        if (this.toggleData.weekLeft === false) {
            this.toggleData.weekLeft = true;
        }
    }
    addRow = async () => {
        // Pastikan timesheet_data dan project ada
        if (this.timesheet_data && this.timesheet_data.project) {
            const newRowData = { date: "", unit_amount: 0, name: "" }; // Data baru dengan nilai awal kosong
            this.usedData.push(newRowData); // Menambahkan data baru ke array usedData
        
            // Mengambil elemen tabel
            const tableBody = document.querySelector('.table tbody');
        
            // Membuat elemen baris baru
            const newRow = document.createElement('tr');
            console.log("1",this.timesheet_data.project)
            // Menambahkan elemen sel ke dalam baris baru
            newRow.innerHTML = `
                <td id="">
                    <input class="toDelete" type="checkbox" name="initialRows[0][toDelete]" id="initialRows_0_toDelete"/>
                </td>
                <td>
                    <div class="projectInputWrapper">
                        <input type="text" class="projectSearch" style="width:225px" placeholder="Search for a project..." id="projectSearch" name="projectSearch"/>
                        
                        <ul class="list-group" style="width:225px">
                            ${this.timesheet_data.project.map(project => `
                                <li class="list-group-item" value="${project.id}">
                                    ${project.name}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                </td>
                <td>
                    <select class="projectActivity" style="width:225px" name="activityProject" id="initialRows_0_projectActivityName">
                        <option value="-1">-- Select --</option>
                        ${this.select_activity.map(activity => `
                            <option value="${activity.id}">
                                ${activity.name}
                            </option>
                        `).join('')}
                    </select>
                    <input type="hidden" name="initialRows[0][projectActivityId]" id="initialRows_0_projectActivityId"/>
                </td>
            `;
        
            // Menambahkan baris baru ke dalam tabel
            tableBody.appendChild(newRow);
        } else {
            // Handle empty or undefined timesheet_data
            console.error("timesheet_data or project is empty or undefined.");
        }
    }
    
    
    
    

    cancel = async () => {
        if (this.toggleData.weekLeft === true) {
            this.toggleData.weekLeft = false;
        }

        this.usedData = reactive(this.weekData[0].data);
        location.reload();
    }

    saveDescription = async (hours) => {
        event.preventDefault();
        const newDescription = document.getElementById(`description${hours.id}`).value;

        hours.name = newDescription;

        const modalId = `exampleModal${hours.id}`;
        const modalElement = document.querySelector(`#${modalId}`);
        if (modalElement) {
            modalElement.classList.remove("show");
        }
        this.notification.add("Successfully add new task", { title: "Success", type: "info" });
    }

    formatDate(dateString) {
        const date = moment(dateString).format("ddd D");
        return date;
    }

    formatDateheader(dateString) {
        let day = dateString.substring(0, 3);
        let date = dateString.substring(8, 10);
        return day + " " + date;
    }

    formatDateForForm(stringDATA) {
        let dateObject = new Date(stringDATA);

        let year = dateObject.getFullYear();
        let month = String(dateObject.getMonth() + 1).padStart(2, '0');
        let day = String(dateObject.getDate()).padStart(2, '0');

        let formattedDate = `${year}-${month}-${day}`;
        return formattedDate;
    }
}

CustomTimesheetComp.template = "ikon_employee.Timesheet";
CustomTimesheetComp.components = { Layout };

registry.category("actions").add("ikon_employee.Timesheet", CustomTimesheetComp);
