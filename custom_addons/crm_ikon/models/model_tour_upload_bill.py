from odoo import fields, models, _, Command, tools
import base64
from datetime import timedelta


class AccountTourUploadBillCustom(models.TransientModel):
    _inherit = 'account.tour.upload.bill'

    