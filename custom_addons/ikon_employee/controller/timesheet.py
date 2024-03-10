import logging
from datetime import datetime, timedelta

from odoo import http, fields, models
from odoo.fields import Date
from odoo.http import request

_logger = logging.getLogger(__name__)



class CustomTimeSheetRoute(http.Controller):

    @http.route("/ikon_employee/timesheet_data", type="json", auth="user")
    def timesheet_data(self):
        user = request.env.user
        project = request.env['project.task'].search_read([('user_ids', '=', user.id)], ['project_id'])
        activity = request.env['project.task'].search_read([('user_ids', '=', user.id)], ['name'])
        dates = request.env['account.analytic.line'].search_read([('user_id', '=', user.id)], ['date'], limit=7)
        hours = request.env['account.analytic.line'].search_read([('user_id', '=', user.id)], ['unit_amount'], limit=7)
        return {
            "project": project,
            "activity": activity,
            "date": dates,
            "hours": hours
        }

    # @http.route("/ikon_employee/timesheet_data", type="json", auth="user")
    # def timesheet_data(self):
    #     user = request.env.user
    #
    #     # Calculate start and end dates of the current week
    #     # today = datetime.now()
    #     # start_of_week = today - timedelta(days=today.weekday())
    #     # end_of_week = start_of_week + timedelta(days=6)
    #     project = request.env['project.task'].search_read([('user_ids', '=', user.id)], ['project_id'])
    #     activity = request.env['project.task'].search_read([('user_ids', '=', user.id)], ['name'])
    #
    #     # Generate list of days and dates for the week
    #     days_and_dates = request.env['project.task'].search_read([('user_ids', '=', user.id)], ['date'])
    #     # days_and_dates = []
    #     # for i in range(7):
    #     #     day = (start_of_week + timedelta(days=i)).strftime('%a')
    #     #     date = (start_of_week + timedelta(days=i)).strftime('%d')
    #     #     days_and_dates.append({'day': day, 'date': date})
    #     #
    #     # project = request.env['project.task'].search_read([
    #     #     ('user_ids', '=', user.id),
    #     #     ('date', '>=', start_of_week),
    #     #     ('date', '<=', end_of_week)
    #     # ], ['project_id'])
    #     #
    #     # activity = request.env['project.task'].search_read([
    #     #     ('user_ids', '=', user.id),
    #     #     ('date', '>=', start_of_week),
    #     #     ('date', '<=', end_of_week)
    #     # ], ['name'])
    #     #
    #     _logger.info("timesheet_data: %s", {
    #         "days_and_dates": days_and_dates
    #     })
    #
    #     return {
    #         "project": project,
    #         "activity": activity,
    #         "days_and_dates": days_and_dates
    #     }

    # @http.route("/ikon_employee/timesheet_form", type="json", auth="user")
    # def timesheet_form(self, **kwargs):
    #     user = request.env.user
    #     activity = request.env['account.analytics.line'].search([('user_id', '=', user.id)])
    #
    #     new_activity = activity.create({
    #         "date": fields.Date.Today(),
    #         "project_id": 3,
    #         "task_id": 7,
    #         "name": "Bagas Nganggur",
    #         "unit_amount": 8,
    #     })
    #
    #     return True



