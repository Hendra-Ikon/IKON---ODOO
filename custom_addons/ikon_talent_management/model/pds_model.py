from datetime import datetime

from odoo import fields, models, api
from odoo.http import request
from odoo.exceptions import AccessError, UserError
from odoo.tools.translate import _

YEARS = datetime.now().year
start_year = 1945

YEAR_SELECTION = [(str(y), str(y)) for y in range(YEARS, start_year - 1, -1)]



RELIGION = [
    ('select', 'CLICK TO SELECT'),
    ("islam", "ISLAM"),
    ("kristen", "KRISTEN"),
    ("hindu", "HINDU"),
    ("budha", "BUDHA"),
    ("konghuchu", "KONGHUCHU"),

]

MARITAL_STATUS = [
    ('select', 'CLICK TO SELECT'),
    ('single', 'Single'),
    ('married', 'Married'),
    ('divorced', 'Divorced'),
]

ABILITY_AREA = [
    ('select', 'Click to select'),
    ("reading", "READING"),
    ('writing', 'WRITING'),
    ('speaking', 'SPEAKING'),
    ('listening', 'LISTENING'),
]

SEX = [
    ('select', 'CLICK TO SELECT'),
    ('male', 'MALE'),
    ('female', 'FAMALE'),
]

LEVELDEGREE = [
    ('select', 'Click to select'),
    ('high_school', 'High School'),
    ('bachelor', 'Bachelor Degree'),
    ('master', 'Master Degree'),
    ('doctor', 'Doctoral Degree'),
]

LANGUAGE_LEVEL = [
    ('select', 'Click to select'),
    ('poor', 'POOR'),
    ('fair', 'FAIR'),
    ('fluent', 'FLUENT'),
]


class PDSData(models.Model):
    _inherit = "hr.applicant"

    _description = "Personal Data Sheet"

    partner_id = fields.Many2one('res.partner', "Contact", copy=False)

    # Personal Records
    pds_fullname = fields.Char(string="Nama")
    pds_nik = fields.Char(string="NIK")
    pds_addressNIK = fields.Char(string="Alamat NIK")
    pds_zipcode_addressNIK = fields.Char(string="Zip")
    pds_currentAddress = fields.Char(string="Alamat sekarang")
    pds_zipcode_currentAddress = fields.Char(string="Zip")
    pds_phoneNumber = fields.Char(string="No Hp")
    pds_email = fields.Char(string="Personal Email")
    pds_placeOfBirth = fields.Char(string="Place of birth")
    pds_nationality = fields.Char(string="Nationality")
    pds_religion = fields.Selection(RELIGION)
    pds_dob = fields.Date(string="Date of Birth")
    pds_marital_status = fields.Selection(MARITAL_STATUS, string="Marital Status", )
    pds_sex = fields.Selection(SEX, string="Sex", )
    height_value = fields.Integer(string="Height Value")

    pds_fi_bank = fields.Char(string="Bank Name")
    pds_fi_bank_no = fields.Char(string="Bank Account")
    pds_fi_holder_name =  fields.Char(string="Account Holder Name" )
    pds_fi_npwp_number = fields.Char(string="Tax No (NPWP)")
    pds_fi_npwp_name = fields.Char(string="NPWP Name")
    pds_fi_npwp_address = fields.Char(string="NPWP Address")
    pds_fi_ptkp = fields.Char(string="PTKP")

    pds_ijazah_name = fields.Char(string="Ijazah")
    pds_transcript_nilai_name = fields.Char(string="Transcript Nilai")
    pds_bpjs_name = fields.Char(string="BPJS")
    pds_npwp_name = fields.Char(string="NPWP")
    pds_sertification_name = fields.Char(string="Sertification")

    # pds_education = fields.One2many('custom.edu', 'applicant_id', string='Education', domain="[('user_id', '=', user_id)]")
    pds_education = fields.One2many('custom.edu', 'applicant_id', string='Education')
    pds_certifications = fields.One2many('custom.certif', 'applicant_id', string='Certifications')
    pds_course = fields.One2many('custom.nonformaledu', 'applicant_id', string='Non Formal Edu')
    pds_lang_prof = fields.One2many('custom.language.prof', 'applicant_id', string='Language Proficiency')
    pds_work_exp = fields.One2many('custom.work.experience', 'applicant_id', string='Working Experience')
    pds_exp_sal = fields.One2many('custom.expected.salary', 'applicant_id', string='Expected Salary')
    pds_org = fields.One2many('custom.org', 'applicant_id', string='Organization Activities')
    pds_health = fields.One2many('custom.health', 'applicant_id', string='Health activities')
    pds_resume = fields.One2many('custom.resume.experience', 'applicant_id', string='Resume')
    pds_family = fields.One2many('custom.family.information', 'applicant_id', string='Family Information')
    pds_emCont = fields.One2many('custom.emergency.contact', 'applicant_id', string='Emergency Contact')
    pds_oac = fields.One2many('custom.other.activity', 'applicant_id', string='Other Activity')

    email_from = fields.Char("Email", size=128, compute='_compute_partner_phone_email',
        inverse='_inverse_partner_email', store=True)
   
    summary_experience = fields.Text(string="Summary of Experience")
    toggle_pds = fields.Integer(string="Switch PDS Element", default=0)
    open_modal = fields.Boolean(string="Modal Popup", default=True)

    pds_created_at = fields.Datetime(string='Created At', readonly=True)
    rsm_com_job_title = fields.Char(related="pds_resume.rsm_com_job_title", string="Job Title in Company")

    group_ids = fields.Many2one('res.groups', string='Group')


    @api.onchange('email_from')
    def _onchange_pds_fullname(self):
        if self.email_from:
            existing_record = self.search([('email_from', '=', self.email_from)], limit=1)
            if existing_record:
                self.pds_fullname = existing_record.pds_fullname
                self.pds_nik = existing_record.pds_nik
                self.pds_addressNIK = existing_record.pds_addressNIK
                self.pds_zipcode_addressNIK = existing_record.pds_zipcode_addressNIK
                self.pds_currentAddress = existing_record.pds_currentAddress
                self.pds_phoneNumber = existing_record.pds_phoneNumber
                self.pds_zipcode_currentAddress = existing_record.pds_zipcode_currentAddress
                self.pds_email = existing_record.pds_email
                self.pds_placeOfBirth = existing_record.pds_placeOfBirth
                self.pds_nationality = existing_record.pds_nationality
                self.pds_religion = existing_record.pds_religion
                self.pds_dob = existing_record.pds_dob
                self.pds_marital_status = existing_record.pds_marital_status
                self.pds_sex = existing_record.pds_sex
                self.height_value = existing_record.height_value
                self.pds_fi_bank = existing_record.pds_fi_bank
                self.pds_fi_bank_no = existing_record.pds_fi_bank_no
                self.pds_fi_holder_name = existing_record.pds_fi_holder_name
                self.pds_fi_npwp_number = existing_record.pds_fi_npwp_number
                self.pds_fi_npwp_name = existing_record.pds_fi_npwp_name
                self.pds_fi_npwp_address = existing_record.pds_fi_npwp_address
                self.pds_fi_ptkp = existing_record.pds_fi_ptkp
                self.pds_ijazah_name = existing_record.pds_ijazah_name
                self.pds_transcript_nilai_name = existing_record.pds_transcript_nilai_name
                self.pds_bpjs_name = existing_record.pds_bpjs_name
                self.pds_npwp_name = existing_record.pds_npwp_name
                self.pds_sertification_name = existing_record.pds_sertification_name
                self.pds_education = existing_record.pds_education
                self.pds_certifications = existing_record.pds_certifications
                self.pds_course = existing_record.pds_course
                self.pds_lang_prof = existing_record.pds_lang_prof
                self.pds_work_exp = existing_record.pds_work_exp
                self.pds_exp_sal = existing_record.pds_exp_sal
                self.pds_org = existing_record.pds_org
                self.pds_health = existing_record.pds_health
                self.pds_family = existing_record.pds_family
                self.pds_emCont = existing_record.pds_emCont
                self.pds_oac = existing_record.pds_oac
            else:
                self.pds_fullname = False
                self.pds_nik = False
                self.pds_addressNIK = False
                self.pds_zipcode_addressNIK = False
                self.pds_currentAddress = False
                self.pds_zipcode_currentAddress = False
                self.pds_phoneNumber = False
                self.pds_email = False
                self.pds_placeOfBirth = False
                self.pds_nationality = False
                self.pds_religion = False
                self.pds_dob = False
                self.pds_marital_status = False
                self.pds_sex = False
                self.height_value = False
                self.pds_fi_bank = False
                self.pds_fi_bank_no = False
                self.pds_fi_holder_name = False
                self.pds_fi_npwp_number = False
                self.pds_fi_npwp_name = False
                self.pds_fi_npwp_address = False
                self.pds_fi_ptkp = False
                self.pds_ijazah_name = False
                self.pds_transcript_nilai_name = False
                self.pds_bpjs_name = False
                self.pds_npwp_name = False
                self.pds_sertification_name = False
                self.pds_education = False
                self.pds_certifications = False
                self.pds_course = False
                self.pds_lang_prof = False
                self.pds_work_exp = False
                self.pds_exp_sal = False
                self.pds_org = False
                self.pds_health = False
                self.pds_family = False
                self.pds_emCont = False
                self.pds_oac = False
                # self.pds_education = [(5, 0, 0)]
                # self.pds_certifications = [(5, 0, 0)]
                # self.pds_course = [(5, 0, 0)]
                # self.pds_lang_prof = [(5, 0, 0)]
                # self.pds_work_exp = [(5, 0, 0)]
                # self.pds_exp_sal = [(5, 0, 0)]
                # self.pds_org = [(5, 0, 0)]
                # self.pds_health = [(5, 0, 0)]
                # self.pds_resume = [(5, 0, 0)]
                # self.pds_family = [(5, 0, 0)]
                # self.pds_emCont = [(5, 0, 0)]
                # self.pds_oac = [(5, 0, 0)]
                
                

    @api.model
    def create_pds(self, values):
        if 'pds_nik' in values and not self.pds_created_at:
            values['pds_created_at'] = datetime.now()
            print(f'Tanggal Pengisian {values}')
        return super(PDSData, self).write(values)

    # def write(self, values):
    #     if 'name' in values and not self.updated_at:
    #         values['updated_at'] = datetime.now()
    #     return super(YourModel, self).write(values)


    def create_employee_from_applicant(self):
        """ Create an employee from applicant """
        self.ensure_one()
        self._check_interviewer_access()

        contact = request.env["res.partner"].search([("email", "=", self.email_from)])
        user = request.env["res.users"].search([("login", "=", self.email_from)])

        user.active = False
        contact.active = False



            # Prepare employee data
        employee_data = {
            'default_name': self.partner_name or False,
            'default_job_id': self.job_id.id,
            'default_job_title': self.job_id.name,
            'default_department_id': self.department_id.id,
            'default_address_id': self.company_id.partner_id.id,
            'default_work_email': self.email_from,
            'default_work_phone': self.partner_phone or self.partner_mobile,
            'form_view_initial_mode': 'edit',
            'default_applicant_id': self.ids,
            'default_summary_experience': self.summary_experience,
            'default_employee_resumes': [(0, 0, {
                'employee_id': self.emp_id.id,
                'resume_dateStart': experience.resume_dateStart,
                'resume_dateEnd': experience.resume_dateEnd,
                'rsm_com_name': experience.rsm_com_name,
                'rsm_com_job_title': experience.rsm_com_job_title,
                'rsm_com_projectDes': experience.rsm_com_projectDes,
                'resume_tech_used': experience.resume_tech_used,
                'resume_sys_used': experience.resume_sys_used,
                'resume_tech_used_certificate': [(6, 0, experience.resume_tech_used_certificate.ids)],
                'company_image': experience.company_image,
            }) for experience in self.pds_resume],
        }



        # Create window action
        dict_act_window = self.env['ir.actions.act_window']._for_xml_id('hr.open_view_employee_list')
        dict_act_window['context'] = employee_data

        return dict_act_window

class HrApplEdu(models.Model):
    _name = 'custom.edu'

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    user_id = fields.Integer( string='User')
    employee_id = fields.Many2one('hr.employee', string='Applicant')
    pds_edu_inst_name = fields.Char(string="Institution name")
    pds_edu_level = fields.Selection(LEVELDEGREE, string="Level", default='select')
    pds_edu_major = fields.Char(string="Major")
    pds_edu_location = fields.Char(string="Location")
    pds_edu_start_year = fields.Selection(YEAR_SELECTION, string="Start year")
    pds_edu_end_year = fields.Selection(YEAR_SELECTION,string="End year")


class HrApplCertif(models.Model):
    _name = 'custom.certif'

    # Certification
    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    employee_id = fields.Many2one('hr.employee', string='Applicant')
    pds_cert_name = fields.Char(string="Certification name", required=False)
    pds_cert_provider = fields.Char(string="Provider", required=False)
    pds_cert_issued_year = fields.Selection(YEAR_SELECTION, string='Issued year', required=False)


class HrApplNonFormalEdu(models.Model):
    _name = "custom.nonformaledu"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    employee_id = fields.Many2one('hr.employee', string='Applicant')
    pds_course_name = fields.Char(string="Course name")
    pds_course_provider = fields.Char(string="Provider")
    pds_course_issued_year = fields.Selection(YEAR_SELECTION, string='Issued year')


class HrApplLanguageProf(models.Model):
    _name = "custom.language.prof"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    employee_id = fields.Many2one('hr.employee', string='Applicant')
    pds_lang_name = fields.Char(string="Language name")
    pds_ability = fields.Selection(ABILITY_AREA, string="Ability area")
    pds_lang_percen = fields.Selection(LANGUAGE_LEVEL, string="Level", default='1')


class HrApplWorkExperience(models.Model):
    _name = "custom.work.experience"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    employee_id = fields.Many2one('hr.employee', string='Applicant')
    pds_workex_company_name = fields.Char(string="Company name", help='Company name')
    pds_workex_lob = fields.Char(string="Line of bussiness", help="Line of bussiness")
    pds_workex_last_pos = fields.Char(string="Last Position", help="Last Position")
    pds_workex_reason_leave = fields.Char(string="Reason for leaving", help="Reason for leaving")
    pds_workex_last_salary = fields.Char(string="Last salary", help="Last salary")
    pds_workex_period_from = fields.Date(string="Working period From", help='Working period from')
    pds_workex_period_to = fields.Date(string="Working period To", help="Working period to")


class HrApplExpectedSalary(models.Model):
    _name = "custom.expected.salary"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    employee_id = fields.Many2one('hr.employee', string='Applicant')
    pds_expected_salary = fields.Char(string="Expected Salary", help="Expected Salary", default="0")
    pds_expected_benefit = fields.Char(string="Expected Benefit", help="Expected Benefit",
                                       default="Your expected benefit")


class HrApplOrg(models.Model):
    _name = "custom.org"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_org_name = fields.Char(string="Organization name")
    pds_org_nature = fields.Char(string="Organization Nature Activities")
    pds_org_position = fields.Char(string="Organization Position")
    pds_org_year = fields.Selection(YEAR_SELECTION, string="Year")


class HrApplHealth(models.Model):
    _name = "custom.health"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_health_radio = fields.Boolean(string="Health history", default=False)
    pds_health_period = fields.Char(string="Period")
    pds_health_type = fields.Char(string="Type")
    pds_health_hospital = fields.Char(string="Hospital name")
    pds_health_year = fields.Selection(YEAR_SELECTION,string="Year")


class HrApplFamily(models.Model):
    _name = "custom.family.information"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_family_desc = fields.Char(string="Family Description")
    pds_family_name = fields.Char(string="Name")
    pds_family_sex =  fields.Selection(SEX, string="Sex" )
    pds_family_age = fields.Char(string="Age")
    pds_family_education = fields.Char(string="Education")
    pds_family_company_position= fields.Char(string="Occupation (Company & Position)")
    pds_family_type= fields.Char(string="type")

class HrApplEmerContact(models.Model):
    _name = "custom.emergency.contact"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_emercon_name = fields.Char(string="Name")
    pds_emercon_address = fields.Char(string="Address")
    pds_emercon_phone =  fields.Char(string="Phone" )
    pds_emercon_relationship = fields.Char(string="Relationship")

class HrApplOtherAct(models.Model):
    _name = "custom.other.activity"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_oc_name = fields.Char(string="Hobby Name")
    pds_rate = fields.Char(string="Rate")


 