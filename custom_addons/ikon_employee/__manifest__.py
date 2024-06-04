{
    'name': 'IKON Employee Module',
    'summary': """IKON Employee Module""",
    'version': '16.0',
    "author": "Ikon Developer",
    'company': 'Ikonsultan Inovatama',
    'website': 'https://www.ikonsultan.com',
    'category': 'Tools',
    'images': [],
    'depends': ['base', 'web', 'website', 'portal', 'website_hr_recruitment', 'hr_recruitment'],
    "external_dependencies": {"python3.9": ["graphene"]},
    'license': 'AGPL-3',
    'data': [
        # Timesheet
        'views/timesheet/timesheet.xml',
    ],
    'assets': {
        'web.assets_frontend': [
        ],
        "web.assets_backend": [
            "ikon_employee/static/src/components/custom_timesheet.js",
            "ikon_employee/static/src/services/timesheet_service.js",
            "ikon_employee/static/src/components/**/*.xml",
            "ikon_employee/static/src/components/**/*.scss",
        ],

    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
