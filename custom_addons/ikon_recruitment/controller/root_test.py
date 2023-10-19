import os
from odoo import http
from odoo.http import request



class RootTestEndpoint(http.Controller):

    @http.route('/api/test', type='http', auth='public', csrf=False)
    def api_test(self, **kwargs):
        env_test = os.environ.get('TEST_ENV')
        print(env_test)
        return f'The Environtment test is ({env_test})'
