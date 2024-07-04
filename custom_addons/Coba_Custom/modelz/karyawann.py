from odoo import api, fields, models
from odoo.exceptions import ValidationError

class KaryawannIkon(models.Model):
    _name = "karyawann.ikon"
    _inherit = ['mail.thread']
    _description = "Karyawann Records"

    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string="Age", required=True, tracking=True)
    married = fields.Boolean(string="Married?", tracking=True)
    noted = fields.Text(string="Notes")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")

    capitalized_name = fields.Char(string='Capitalized Name', compute='_compute_capitalized_name', store=True)
    ref = fields.Char(string="Reference", default=lambda self: ('New'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list :
            vals['ref'] = self.env['ir.sequence'] .next_by_code('karyawan.ikon')
        return super(KaryawannIkon, self). create(vals_list)
    
    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(("Age has to be recorded!"))

    @api.depends('name')
    def _compute_capitalized_name(self):
        for record in self:
            if record.name:
                record.capitalized_name = record.name.upper()
            else:
                record.capitalized_name = ''

    payment_term_id = fields.Many2one(
        'account.payment.term', 
        string='Payment Terms',
        context={},
        domain=[('company_id', '=', False), ('company_id', '=', 'company_id')]
    )

    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 18:
            self.noted = 'This employee is a minor.'
        else:
            self.noted = 'This employee is an adult.'

    message_follower_ids = fields.One2many(
        'mail.followers', 'res_id',
        domain=lambda self: [('res_model', '=', self._name)],
        string='Followers')
    message_ids = fields.One2many(
        'mail.message', 'res_id',
        domain=lambda self: [('model', '=', self._name)],
        string='Messages')
