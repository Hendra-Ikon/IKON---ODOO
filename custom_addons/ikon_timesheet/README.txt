EXAMPLE QUERY

update approve

mutation {
    updateTimesheet(
        timesheetId: 322,
        action: "approve"
    ) {
        success
        timesheet {
            id
            name
            state
            status
            employeeId
            unitAmount
            date
            approvedDate
        }
    }
}

update reject

mutation {
    updateTimesheet(
        timesheetId: 322,
        action: "reject",
        reason: "Hours need adjustment"
    ) {
        success
        timesheet {
            id
            state
            status
            rejectedReason
            rejectedDate
        }
    }
}

create timesheet

mutation {
    createTimesheet(input: {
        name: "Development Task",
        projectId: 1,
        taskId: 2,
        unitAmount: 8.0,
        employeeId: 1,
        date: "2024-12-10"
    }) {
        success
        timesheet {
            id
            name
            state
            status
            employeeId
            unitAmount
            date
        }
    }
}

delete timesheet

mutation {
    deleteTimesheet(id: 322) {
        success
        message
    }
}

search all

query {
    timesheets{
        id
        name
        state
        status
    }
}

search by id

query {
    timesheet(id: 4) {
        id
        name
        state
        status
        employeeId
        unitAmount
        date
    }
}