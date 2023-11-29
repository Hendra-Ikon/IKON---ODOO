from odoo import api, http

class MyProfile(http.Controller):

    @http.route("/custom/profile")
    def custom_profile(self):

        return http.request.render("ikon_recruitment.custom_profile_view")