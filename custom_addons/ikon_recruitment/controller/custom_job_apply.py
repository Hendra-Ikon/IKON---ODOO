import base64

from odoo import http, fields, models
from odoo.http import request
import json


class ResumeTalent(http.Controller):

    @http.route("/resume", type="http", auth="user", website=True, csrf=False)
    def resume_view(self):
        user = request.env.user
        resume = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        applicant = request.env['hr.applicant'].search([("email_from", '=', user.email)])

        data = {}
        if resume:
            data = {
                'data': resume,
                'applicant': applicant,
            }

        return request.render("ikon_talent_management.resume_talent_view", data)