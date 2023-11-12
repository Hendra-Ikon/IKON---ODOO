# import os
# from odoo import http
# from odoo.http import request
#
# class PDSController(http.Controller):
#
#     @http.route("/pds/data", type='http', auth='user', website=True)
#     def pds_route(self):
#
#         record = request.env['pds.data'].search([])
#         # return request.render("ikon_talent_management.custom_pds_data", {'record': record})
#         print(record.fullname)
#         return request.render("ikon_talent_management.view_pds_form")
#         # return record
#         # return "<h1>TEST</h1>"
