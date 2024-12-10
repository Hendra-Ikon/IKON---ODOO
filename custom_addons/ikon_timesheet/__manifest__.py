# -*- coding: utf-8 -*-
##############################################################################
#
#    PT. IKONSULTAN INOVATAMA
#
#    Copyright (C) 2023-TODAY PT. IKONSULTAN INOVATAMA
#    Author: ORISON S
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'IKON Custom Timesheet',
    'summary': 'IKON Custom Timesheet for Odoo 16',
    'version': '16.0.1.1.0',
    'category': 'Human Resources',
    'company': 'PT. IKONSULTAN INOVATAMA',
    'description': """
        This module allows timesheet approver to see, approve and reject employee timesheet submission.
    """,
    'author': 'Orison Situmorang',
    'depends': ['base', 'hr_timesheet', 'graphql_base', 'web'],
    "external_dependencies": {"python3.9": ["graphene", "graphql-core"]},
    'data': [
        'security/ir.model.access.csv',
        'views/email_template.xml',
        'views/inherit_timesheet.xml',
        'views/timesheet_calendar_view.xml',
        'views/timesheet_report_calender_view.xml',
        'views/timesheet_validation_groups.xml',
        'views/timesheet_validation.xml',
    ],
    'installable': True,
    'application': False,
}
