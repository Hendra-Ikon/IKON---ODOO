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
                const textInput = document.getElementById('initialRows_0_projectActivityId');
        
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
        
                    textInput.value = selectedActivityId;
                });
            }
        });
    }

    send = async (form, hours) => {
        event.preventDefault();
    
        const formDataArray = [];
        const formElement = document.getElementById('timesheetForm');
        const formData = new FormData(formElement);

    
        console.log("hours", hours);
        
        
        
        this.timesheet_data.project.forEach((project) => {
            const unitAmounts = [];
            hours.forEach((hour, index) => {
                const hourId = `initialRows_${project.id}_${hour.id}_${index}`;
                const unitAmountElement = document.getElementById(hourId);
                const unitAmount = unitAmountElement ? parseFloat(unitAmountElement.value) : null;
        
                // if (unitAmount !== null && !isNaN(unitAmount)) {
                //     unitAmounts.push(unitAmount);
                // } else {
                //     unitAmounts.push(hour.unit_amount);
                // }
                console.log("unitAmount", unitAmount)
                console.log("hour.unit_amount", hour.unit_amount)
                unitAmounts.push(unitAmount);
                unitAmounts.push(hour.unit_amount);
                
                // unitAmounts.push(unitAmount)
                // unitAmounts.push(hour.unit_amount)
                if (this.addRow) {
                    let descriptionInput = "test";
    
                    if (descriptionInput) {
                        const name = descriptionInput;
    
                        const formDataEntry = {
                            ...this.state,
                            unit_amount: unitAmount,
                            product_uom_id: 4,
                            account_id: 2,
                            user_id: 1,
                            company_id: 1,
                            employee_id: 1,
                            department_id: 1,
                            timesheet_invoice_type: "non_billable",
                            date: hour.date,
                            name: name,
                            project_id: project.id,
                            task_id: this.select_activity[0].id,
                        };
                        formDataArray.push(formDataEntry);
                    }
                }
            });
            console.log("unitAmounts", unitAmounts);
        });
       
        console.log("FormDataArray", formDataArray);
    };
    

    
    
    // edit = async () => {
    //     if (this.toggleData.weekLeft === false) {
    //         this.toggleData.weekLeft = true;
           
    //     }
    // }
    add = async () => {
       

        var table = document.getElementById("myTable");

        // Membuat baris baru
        var newRow = table.insertRow();

        // Membuat sel baru dan mengisinya dengan konten
        var cell1 = newRow.insertCell(0);
        var cell2 = newRow.insertCell(1);

        // Menambahkan teks ke sel
        cell1.innerHTML = "Data 1";
        cell2.innerHTML = "Data 2";

    }

    addRow = async () => {
        try {
            // Toggle weekLeft if it's false
            if (this.toggleData.weekLeft === false) {
                this.toggleData.weekLeft = true;
                this.addRow();
            }
    
            // Ensure timesheet_data and project exist
            if (this.timesheet_data && this.timesheet_data.project) {
                const newRowData = { id: this.usedData.length + 1, date: "", unit_amount: 0, name: "" };
    
                // Add new data to usedData array if less than 7
                if (this.usedData.length < 7) {
                    this.usedData.push(newRowData);
                } else {
                    this.usedData[this.usedData.length - 1] = newRowData;
                }
    
                // Get the table body element
                const tableBody = document.querySelector('.table tbody');
                
 
    
                // Create a new row element
                const newRow = document.createElement('tr');
    
                // Add cell elements to the new row
                newRow.innerHTML = `
                    <td>
                        <input class="toDelete" type="checkbox" name="initialRows[${newRowData.id}][toDelete]" id="initialRows_${newRowData.id}_toDelete"/>
                    </td>
                    <td>
                        <div class="projectInputWrapper">
                            <input type="text" class="projectSearch" style="width:225px" placeholder="Search for a project..." id="projectSearch_${newRowData.id}" name="projectSearch_${newRowData.id}"/>
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
                        <select class="projectActivity" style="width:225px" name="activityProject_${newRowData.id}" id="initialRows_${newRowData.id}_projectActivityName">
                            <option value="-1">-- Select --</option>
                            ${this.select_activity.map(activity => `
                                <option value="${activity.id}">
                                    ${activity.name}
                                </option>
                            `).join('')}
                        </select>
                        <input type="hidden" name="initialRows[${newRowData.id}][projectActivityId]" id="initialRows_${newRowData.id}_projectActivityId"/>
                    </td>
                    ${this.usedData.map((hour, index) => `
                    <td class="comments">
                        <div class="comment_wrapper">
                            <input align="center" class="timeBox" type="text"
                                   name="initialRows[${newRowData.id}][${hour.id}]"
                                   id="initialRows_${newRowData.id}_${hour.id}_${index}" t-model="hour.unit_amount" value="${hour.unit_amount}"/>
                            <img class="commentIcon" data-bs-toggle="modal"
                                 t-att-data-bs-target="'#exampleModal' + ${hour.id}"
                                 src="/ikon_recruitment/static/src/img/comment.png"/>
    
                            <input type="hidden" name="taskId" t-model="state.task_id"
                                   t-att-value="'1'"
                                   value="'1'" id="taskId_${hour.id}_${index}"/>
    
                            <input type="hidden" name="projectId" t-model="state.project_id"
                                   t-attf-value="dataProjectId" value="dataProjectId"
                                   id="projectId_${hour.id}_${index}"/>
    
                            <input type="hidden" name="dataId" t-model="hour.id"
                                   t-attf-value="hour.id" value="${hour.id}" id="dataId_${newRowData.id}_${hour.id}_${index}"/>
    
                            <input type="hidden" name="dateId" t-model="hour.date"
                                   t-attf-value="hour.date" value="${hour.date}" id="dateId_${newRowData.id}_${hour.id}_${index}"/>
    
                            <div class="modal fade" t-att-id="'exampleModal' + ${hour.id}"
                                 tabindex="-1"
                                 aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h1 class="modal-title fs-5" id="exampleModalLabel">
                                                Add
                                                New
                                                Task
                                            </h1>
                                            <button type="button" class="btn-close"
                                                    data-bs-dismiss="modal"
                                                    aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <div class="mb-3 row">
                                                <label for="name"
                                                       class="col-sm-2 col-form-label">
                                                    Task
                                                    Description
                                                </label>
                                                <div class="col-sm-10">
                                                    <input type="text" class="form-control"
                                                           id="description${hour.id}_${index}"
                                                           name="description"
                                                           value=""/>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary"
                                                    data-bs-dismiss="modal">Close
                                            </button>
                                            <button type="button" class="btn btn-primary"
                                                    t-on-click="() => saveDescription(hour)">
                                                Save
                                                changes
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </td>
                `).join('')}
                `;
    
                // Add the new row to the table
                tableBody.appendChild(newRow);
    
                const projectSearchInput = newRow.querySelector(`#projectSearch_${newRowData.id}`);
                const projectListItems = newRow.querySelectorAll('.list-group-item');
    
                // Filter project list based on search input
                if (projectSearchInput) {
                    projectSearchInput.addEventListener("input", filterList);
    
                    function filterList() {
                        const filter = projectSearchInput.value.toLowerCase();
                        projectListItems.forEach(item => {
                            let text = item.textContent.toLowerCase();
                            if (text.includes(filter)) {
                                item.style.display = "block";
                            } else {
                                item.style.display = "none";
                            }
                        });
                    }
                }
    
                // Select project and update activities
                projectListItems.forEach(item => {
                    item.addEventListener('click', (event) => {
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
    
                            projectListItems.forEach(item => {
                                item.style.display = "none";
                            });
                        }
                    });
                });
    
                function updateActivitySelect(activities) {
                    const activitySelect = newRow.querySelector(`#initialRows_${newRowData.id}_projectActivityName`);
                    if (!activitySelect) {
                        console.error("Activity select element not found.");
                        return;
                    }
    
                    activitySelect.innerHTML = '<option value="-1">-- Select --</option>';
    
                    activities.forEach(activity => {
                        let option = document.createElement('option');
                        option.value = activity.id;
                        option.textContent = activity.name;
                        activitySelect.appendChild(option);
                    });
                }
            } else {
                // Handle empty or undefined timesheet_data
                console.error("timesheet_data or project is empty or undefined.");
            }
        } catch (error) {
            console.error("An error occurred:", error);
        }
    };
    
    
    
    
    

    cancel = async () => {
        if (this.toggleData.weekLeft === true) {
            this.toggleData.weekLeft = false;
        }

        this.usedData = reactive(this.weekData[0].data);
        // location.reload();
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
