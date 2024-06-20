
################################################################################
{
    'name': 'IKON Timesheet',
    'version': '16.0.1.0.0',
    'category': 'Services',
    'summary': 'Timesheet Calendar View.',
    'description': 'Timesheet Calendar View.',
    'author': 'IKON',
    'company': 'PT Ikonsultan Inovatama',
    'maintainer': 'IKON',
    'website': "https://www.ikonsultan.com",
    'license': '',
    'depends': ['base', 'hr_timesheet'],
    'data': [
        'views/hr_timesheet_calendar_view.xml',
        'views/hr_timesheet_report_calender_view.xml',
        'views/inherit_timesheet.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
