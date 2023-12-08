{
    'name': 'IKON Talent Management',
    'summary': """IKON Talent Management""",
    'version': '16.0',
    "author": "Ikon Developer",
    'company': 'Ikonsultan Inovatama',
    'website': 'https://www.ikonsultan.com',
    'category': 'Tools',
    'images'  : [],
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
        'views/pds_view.xml',
        'static/src/js/pds_popup_template.xml',
        # 'views/view_report/report_talent.xml',
    ],

    "assets": {
        "web.assets_frontend": [
            # "ikon_talent_management/static/src/js/pds.js",
        ],
        "web.assets_backend": [
            "ikon_talent_management/static/src/js/pds.js",
        ],
    },
    # 'js': [
    #     'static/src/js/simple_alert.js',
    # ],

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': True,
}
