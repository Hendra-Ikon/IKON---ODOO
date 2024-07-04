from odoo import api, fields, models
from odoo.exceptions import ValidationError
# from odoo.tools.translate import _

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread']
    _description = "patient record"

    name = fields.Char(string="Name", tracking=True)
    age = fields.Integer(string="Age", tracking=  True)
    is_child = fields.Boolean(string="is child?", tracking=True)
    noted = fields.Text(string="Notes", compute="_compute_notes", store=True)
    gender = fields.Selection([('male', "Male"), ('female', "Female"), ("others", "Others")], string="Gender", tracking=True)
    # customer = fields.Many2one('res.partner', string="customer")
    capitalized_name = fields.Char(string='Capitalized Name', compute='_compute_capitalized_name', store=True)
    ref = fields.Char(string="Reference", default=lambda self:('New'))
    a = fields.Char(string="A", tracking=True)
    b = fields.Char(string="B", tracking=True)
    dates = fields.Date(string="Dates")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super (HospitalPatient, self).create(vals_list)

    @api.constrains('age', 'is_child')
    def _check_age(self):
        for rec in self:
            if rec.age == 0: 
                raise ValidationError("Age harus diisi")

    @api.depends('name', 'age')
    def _compute_notes(self):
        for rec in self:
            if rec.name and rec.age:
                rec.noted = ("nama " + rec.name + " berumur " + str(rec.age))
            else:
                rec.noted = ''

    @api.onchange('age')
    def _onchange_age(self):
        if self.age <= 10:
            self.is_child = True
        else:
            self.is_child = False