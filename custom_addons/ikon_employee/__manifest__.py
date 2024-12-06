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
    'name': 'IKON Custom Employee',
    'summary': 'IKON Custom Employee for Odoo 16',
    'version': '16.0.1.1.0',
    'category': 'Human Resources',
    'company': 'PT. IKONSULTAN INOVATAMA',
    'description': """
        This module allows assigning multiple user approvers for employee timesheets, leaves, and expenses.
    """,
    'author': 'Orison Situmorang',
    'depends': ['hr', 'hr_timesheet', 'hr_holidays', 'hr_expense'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'application': False,
}
