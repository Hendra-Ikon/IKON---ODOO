IKON Custom Timesheet module for odoo

This module was created for the purpose of establishing an API using graphene and graphql.
To start running the module please install the dependencies from the docker yaml file by removing the comment prompt and 
make sure the DB name follows with the DBfilter in odoo.conf. when accessing the odoo apps activate ikon timesheet, ikon custom employee, graphql_base.
After the apps are activated the API can be tested inside qraphql playground by the url graphiql/timesheet and graphiql/signin.
The queries for testing are provided below.

Modul ini dibuat untuk tujuan membangun API menggunakan graphene dan graphql. 
Untuk mulai menjalankan modul ini, harap instal dependensi dari file yaml docker dengan menghapus tanda komentar dan pastikan nama database sesuai dengan DBfilter di odoo.conf.
Saat mengakses aplikasi Odoo, aktifkan ikon timesheet, ikon custom employee, dan graphql_base. 
Setelah aplikasi diaktifkan, API dapat diuji di dalam graphql playground melalui URL graphiql/timesheet dan graphiql/signin.
Query untuk testing disediakan di bawah ini.


EXAMPLE QUERY signin

sign in to session

mutation {
    signin(
        db: "database_name",
        login: "user@example.com",
        password: "password"
    ) {
        sessionId
        userId
        username
        login
    }
}


Search session info

query {
    session {
        sessionId
        userId
        username
        login
    }
}

EXAMPLE QUERY Timesheet

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

