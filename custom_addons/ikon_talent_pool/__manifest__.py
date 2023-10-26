{
    'name': 'IKON Talent Pool Module',
    'summary': """IKON Talent Pool Module""",
    'version': '16.0',
    "author": "Ikon Developer",
    'company': 'Ikonsultan Inovatama',
    'website': 'https://www.ikonsultan.com',
    'category': 'Tools',
    'images'  : [],
    'depends': ['base'],
    "external_dependencies": {"python3.9": ["graphene"]},
    'license': 'AGPL-3',
    'data': [
        'views/talent_pool_import_data_views.xml',
        'views/talent_kanban_views.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}