{
    'name': 'IKON Recruitment Module',
    'summary': """IKON Rec Module""",
    'version': '16.0',
    "author": "Ikon Developer",
    'company': 'Ikonsultan Inovatama',
    'website': 'https://www.ikonsultan.com',
    'category': 'Tools',
    'images': [],
    'depends': ['base', 'web', 'website', 'portal', 'website_hr_recruitment', 'hr_recruitment', 'auth_signup'],
    "external_dependencies": {"python3.9": ["graphene"]},
    'license': 'AGPL-3',
    'data': [
        'data/hide_website_menu.xml',
        'security/ir.model.access.csv',
        'views/inherit/jobs_portal.xml',
        'views/inherit/footer_login.xml',
        'views/inherit/custom_job_detail.xml',
        'views/inherit/custom_hr_cruser_snemail.xml',
        'views/inherit/custom_quick_create_appl.xml',
        'views/inherit/custom_height_CV.xml',
        'views/custom_skill_form_view.xml',
        'views/custom_job_detail.xml',
        'views/my_profile_view.xml',
        'views/notification_message.xml',
        'views/inherit/job_apply_form.xml',
        'views/inherit/hr_recruitment.xml',
        'views/tes_popup.xml',
        'static/src/js/user_profile.js',
        'views/custom_hr_applicant_kanban.xml',
        'views/custom_job_position.xml',
        # Timesheet
        'views/timesheet/timesheet.xml',
        # 'views/timesheet/timesheet_dashboard.xml',
        # Screening Form
        # 'views/custom_screening_form_view.xml',
        # 'views/website_screening_form',
        # Custom email
        'data/custom_new_user_mail.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            '/ikon_recruitment/static/src/scss/my_profile.css',
            '/ikon_recruitment/static/src/js/notification_message.js',
            '/ikon_recruitment/static/src/css/popup.css',
        ],
        "web.assets_backend": [
        #     # "ikon_recruitment/static/src/components/custom_timesheet.js",
        #     # "ikon_recruitment/static/src/services/timesheet_service.js",
            "ikon_recruitment/static/src/components/**/*.xml",
            "ikon_recruitment/static/src/components/**/*.scss",
        ],

    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
