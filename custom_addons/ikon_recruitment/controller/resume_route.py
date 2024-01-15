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

    @http.route("/create_resume", methods=['POST', 'GET'], type="http", auth="user", website=True, csrf=False)
    def create_resume(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        resume = request.env['custom.resume.experience'].search([])
        image_data = request.httprequest.files.get('company_image')

        if request.httprequest.method == 'POST':
            try:
                for applicant in applicant_to_update:
                    resume.create({
                        'applicant_id': applicant.id,
                        'resume_dateStart': kwargs.get("resume_dateStart"),
                        'resume_dateEnd': kwargs.get("resume_dateEnd"),
                        'rsm_com_name': kwargs.get("rsm_com_name"),
                        'rsm_com_job_title': kwargs.get("rsm_com_job_title"),
                        'rsm_com_projectDes': kwargs.get("rsm_com_projectDes"),
                        'resume_tech_used_frontend': kwargs.get("resume_tech_used_frontend"),
                        'resume_tech_used_backend': kwargs.get("resume_tech_used_backend"),
                        'resume_tech_used_database': kwargs.get("resume_tech_used_database"),
                        'company_image': image_data.read(),
                        # 'resume_tech_used_frontend': [
                        #     (6, 0, [tag.id for tag in kwargs.get("resume_tech_used_frontend")])],

                    })

                    # print(kwargs.get("company_image"))
                    print(f"Data Image : {image_data.read()}")



            except Exception as e:
                print(f'Error Expected Salary {e}')

        return request.redirect('/resume')
        # 'resume_tech_used_backend': kwargs.get("resume_tech_used_backend"),
        # 'resume_tech_used_database': kwargs.get("resume_tech_used_database"),
        # 'resume_tech_used_certificate': kwargs.get("resume_tech_used_certificate"),


