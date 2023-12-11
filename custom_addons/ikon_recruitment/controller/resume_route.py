
from odoo import http, fields, models
from odoo.http import request
import json

class ResumeTalent(http.Controller):

    @http.route("/resume", type="http", auth="user", website=True, csrf=False)
    def resume_view(self):

        return request.render("ikon_talent_management.resume_talent_view")
