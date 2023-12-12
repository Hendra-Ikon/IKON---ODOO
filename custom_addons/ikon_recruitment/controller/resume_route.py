
from odoo import http, fields, models
from odoo.http import request
import json

class ResumeTalent(http.Controller):

    @http.route("/resume", type="http", auth="user", website=True, csrf=False)
    def resume_view(self):
        user = request.env.user
        resume = request.env['hr.applicant'].search([("email_from", '=', user.email)])

        data = {}
        if resume:
            data = {
                'data': resume,
            }

        return request.render("ikon_talent_management.resume_talent_view", data)

    # @http.route("/create_resume", type="http", auth="user", website=True, csrf=False)
    # def create_resume(self, **kwargs):
    #     user = request.env.user
    #     applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
    #     resume = request.env['custom.resume.experience'].search([])
    #
    #
    #     if request.httprequest.method == 'POST':
    #         try:
    #             for applicant in applicant_to_update:
    #                 resume.create({
    #                     'applicant_id': applicant.id,
    #                     'resume_dateStart': kwargs.get("resume_dateStart"),
    #                     'resume_dateEnd': kwargs.get("resume_dateEnd"),
    #                     'resume_company_name': kwargs.get("resume_company_name"),
    #                     'resume_company_job_title': kwargs.get("resume_company_job_title"),
    #                     'resume_company_projectDes': kwargs.get("resume_company_projectDes"),
    #                 })
    #
    #         except Exception as e:
    #             print(f'Error Expected Salary {e}')
    #     return request.redirect('/resume')
