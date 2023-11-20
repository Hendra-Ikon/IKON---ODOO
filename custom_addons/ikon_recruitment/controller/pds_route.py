import os
from odoo import http
from odoo.http import request
import json


class PDSController(http.Controller):


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

    @http.route("/pds/data", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def pds_route(self, **kwargs):

        user = request.env.user
        pds_data = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        # certifications = pds_data.mapped('pds_certifications')
        certifications = request.env['custom.certif'].search([])
        education = request.env['custom.edu'].search([])

        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        if request.httprequest.method == 'POST':

            education.create({
                'applicant_id': applicant_to_update.id,
                'pds_edu_inst_name': kwargs.get("pds_edu_inst_name"),
                'pds_edu_major': kwargs.get("pds_edu_major"),
                'pds_edu_location': kwargs.get("pds_edu_location"),
                'pds_edu_start_year': kwargs.get("pds_edu_start_year"),
                'pds_edu_end_year': kwargs.get("pds_edu_end_year"),
            })

            certifications.create({
                'applicant_id': applicant_to_update.id,
                'pds_cert_name': kwargs.get("pds_cert_name"),
                'pds_cert_provider': kwargs.get("pds_cert_provider"),
                'pds_cert_issued_year': kwargs.get("pds_cert_issued_year"),
            })

            applicant_to_update.write({
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
                "pds_edu_inst_name": kwargs.get("pds_edu_inst_name"),
                "pds_edu_major": kwargs.get("pds_edu_major"),
                "pds_edu_location": kwargs.get("pds_edu_location"),
                "pds_edu_start_year": kwargs.get("pds_edu_start_year"),
                "pds_edu_end_year": kwargs.get("pds_edu_end_year"),

            })

        data = {
            'pds_data': pds_data[0],
            "page_name": "pds_data"
        }

        return request.render("ikon_talent_management.custom_pds_view", data)



    @http.route("/my/profile", type='http', auth='user', website=True)
    def my_profile(self):
        # user_data = request.env['res.partner'].search([])
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
