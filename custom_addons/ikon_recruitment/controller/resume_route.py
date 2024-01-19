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
                        'resume_sys_int_appl': kwargs.get("resume_sys_int_appl"),
                        'resume_sys_int_middleware': kwargs.get("resume_sys_int_middleware"),
                        'resume_sys_int_email_notif': kwargs.get("resume_sys_int_email_notif"),
                        'company_image': base64.b64encode(image_data.read()),
                        # 'resume_tech_used_frontend': [
                        #     (6, 0, [tag.id for tag in kwargs.get("resume_tech_used_frontend")])],

                    })

                    applicant.update({
                        "custom_skill": kwargs.get("custom_skill"),
                        "summary_experience": kwargs.get("summary_experience"),
                    })

                    # print(kwargs.get("company_image"))
                    print(f"Data Image : {image_data.read()}")



            except Exception as e:
                print(f'Error Expected Salary {e}')

        return request.redirect('/resume')
        # 'resume_tech_used_backend': kwargs.get("resume_tech_used_backend"),
        # 'resume_tech_used_database': kwargs.get("resume_tech_used_database"),
        # 'resume_tech_used_certificate': kwargs.get("resume_tech_used_certificate"),

    @http.route("/create_applicant_custom_data", methods=['POST', 'GET'], type="http", auth="user", website=True, csrf=False)
    def create_applicant_custom_data(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        resume = request.env['custom.resume.experience'].search([])
        image_data = request.httprequest.files.get('company_image')

        if request.httprequest.method == 'POST':
            try:
                for applicant in applicant_to_update:

                    applicant.update({
                        "custom_skill": kwargs.get("custom_skill"),
                        "summary_experience": kwargs.get("summary_experience"),
                    })

                    # print(kwargs.get("company_image"))



            except Exception as e:
                print(f'create_applicant_custom_data {e}')

        return request.redirect('/resume')

    @http.route("/cv", methods=['POST', 'GET'], type="http", auth="user", website=True, csrf=False)
    def cv_view(self):
        user = request.env.user
        applicant = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        applicant_skill = request.env['hr.skill'].search([])
        skill_type = request.env['hr.skill.type'].search([])
        resume = request.env['hr.applicant'].search([("email_from", '=', user.email)])

        data = {}
        if applicant:
            data = {
                'applicant': applicant,
                'data': resume,
                'skill': applicant_skill,
                'skill_type': skill_type,

            }

        return request.render("ikon_talent_management.custom_cv_view", data)

