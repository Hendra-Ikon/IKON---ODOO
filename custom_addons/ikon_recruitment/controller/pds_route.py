import os

from odoo import http, fields, models, _
from odoo.http import request
import json
import logging
from odoo.exceptions import ValidationError

logger = logging.getLogger(__name__)

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
        return request.redirect('/pds/data#education')

    @http.route("/delete_nonfromedu/<int:edu_id>", methods=['POST', 'GET'], type='http', auth='user', website=True,
                csrf=False)
    def delete_nonfromedu(self, edu_id):
        nonedu_record = request.env['custom.nonformaledu'].browse(edu_id)
        nonedu_record.unlink()
        return request.redirect('/pds/data#education')

    @http.route("/delete_language/<int:edu_id>", methods=['POST', 'GET'], type='http', auth='user', website=True,
                csrf=False)
    def delete_language(self, edu_id):
        lang_record = request.env['custom.language.prof'].browse(edu_id)
        lang_record.unlink()
        return request.redirect('/pds/data#language')

    @http.route("/delete_work/<int:edu_id>", methods=['POST', 'GET'], type='http', auth='user', website=True,
                csrf=False)
    def delete_work(self, edu_id):
        work_record = request.env['custom.work.experience'].browse(edu_id)
        work_record.unlink()
        return request.redirect('/pds/data')

    @http.route("/delete_exp/<int:edu_id>", methods=['POST', 'GET'], type='http', auth='user', website=True,
                csrf=False)
    def delete_exp(self, edu_id):
        work_record = request.env['custom.expected.salary'].browse(edu_id)
        work_record.unlink()
        return request.redirect('/pds/data#medical')

    @http.route("/delete_org/<int:org_id>", methods=['POST', 'GET'], type='http', auth='user', website=True,
                csrf=False)
    def delete_org(self, org_id):
        org_record = request.env['custom.org'].browse(org_id)
        org_record.unlink()
        return request.redirect('/pds/data#language')

    @http.route("/delete_health/<int:health_id>", methods=['POST', 'GET'], type='http', auth='user', website=True,
                csrf=False)
    def delete_health(self, health_id):
        health_record = request.env['custom.health'].browse(health_id)
        health_record.unlink()
        return request.redirect('/pds/data#medical')

    @http.route("/create_cert", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def create_cert(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        certifications = request.env['custom.certif'].search([])
        if request.httprequest.method == 'POST':
            try:
                for applicant in applicant_to_update:
                    pds_check = request.env['custom.certif'].search([('applicant_id','=',applicant.id)], limit=1)
                    if pds_check:
                        pass
                    else:
                        applicant_to_update.write({
                            'pds_fill': applicant.pds_fill + 1
                        })

                    certifications.create({
                        'applicant_id': applicant.id,
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
                for applicant in applicant_to_update:
                    pds_check = request.env['custom.edu'].search([('applicant_id','=',applicant.id)], limit=1)
                    if pds_check:
                        pass
                    else:
                        applicant_to_update.write({
                            'pds_fill': applicant.pds_fill + 1
                        })

                    education.create({
                        'applicant_id': applicant.id,
                        'pds_edu_inst_name': kwargs.get("pds_edu_inst_name"),
                        'pds_edu_level': kwargs.get("pds_edu_level"),
                        'pds_edu_major': kwargs.get("pds_edu_major"),
                        'pds_edu_location': kwargs.get("pds_edu_location"),
                        'pds_edu_start_year': kwargs.get("pds_edu_start_year"),
                        'pds_edu_end_year': kwargs.get("pds_edu_end_year"),
                    })
                    
            except Exception as e:
                print(f'Error Education {e}')
        return request.redirect('/pds/data#education')

    @http.route("/create_nonformedu", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def create_nonformedu(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        non_formeducation = request.env['custom.nonformaledu'].search([])
        if request.httprequest.method == 'POST':
            try:
                for applicant in applicant_to_update:
                    pds_check = request.env['custom.nonformaledu'].search([('applicant_id','=',applicant.id)], limit=1)
                    if pds_check:
                        pass
                    else:
                        applicant_to_update.write({
                            'pds_fill': applicant.pds_fill + 1
                        })
                    non_formeducation.create({
                        'applicant_id': applicant.id,
                        'pds_course_name': kwargs.get("pds_course_name"),
                        'pds_course_provider': kwargs.get("pds_course_provider"),
                        'pds_course_issued_year': kwargs.get("pds_course_issued_year"),
                      
                    })
                    
            except Exception as e:
                print(f'Error Non Formal Education {e}')
        return request.redirect('/pds/data#education')

    @http.route("/create_langprof", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def create_langprof(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        lang_prof = request.env['custom.language.prof'].search([])
        if request.httprequest.method == 'POST':
            try:
                for applicant in applicant_to_update:
                    pds_check = request.env['custom.language.prof'].search([('applicant_id','=',applicant.id)], limit=1)
                    if pds_check:
                        pass
                    else:
                        applicant_to_update.write({
                            'pds_fill': applicant.pds_fill + 1
                        })
                    
                    lang_prof.create({
                        'applicant_id': applicant.id,
                        'pds_lang_name': kwargs.get("pds_lang_name"),
                        'pds_ability': kwargs.get("pds_ability"),
                        'pds_lang_percen': kwargs.get("pds_lang_percen"),
                        
                    })
                    
            except Exception as e:
                print(f'Error Language Proficiency {e}')
        return request.redirect('/pds/data#language')

    @http.route("/create_workexp", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def create_workexp(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        work_exp = request.env['custom.work.experience'].search([])
        if request.httprequest.method == 'POST':
            try:
                for applicant in applicant_to_update:
                    work_exp.create({
                        'applicant_id': applicant.id,
                        'pds_workex_company_name': kwargs.get("pds_workex_company_name"),
                        'pds_workex_lob': kwargs.get("pds_workex_lob"),
                        'pds_workex_last_pos': kwargs.get("pds_workex_last_pos"),
                        'pds_workex_reason_leave': kwargs.get("pds_workex_reason_leave"),
                        'pds_workex_last_salary': kwargs.get("pds_workex_last_salary"),
                        'pds_workex_period_from': kwargs.get("pds_workex_period_from"),
                        'pds_workex_period_to': kwargs.get("pds_workex_period_to"),
                    })


            except Exception as e:
                print(f'Error Working Exp {e}')
        return request.redirect('/pds/data')

    @http.route("/create_expected_salary", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def create_expected_salary(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        exp_sal = request.env['custom.expected.salary'].search([])



        if request.httprequest.method == 'POST':
            try:
                for applicant in applicant_to_update:
                    pds_check = request.env['custom.expected.salary'].search([('applicant_id','=',applicant.id)], limit=1)
                    if pds_check:
                        pass
                    else:
                        applicant_to_update.write({
                            'pds_fill': applicant.pds_fill + 1
                        })
                    
                    exp_sal.create({
                        'applicant_id': applicant.id,
                        'pds_expected_salary': kwargs.get("pds_expected_salary"),
                        'pds_expected_benefit': kwargs.get("pds_expected_benefit"),
                    })
                    

            except Exception as e:
                print(f'Error Expected Salary {e}')
        return request.redirect('/pds/data#medical')

    @http.route("/create_org", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def create_org(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        work_exp = request.env['custom.org'].search([])
        if request.httprequest.method == 'POST':
            try:
                for applicant in applicant_to_update:
                    pds_check = request.env['custom.org'].search([('applicant_id','=',applicant.id)], limit=1)
                    if pds_check:
                        pass
                    else:
                        applicant_to_update.write({
                            'pds_fill': applicant.pds_fill + 1
                        })
                    work_exp.create({
                        'applicant_id': applicant.id,
                        'pds_org_name': kwargs.get("pds_org_name"),
                        'pds_org_nature': kwargs.get("pds_org_nature"),
                        'pds_org_position': kwargs.get("pds_org_position"),
                        'pds_org_year': kwargs.get("pds_org_year"),
                    })
                    


            except Exception as e:
                print(f'Error Organization {e}')
        return request.redirect('/pds/data#language')
        

    @http.route("/create_heealth_act", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def create_heealth_act(self, **kwargs):
        user = request.env.user
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        work_exp = request.env['custom.health'].search([])
        if request.httprequest.method == 'POST':
            try:
                for applicant in applicant_to_update:
                    pds_check = request.env['custom.health'].search([('applicant_id','=',applicant.id)], limit=1)
                    if pds_check:
                        pass
                    else:
                        applicant_to_update.write({
                            'pds_fill': applicant.pds_fill + 1
                        })
                    work_exp.create({
                        'applicant_id': applicant.id,
                        'pds_health_radio': kwargs.get("pds_health_radio"),
                        'pds_health_period': kwargs.get("pds_health_period"),
                        'pds_health_type': kwargs.get("pds_health_type"),
                        'pds_health_hospital': kwargs.get("pds_health_hospital"),
                        'pds_health_year': kwargs.get("pds_health_year"),
                    })
                    
                
                # message = "Health Section successfully added."
                #
                # # Use the website controller to execute JavaScript
                # return request.render("ikon_recruitment.display_notification_template", {'message': message})

            except Exception as e:
                print(f'Error Health Activities {e}')
        return request.redirect('/pds/data#medical')

    @http.route("/pds/data", methods=['POST', 'GET'], type='http', auth='user', website=True, csrf=False)
    def pds_route(self, **kwargs):

        user = request.env.user
        pds_data = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        applicant_to_update = request.env['hr.applicant'].search([("email_from", '=', user.email)])
        exp_sal = request.env['custom.expected.salary'].search([("applicant_id", "=", applicant_to_update.id)])

        if request.httprequest.method == 'POST':
            for applicant in applicant_to_update:
                if applicant_to_update:
                        pass
                else:
                        applicant_to_update.write({
                            'pds_fill': applicant.pds_fill + 1
                        })
                applicant.update({
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


        data = {}
        if pds_data:
            data = {
                'pds_data': pds_data[-1],  # Assuming you want the last element if it exists
                "page_name": "pds_data",
                "open_modal": pds_data[-1].open_modal,
                "exp_sal": exp_sal
            }

        return request.render("ikon_talent_management.custom_pds_view", data)

    @http.route("/my/profile", type='http', auth='user', website=True)
    def my_profile(self):
        user = request.env.user
        user_avatar = user.image_1920
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
                "created": applicant.create_date,
                'from_talent_universitas': applicant.from_talent_universitas,
                'partner_phone': applicant.partner_phone,
                'email_from': applicant.email_from,
                'pds_currentAddress': applicant.pds_currentAddress,
                'degree': applicant.type_id.name,
                'summary_experience': applicant.summary_experience,
                'skill': applicant.custom_skill,
                'fullname': applicant.pds_fullname,
                
            })
            if user_stage is 0 and applicant.toggle_pds is not 0:
                user_stage = applicant.toggle_pds

        # Other profile data retrieval
        uid = request.session.uid
        employment_status = request.env['hr.employee'].search([('user_id', '=', uid)], limit=1)
        # Pass the data to the template
        data = {
            "user_data": user,
            "user_avatar": user_avatar,
            'employee_department': employment_status.department_id.name,
            'employment_status': employment_status,
            'applied_jobs': applied_jobs,
            "user_stage": user_stage,
        }
        logger.info("data", data)

        return request.render("ikon_recruitment.custom_profile_view", data)

    @http.route("/my", type='http', auth='user', website=True)
    def custom_route_my(self):
        user = request.env.user
        user_avatar = user.image_1920
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
                "created": applicant.create_date,
                'from_talent_universitas': applicant.from_talent_universitas,
                'partner_phone': applicant.partner_phone,
                'email_from': applicant.email_from,
                'pds_currentAddress': applicant.pds_currentAddress,
                'degree': applicant.type_id.name,
                'summary_experience': applicant.summary_experience,
                'skill': applicant.custom_skill,
                'fullname': applicant.pds_fullname,
            })
            if user_stage is 0 and applicant.toggle_pds is not 0:
                user_stage = applicant.toggle_pds

        # Other profile data retrieval
        uid = request.session.uid
        employment_status = request.env['hr.employee'].search([('user_id', '=', uid)], limit=1)

        # Pass the data to the template
        data = {
            "user_data": user,
            "user_avatar": user_avatar,
            'employee_department': employment_status.department_id.name,
            'employment_status': employment_status,
            'applied_jobs': applied_jobs,
            "user_stage": user_stage,
        }

        return request.render("ikon_recruitment.custom_profile_view", data)
    
    # pds send mail
    @http.route('/confirm', type='http', auth='user', website=True)
    def send_mail_route(self):
        user = request.env.user
        applicants = request.env['hr.applicant'].sudo().search([('email_from', '=', user.email)])
        job = request.env['hr.job'].sudo().browse(applicants.job_id.id)
        recruiter = request.env['res.users'].sudo().browse(job.user_id.id)
        
        
        # 'PDS Confirm '+ str(applicants.pds_percentage) +'%'+' from '+ applicants.partner_name,
        try:
            link_to_pds_data = 'https://backofficedev.ikonsultan.co.id/my/profile'
            mail_template = request.env.ref('ikon_recruitment.set_pds_email_send').sudo() # Ganti dengan nama template email yang sesuai      
            mail_template.send_mail(
                recruiter.id,
                email_values = {
                'email_to': recruiter.login,
                'subject' : f"{applicants.partner_name} - {job.name} Has Filled Out the PDS Form.",
                'body_html': '''
        <p>Hello %s,</p>
        <p>Candidate with:</p>
        <ul>
            <li>Name : %s</li>
            <li>Position : %s</li>
        </ul>
        <p>Has Filled Out The PDS Form. You can check their PDS by looking at the pipeline or click link below:</p>
        <p><a href="%s" target="_blank">View Candidate PDS Data</a></p>
    ''' % (recruiter.name, applicants.partner_name, job.name, link_to_pds_data),
            },
            force_send=True)

        except ValidationError as e:
            return f"Error: {e}"
        
        return request.redirect('/pds/data#confirm')





class WebsiteNotifications(models.TransientModel):

    _name = 'website.notification'


    notification = fields.Char('Notification')
    user_id = fields.Many2one('res.users', string="Users")
    state = fields.Selection([('to_send', 'To Send'),
                              ('sent', 'Sent')],
                             string="Status", required=True,
                             default='to_send')

    def get_notifications(self, user_id):
        notifications = self.env['website.notification'].search(
            [('user_id', '=', user_id), ('state', '=', 'to_send')])

        names = notifications.mapped('notification')
        for rec in notifications:
            rec.state = 'sent'
        return names