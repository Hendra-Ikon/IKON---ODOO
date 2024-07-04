from odoo import http
from odoo.http import route, request

class RootRedirect(http.Controller):

    @route('/')
    def index(self, **kw):
        if http.request.env.user._is_public():
            return request.redirect('/web/login?redirect=/web/discuss')
        else:
            return request.redirect('/web')
