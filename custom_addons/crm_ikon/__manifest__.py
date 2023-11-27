{
    'name': 'CRM IKON',
    'summary': """CRM Ikon Module""",
    'version': '16.0',
    "author": "Ikon Developer",
    'company': 'Ikonsultan Inovatama',
    'website': 'https://www.ikonsultan.com',
    'category': 'Tools',
    'depends': ['base', 'crm', 'sale', 'sale_management', 'multicolor_backend_theme', 'base_setup', 'mail', 'web'],
    "external_dependencies": {"python3.9": ["graphene"]},
    'license': 'AGPL-3',
    'data': [
        # security
        'security/crm_ikon_groups.xml',
        
        # data
        'data/load_medium.xml',
        'data/load_source.xml',
        'data/load_service_category.xml',
        'data/load_service.xml',
        'data/load_term_payment.xml',
        # 'data/load_crm_stage.xml',
        'data/load_crm_categories.xml',
        
        # views
        'views/term_payment_views.xml',
        'views/term_payment_plan_views.xml',
        
        # views inherit
        'views/inherit_crm_lead_views.xml',
        'views/inherit_sale_order_views.xml',
        'views/inherit_sale_product_views.xml',
        'views/inherit_product_form_views.xml',
        'views/inherit_invoice_line_views.xml',
        'views/inherit_invoice_views.xml',
        'views/inherit_sales_team_views.xml',
        'views/inherit_partner_views.xml',
        'views/inherit_stage_views.xml',
        'views/inherit_contact_views.xml',
        'views/inherit_categories_views.xml',
        'views/view_crm_lead_form_inherit.xml',

        # report
        'report/sale_report_inherit.xml',
        'report/invoice_report_inherit.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'post_init_hook': '_post_init_hook',
    'uninstall_hook': '_uninstall_hook',
    'assets': {
        'web.assets_backend': [
            'crm_ikon/static/js/contact_kanban_import_button.js',
            'crm_ikon/static/js/contact_list_import_button.js',
            'crm_ikon/static/xml/contact_kanban_import_button.xml',
            'crm_ikon/static/xml/contact_list_import_button.xml',
        ],
    },
}
