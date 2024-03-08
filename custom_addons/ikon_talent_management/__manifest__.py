{
    'name': 'IKON Talent Management',
    'summary': """IKON Talent Management""",
    'version': '16.0',
    "author": "Ikon Developer",
    'company': 'Ikonsultan Inovatama',
    'website': 'https://www.ikonsultan.com',
    'category': 'Tools',
    'images': [],
    'images': [],
    'depends': ['base', "web", 'hr_recruitment', 'hr_skills', 'website', ],
    "external_dependencies": {"python3.9": ["graphene"]},
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/talent_pool_import_data_views.xml',
        'views/talent_tree_view.xml',
        'views/talent_kanban_views.xml',
        'views/menu_talent.xml',
        'views/views.xml',
        'views/pds_talent.xml',
        'views/employee_resume.xml',
        'views/pds_view.xml',
        # 'views/resume_view.xml',
        'report/cv_report.xml',
        'report/cv_template_pds.xml',
        'report/cv_hitam_cand.xml',
        'report/cv_template_employee.xml',
        'report/pds_report.xml',
        'report/pds_report_template.xml',
        'report/pageformat_cv.xml',
        # 'views/CV_view.xml',
        # 'views/custom_resume_template.xml',
        'static/src/js/pds_popup_template.xml',
        # 'views/view_report/report_talent.xml',
    ],

    "assets": {
        "web.assets_frontend": [
            "ikon_talent_management/static/src/js/pds.js",
             "ikon_talent_management/static/src/js/tab.js",
        ],
         "web.assets_frontend_min": [
            "ikon_talent_management/static/src/css/popup.scss",
        ],
        "web.assets_backend": [
            # "ikon_talent_management/static/src/js/pds.js",
            "ikon_talent_management/static/src/js/custom_resume.js",
            "ikon_talent_management/static/src/scss/*",
            "ikon_talent_management/static/src/views/**/*.xml",
            'addons/hr_skills/static/src/fields/*',
            # "ikon_talent_management/static/src/js/custom_one2many_list.js",
            # 'hr_skills/static/src/fields/skills_one2many.xml',
            # 'hr_skills/static/src/fields/*',
            # 'hr_skills/static/src/scss/*.scss',
            # 'hr_skills/static/src/views/*.js',
            # 'hr_skills/static/src/xml/**/*',
        ],
        # "web.assets_common": [
        #     # "ikon_talent_management/static/src/js/pds.js",
        #
        # ],
        'ikon_talent_management.report_assets_common': [
            "ikon_talent_management/static/src/css/cv_pdf.css",
  
        ]
    },
    # 'js': [
    #     'static/src/js/simple_alert.js',
    # ],

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': True,
}