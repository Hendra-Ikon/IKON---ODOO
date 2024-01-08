from odoo import fields, api, models, tools


class CsBankAcc(models.TransientModel):
    _inherit = "account.payment.register"

    bank_id = fields.Many2one("custom.bank.acc", string="Bank Alias")
    # custom_bank_name = fields.Char(string="Bank Name")
    # custom_bank_number = fields.Char(string="Bank Account Number")


class FKBankAcc(models.TransientModel):
    _name = "custom.bank.acc"

    # acc_pay_id = fields.Many2one('account.payment.register', string='Bank Alias')
    custom_bank_name = fields.Char(string="Bank Name")
    custom_bank_number = fields.Char(string="Bank Account Number")


class BankBranch(models.Model):

    _inherit = "res.partner.bank"

    custom_bank_branch = fields.Char(string="Branch")
