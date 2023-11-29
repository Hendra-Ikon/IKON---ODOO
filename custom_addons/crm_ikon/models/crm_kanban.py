from odoo import fields, api, models, tools

class CRMLead(models.Model):

    _inherit = "crm.lead"

    toggle_confirm = fields.Boolean(string="Toogle Confirmation", default=False)

    @api.model
    def get_toggle_confirm_value(self, lead_id):
        # lead = self.browse(lead_id)
        return self.toggle_confirm

    @api.onchange("stage_id")
    def open_dialog(self):

        return self.toggle_confirm

    @api.model
    def crm_kanban_moved(self):

        return {
            'name': 'Confirmation',
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('crm_ikon.view_crm_lead_form_inherit').id,
            'view_type': 'form',
            'target': 'current',
        }


        # confirmation_msg = "Kanban card is moved. Do you want to proceed?"



        # Display confirmation popup
        # return {
        #     'warning': {
        #         'title': 'Confirmation',
        #         'message': confirmation_msg,
        #         'buttons': {
        #             'confirm': 'Yes',
        #             'cancel': 'No'
        #         },
        #     },
        # }

# from odoo import api, fields, models
#
# class CRMLead(models.Model):
#     _inherit = "crm.lead"
#
#
#     def action_open_confirmation_dialog(self):
#         confirmation_msg = "Kanban card is moved. Do you want to proceed?"
#         return {
#             'name': 'Confirmation',
#             'type': 'ir.actions.act_window',
#             'res_model': 'crm.lead',
#             'view_mode': 'form',
#             'view_id': self.env.ref('ccrm_ikon.view_crm_lead_form_inherit').id,
#             'view_type': 'form',
#             'target': 'new',
#             'context': {'default_confirmation_msg': confirmation_msg},
#         }


# from odoo import fields, api, models
# from odoo.exceptions import UserError
#
# class CRMLead(models.Model):
#
#     _inherit = "crm.lead"
#
#     @api.onchange("stage_id")
#     def crm_kanban_moved(self):
#         confirmation_msg = "Kanban card is moved. Do you want to proceed?"
#         return {
#             'confirm': {
#                 'title': 'Confirmation',
#                 'message': confirmation_msg,
#                 'buttons': [
#                     {'text': 'Proceed', 'classes': 'btn-primary', 'close': True},
#                     {'text': 'Cancel', 'classes': 'btn-secondary', 'close': True},
#                 ],
#             }
#         }
#
#
#

class PopupModel(models.Model):

    _name = "popup.crm"

    popup_message = fields.Char(string="Popup Message", default="Kanban card is moved. Do you want to proceed?")

