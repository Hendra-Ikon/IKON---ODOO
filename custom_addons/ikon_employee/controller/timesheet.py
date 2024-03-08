
from odoo import http, fields, models
from odoo.fields import Date
from odoo.http import request


class CustomTimeSheetRoute(http.Controller):

    @http.route("/ikon_employee/timesheet_data", type="json", auth="user")
    def timesheet_data(self):
        user = request.env.user
        project = request.env['project.task'].search_read([('user_ids', '=', user.id)], ['project_id'])
        activity = request.env['project.task'].search_read([('user_ids', '=', user.id)], ['name'])
        return {
            "project": project,
            "activity": activity
        }

    @http.route("/ikon_employee/timesheet_form", type="json", auth="user")
    def timesheet_form(self, **kwargs):
        user = request.env.user
        activity = request.env['account.analytics.line'].search([('user_id', '=', user.id)])

        new_activity = activity.create({
            "date": fields.Date.Today(),
            "project_id": 3,
            "task_id": 7,
            "name": "Bagas Nganggur",
            "unit_amount": 8,
        })

        return True



