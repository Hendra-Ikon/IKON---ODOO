import os
from odoo import http
from odoo.http import request


class PDSController(http.Controller):

    @http.route("/pds/data", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def pds_route(self, **kwargs):
        user_id = request.env.user.id  # Use Odoo's user ID if available

        applicant_to_update = request.env['hr.applicant'].search([("user_id", '=', user_id)])
        if request.httprequest.method == 'POST':
            applicant_to_update.write({
                # 'name': applicant_name.name,
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
                # "interviewer_ids": [(6, 0, user_id)]
            })

            # return request.redirect('/job-thank-you')
        pds_data = request.env['hr.applicant'].search([], limit=1)

        data = {
            'pds_data': pds_data,
        }

        return request.render("ikon_talent_management.custom_pds_view", data)

    @http.route("/my/profile", type='http', auth='user', website=True)
    def my_profile(self):
        # user_data = request.env['res.partner'].search([])
        user = request.env.user
        applicants = request.env['hr.applicant'].search([('email_from', '=', user.email)])

        # Fetch the applied jobs from the computed field
        applied_jobs = []
        for applicant in applicants:
            applied_jobs.append({
                'job': applicant.job_id,
                'stage': applicant.stage_id.name if applicant.stage_id else 'N/A'
            })

        # Other profile data retrieval
        uid = request.session.uid
        employment_status = request.env['hr.employee'].search([('user_id', '=', uid)], limit=1)

        # Pass the data to the template
        data = {
            "user_data": user,
            'employee_department': employment_status.department_id.name,
            'employment_status': employment_status,
            'applied_jobs': applied_jobs,
        }

        return request.render("ikon_recruitment.custom_profile_view", data)
