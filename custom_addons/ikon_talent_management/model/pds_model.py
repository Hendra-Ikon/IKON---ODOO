from odoo import fields, models, api
from odoo.http import request

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
    ('female', 'Married'),
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

    pds_education = fields.One2many('custom.edu', 'applicant_id', string='Education')
    pds_certifications = fields.One2many('custom.certif', 'applicant_id', string='Certifications')
    pds_course = fields.One2many('custom.nonformaledu', 'applicant_id', string='Non Formal Edu')
    pds_lang_prof = fields.One2many('custom.language.prof', 'applicant_id', string='Language Proficiency')
    pds_work_exp = fields.One2many('custom.work.experience', 'applicant_id', string='Working Experience')
    pds_exp_sal = fields.One2many('custom.expected.salary', 'applicant_id', string='Expected Salary')
    pds_org = fields.One2many('custom.org', 'applicant_id', string='Organization Activities')
    pds_health = fields.One2many('custom.health', 'applicant_id', string='Health activities')
    pds_resume = fields.One2many('custom.resume.experience', 'applicant_id', string='Resume')
    summary_experience = fields.Text(string="Summary of Experience")
    toggle_pds = fields.Integer(string="Switch PDS Element", default=0)
    open_modal = fields.Boolean(string="Modal Popup", default=True)

    # Resume
#     resume_dateStart = fields.Date(string="Resume Start")
#     resume_dateEnd = fields.Date(string="Resume End")
#     rsm_com_name = fields.Char(string="Company Name")
    rsm_com_job_title = fields.Char(related="pds_resume.rsm_com_job_title", string="Job Title in Company")
#     rsm_com_projectDes = fields.Char(string="Project Description")
#     resume_tech_used_backend = fields.Many2many('custom.technology.tag', "resume_techs_tag_rel",
#                                                 string='Backend Technology Used')
#     resume_tech_used_frontend = fields.Many2many('custom.technology.tag', "resume_techs_tag_rel",
#                                                  string='Frontend Technology Used')
#     resume_tech_used_database = fields.Many2many('custom.technology.tag', "resume_techs_tag_rel",
#                                                  string='Database Technology Used')
#
#
# class TechnologyTag(models.Model):
#     _name = 'custom.technology.tag'
#     _description = 'Technology Tags'
#
#     name = fields.Char(string='Tag Name', )

    # resume_company_id = fields.One2many("custom.resume.experience.company", "resume_experience_id", string="Company ID")


class HrApplEdu(models.Model):
    _name = 'custom.edu'

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_edu_inst_name = fields.Char(string="Institution name")
    pds_edu_level = fields.Selection(LEVELDEGREE, string="Level", default='select')
    pds_edu_major = fields.Char(string="Major")
    pds_edu_location = fields.Char(string="Location")
    pds_edu_start_year = fields.Date(string="Start year")
    pds_edu_end_year = fields.Date(string="End year")


class HrApplCertif(models.Model):
    _name = 'custom.certif'

    # Certification
    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_cert_name = fields.Char(string="Certification name", required=False)
    pds_cert_provider = fields.Char(string="Provider", required=False)
    pds_cert_issued_year = fields.Date(string='Issued year', required=False, default="01/01/2001")


class HrApplNonFormalEdu(models.Model):
    _name = "custom.nonformaledu"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_course_name = fields.Char(string="Course name")
    pds_course_provider = fields.Char(string="Provider")
    pds_course_issued_year = fields.Date(string='Issued year')


class HrApplLanguageProf(models.Model):
    _name = "custom.language.prof"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_lang_name = fields.Char(string="Language name")
    pds_ability = fields.Selection(ABILITY_AREA, string="Ability area")
    pds_lang_percen = fields.Selection(LANGUAGE_LEVEL, string="Level", default='1')


class HrApplWorkExperience(models.Model):
    _name = "custom.work.experience"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_workex_company_name = fields.Char(string="Company name", help='Company name')
    pds_workex_lob = fields.Char(string="Line of bussiness", help="Line of bussiness")
    pds_workex_last_pos = fields.Char(string="Last Position", help="Last Position")
    pds_workex_reason_leave = fields.Char(string="Reason for leaving", help="Reason for leaving")
    pds_workex_last_salary = fields.Char(string="Last salary", help="Last salary")
    pds_workex_period_from = fields.Date(string="Working period", help='Working period from')
    pds_workex_period_to = fields.Date(string="to", help="Working period to")


class HrApplExpectedSalary(models.Model):
    _name = "custom.expected.salary"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_expected_salary = fields.Char(string="Expected Salary", help="Expected Salary", default="0")
    pds_expected_benefit = fields.Char(string="Expected Benefit", help="Expected Benefit",
                                       default="Your expected benefit")


class HrApplOrg(models.Model):
    _name = "custom.org"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_org_name = fields.Char(string="Organization name")
    pds_org_nature = fields.Char(string="Organization Nature Activities")
    pds_org_position = fields.Char(string="Organization Position")
    pds_org_year = fields.Date(string="Year")


class HrApplHealth(models.Model):
    _name = "custom.health"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    pds_health_radio = fields.Boolean(string="Health history", default=False)
    pds_health_period = fields.Char(string="Period")
    pds_health_type = fields.Char(string="Type")
    pds_health_hospital = fields.Char(string="Hospital name")
    pds_health_year = fields.Date(string="Year")
