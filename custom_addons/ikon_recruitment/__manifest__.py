{
    'name': 'IKON Recruitment Module',
    'summary': """IKON Rec Module""",
    'version': '16.0',
    "author": "Ikon Developer",
    'company': 'Ikonsultan Inovatama',
    'website': 'https://www.ikonsultan.com',
    'category': 'Tools',
    'images': [],
    'depends': ['base', 'web', 'website', 'portal', 'website_hr_recruitment', ],
    "external_dependencies": {"python3.9": ["graphene"]},
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/inherit/jobs_portal.xml',
        'views/inherit/footer_login.xml',
        'views/inherit/custom_job_detail.xml',
        'views/inherit/custom_hr_cruser_snemail.xml',
        'views/inherit/custom_quick_create_appl.xml',
        'views/custom_skill_form_view.xml',
        'views/custom_job_detail.xml',
        'views/my_profile_view.xml',
        'views/tes_popup.xml',
        'static/src/js/user_profile.js',

        'views/custom_hr_applicant_kanban.xml',
        'views/custom_job_position.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/ikon_recruitment/static/src/scss/my_profile.css',
        ],
        # 'ikon_recruitment.assets': [
        #     ''
        # ]
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
