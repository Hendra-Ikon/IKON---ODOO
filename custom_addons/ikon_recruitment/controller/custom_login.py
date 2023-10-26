import logging

from odoo import http
from odoo.http import route, request
_logger = logging.getLogger(__name__)

class CustomLogin(http.Controller):

    @http.route('/tes/login', type='http', auth='public', website=True)
    def custom_login(self, **kw):

        _logger.info("**************** HALLOOOOO ********************")
        print("**************** HALLOOOOO ********************")

        return "<h1>Hello, World</h1>"