# -*- coding: utf-8 -*-
{
    'name': "Kanban Stage Change Confirmation",

    'summary': """
        Add confirmation when change kanban stage""",

    'description': """
        Show popup when kanban record change stage (drag & drop) to avoid mistake.
    """,

    'author': 'Afifi A.M.',
    'maintainer': 'Afifi A.M.',
    'category': 'Tools',
    'license': 'LGPL-3',
    'version': '14.0.1.0',

    'depends': ['base'],
    'data': [
        # 'views/assets.xml',
    ],
    "assets": {
        # "web.assets_frontend": [
        #     # "ikon_talent_management/static/src/js/pds.js",
        # ],
        "web.assets_backend": [
            "pip_kanban_stage_confirmation/static/src/js/kanban_view.js",
        ],
    },
    'images': ['static/description/thumbnail.gif'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
