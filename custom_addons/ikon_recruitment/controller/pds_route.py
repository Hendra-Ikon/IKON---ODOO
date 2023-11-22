import os
from odoo import http, fields
from odoo.http import request
import json


class PDSController(http.Controller):

    @http.route("/tes/popup", type='http', auth='none', website=True, csrf=False)
    def open_popup(self):
        return request.render("ikon_recruitment.tes_popup")


    @http.route("/edit_cert/<int:cert_id>", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def edit_cert(self, cert_id, **kwargs):
        cert_record = request.env['custom.certif'].browse(cert_id)
        # cert_record = request.env['hr.applicant'].search([("pds_certifications", "=", cert_id)])
        cert_record.write({
            'pds_cert_name': kwargs.get('pds_cert_name'),
            'pds_cert_provider': kwargs.get('pds_cert_provider'),
            'pds_cert_issued_year': kwargs.get('pds_cert_issued_year'),
        })
        return request.redirect('/pds/data')

    @http.route("/remove_cert/<int:cert_id>", methods=['POST', 'GET'], type='http', auth='user', website=True,
                csrf=False)
    def remove_cert(self, cert_id):
        cert_record = request.env['custom.certif'].browse(cert_id)
        cert_record.unlink()
        return request.redirect('/pds/data')

    @http.route("/delete_edu/<int:edu_id>", methods=['POST', 'GET'], type='http', auth='user', website=True,
                csrf=False)
    def delete_edu(self, edu_id):
        edu_record = request.env['custom.edu'].browse(edu_id)
        edu_record.unlink()
        return request.redirect('/pds/data')

    @http.route("/delete_nonfromedu/<int:edu_id>", methods=['POST', 'GET'], type='http', auth='user', website=True,
                csrf=False)
    def delete_nonfromedu(self, edu_id):
        nonedu_record = request.env['custom.nonformaledu'].browse(edu_id)
        nonedu_record.unlink()
        return request.redirect('/pds/data')

    @http.route("/delete_language/<int:edu_id>", methods=['POST', 'GET'], type='http', auth='user', website=True,
                csrf=False)
    def delete_language(self, edu_id):
        lang_record = request.env['custom.language.prof'].browse(edu_id)
        lang_record.unlink()
        return request.redirect('/pds/data')

    @http.route("/delete_work/<int:edu_id>", methods=['POST', 'GET'], type='http', auth='user', website=True,
                csrf=False)
    def delete_work(self, edu_id):
        work_record = request.env['custom.work.experience'].browse(edu_id)
        work_record.unlink()
        return request.redirect('/pds/data')

    @http.route("/create_cert", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def create_cert(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        certifications = request.env['custom.certif'].search([])
        if request.httprequest.method == 'POST':
            try:
                certifications.create({
                    'applicant_id': applicant_to_update[-1].id,
                    'pds_cert_name': kwargs.get("pds_cert_name"),
                    'pds_cert_provider': kwargs.get("pds_cert_provider"),
                    'pds_cert_issued_year': kwargs.get("pds_cert_issued_year"),
                })
                applicant_to_update.open_modal = True
            except Exception as e:
                print(f'Error Certification {e}')

        return request.redirect('/pds/data')

    @http.route("/create_edu", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def create_edu(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        education = request.env['custom.edu'].search([])
        if request.httprequest.method == 'POST':
            try:
                education.create({
                    'applicant_id': applicant_to_update[-1].id,
                    'pds_edu_inst_name': kwargs.get("pds_edu_inst_name"),
                    'pds_edu_major': kwargs.get("pds_edu_major"),
                    'pds_edu_location': kwargs.get("pds_edu_location"),
                    'pds_edu_start_year': kwargs.get("pds_edu_start_year"),
                    'pds_edu_end_year': kwargs.get("pds_edu_end_year"),
                })
            except Exception as e:
                print(f'Error Education {e}')
        return request.redirect('/pds/data')

    @http.route("/create_nonformedu", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def create_nonformedu(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        non_formeducation = request.env['custom.nonformaledu'].search([])
        if request.httprequest.method == 'POST':
            try:
                non_formeducation.create({
                    'applicant_id': applicant_to_update[-1].id,
                    'pds_course_name': kwargs.get("pds_course_name"),
                    'pds_course_provider': kwargs.get("pds_course_provider"),
                    'pds_course_issued_year': kwargs.get("pds_course_issued_year"),
                })
            except Exception as e:
                print(f'Error Non Formal Education {e}')
        return request.redirect('/pds/data')

    @http.route("/create_langprof", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def create_langprof(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        lang_prof = request.env['custom.language.prof'].search([])
        if request.httprequest.method == 'POST':
            try:
                lang_prof.create({
                    'applicant_id': applicant_to_update[-1].id,
                    'pds_lang_name': kwargs.get("pds_lang_name"),
                    'pds_lang_percen': kwargs.get("pds_lang_percen"),
                })
            except Exception as e:
                print(f'Error Language Proficiency {e}')
        return request.redirect('/pds/data')

    @http.route("/create_workexp", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def create_workexp(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        work_exp = request.env['custom.work.experience'].search([])
        if request.httprequest.method == 'POST':
            try:
                work_exp.create({
                    'applicant_id': applicant_to_update[-1].id,
                    'pds_workex_company_name': kwargs.get("pds_workex_company_name"),
                    'pds_workex_lob': kwargs.get("pds_workex_lob"),
                    'pds_workex_period_from': kwargs.get("pds_workex_period_from"),
                    'pds_workex_period_to': kwargs.get("pds_workex_period_to"),
                })

                # new_work_exp = {
                #     'applicant_id': applicant_to_update.id,
                #     'pds_workex_company_name': kwargs.get("pds_workex_company_name"),
                #     'pds_workex_lob': kwargs.get("pds_workex_lob"),
                #     'pds_workex_period_from': kwargs.get("pds_workex_period_from"),
                #     'pds_workex_period_to': kwargs.get("pds_workex_period_to"),
                # }
                #
                # # Assuming 'work_experience_ids' is the one2many field linking hr.applicant and custom.work.experience
                #
                # for applicant in applicant_to_update:
                #     applicant.write({'pds_work_exp': [(0, 0, new_work_exp)]})
            except Exception as e:
                print(f'Error Language Proficiency {e}')
        return request.redirect('/pds/data')

    @http.route("/pds/data", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def pds_route(self, **kwargs):

        user = request.env.user
        pds_data = request.env['hr.applicant'].search([("email_from", '=', user.email)])

        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        if request.httprequest.method == 'POST':
            for applicant in applicant_to_update:
                applicant.write({
                    "pds_fullname": kwargs.get("pds_fullname"),
                    "pds_nik": kwargs.get("pds_nik"),
                    "pds_addressNIK": kwargs.get("pds_addressNIK"),
                    "pds_zipcode_addressNIK": kwargs.get("pds_zipcode_addressNIK"),
                    "pds_currentAddress": kwargs.get("pds_currentAddress"),
                    "pds_zipcode_currentAddress": kwargs.get("pds_zipcode_currentAddress"),
                    "pds_phoneNumber": kwargs.get("pds_phoneNumber"),
                    "pds_email": kwargs.get("pds_email"),
                    "pds_placeOfBirth": kwargs.get("pds_placeOfBirth"),
                    "pds_nationality": kwargs.get("pds_nationality"),
                    "pds_religion": kwargs.get("pds_religion"),
                    "pds_dob": kwargs.get("pds_dob"),
                    "pds_marital_status": kwargs.get("pds_marital_status"),
                    "pds_sex": kwargs.get("pds_sex"),
                })

        data = {
            'pds_data': pds_data[-1],
            "page_name": "pds_data",
            "open_modal": pds_data[-1].open_modal
        }

        return request.render("ikon_talent_management.custom_pds_view", data)



    @http.route("/my/profile", type='http', auth='user', website=True)
    def my_profile(self):
        user = request.env.user
        applicants = request.env['hr.applicant'].search([('email_from', '=', user.email)])

        stage_checks = request.env['hr.applicant'].search([('email_from', '=', user.email)])

        for stage_check in stage_checks:
            if stage_check.stage_id.name == "PDS Submission":
                stage_check.write({'toggle_pds': 1})

        user_stage = 0
        applied_jobs = []
        for applicant in applicants:
            applied_jobs.append({
                'job': applicant.job_id,
                'stage': applicant.stage_id.name if applicant.stage_id else 'N/A',
                "created": applicant.create_date
            })
            if user_stage is 0 and applicant.toggle_pds is not 0:
                user_stage = applicant.toggle_pds

        # Other profile data retrieval
        uid = request.session.uid
        employment_status = request.env['hr.employee'].search([('user_id', '=', uid)], limit=1)

        # Pass the data to the template
        data = {
            "user_data": user,
            'employee_department': employment_status.department_id.name,
            'employment_status': employment_status,
            'applied_jobs': applied_jobs,
            "user_stage": user_stage,
        }

        return request.render("ikon_recruitment.custom_profile_view", data)
