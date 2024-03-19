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
        activity = request.env['project.task'].search_read([('user_ids', '=', user.id)], ['name', 'project_id'])
        dates = request.env['account.analytic.line'].search_read([('user_id', '=', user.id)], ['date'], limit=7)
        hours = request.env['account.analytic.line'].search_read([('user_id', '=', user.id)], ['unit_amount', 'name', 'id', 'date'], limit=7)
        tes = request.env['account.analytic.line'].search_read([('user_id', '=', user.id)], ['unit_amount', 'name', 'id', 'date'])
        task_description = request.env['account.analytic.line'].search_read([('user_id', '=', user.id)], ['name'], limit=7)
        return {
            "project": project,
            "activity": activity,
            "date": dates,
            "hours": hours,
            "taskDescription": task_description,
            "tes": tes,
        }





