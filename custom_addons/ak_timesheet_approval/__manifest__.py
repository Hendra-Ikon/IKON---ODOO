# -*- coding: utf-8 -*-
{
    'name': "Timesheet Approval",

    'summary': """
        Manager can approve and reject the time sheet of an employee.""",

    'description': """
        With the help of this module you can manage manager can approve or reject the time sheet and it automatically send the mail to 
        the employee.
    """,

    'author': "Akili systems Pvt. Ltd.",
    'website': "http://www.akilisystems.in",
    'category': "tools",
    'version': "16.0.1",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    'depends': ['hr_timesheet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/timesheet_validation_groups.xml',
        'views/timesheet_validation.xml',
        'views/email_template.xml',
    ],

    
    'images': ['static/description/banner.jpg'],
    'autoinstall': False,
    'installable': True,
    'application': False
}
