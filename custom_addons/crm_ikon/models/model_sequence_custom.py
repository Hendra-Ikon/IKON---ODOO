# models/models.py

from odoo import models, fields, api, _
import logging
from odoo.exceptions import AccessError, UserError, ValidationError
logger = logging.getLogger(__name__)
import re
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    
    
    def quo_set(self):
        existing_record = self.env['setting.seq.custom'].search([('ref', '=', 'Quo')], limit=1)
        
        if existing_record:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Existing Sequence',
                'res_model': 'setting.seq.custom',
                'view_mode': 'form',
                'res_id': existing_record.id,
                'target': 'new',
                'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
            }
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Sequence Quotation',
            'res_model': 'setting.seq.custom',
            'view_mode': 'form',
            'view_id': self.env.ref('crm_ikon.view_setting_seq_custom_form').id,
            'target': 'new',
            'context': {
                'default_ref': "Quo",
            },
        }
    
    def inv_set(self):
        existing_record = self.env['setting.seq.custom'].search([('ref', '=', 'Inv')], limit=1)
        
        if existing_record:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Existing Sequence',
                'res_model': 'setting.seq.custom',
                'view_mode': 'form',
                'res_id': existing_record.id,
                'target': 'new',
                'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
            }
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Sequence Invoice',
            'res_model': 'setting.seq.custom',
            'view_mode': 'form',
            'view_id': self.env.ref('crm_ikon.view_setting_seq_custom_form').id,
            'target': 'new',
            'context': {
                'default_ref': "Inv",
            },
        }
        

class ResConfigSettings(models.TransientModel):
    _name = 'setting.seq.custom'
    
    sequence_id = fields.Many2one('ir.sequence', string='Sequences')
    next_numbers = fields.Integer(related="sequence_id.number_next_actual", string='Next Numbers', compute='_compute_next_numbers', store=False, readonly=False)
    format_quo = fields.Char(string='Format Quotation')
    seq_number = fields.Integer(string="Current Seq Number")
    ref = fields.Char(string='ref', readonly=True)

    @api.constrains('format_quo')
    def _check_format_quo_keys(self):
        for record in self:
            formatted_data_str = record.format_quo

            matches = re.findall(r"(@[A-Z]+): '([^']+)'", formatted_data_str)

            valid_keys = {'@SEQ', '@MONTH', '@YEAR', '@TEXT'}
            for key, value in matches:
                if key not in valid_keys:
                    raise ValidationError(_('Invalid key found in format: %s') % key)
                   
    @api.depends('next_numbers')  # Jika ingin menghitung secara otomatis ketika field lainnya berubah
    def _compute_next_numbers(self):
        seq = self.env['ir.sequence'].search([('code', '=', 'sale.order')])

        if seq:
            self.next_numbers = seq.number_next_actual
        else:
            self.next_numbers = None  # Atau berikan nilai default yang sesuai dengan kebutuhan Anda
            
    @api.depends('next_numbers')
    def reset_seq(self):
        seq = self.env['ir.sequence'].search([('code', '=', 'sale.order')])

        if seq:
            # Mengubah nilai number_next_actual menjadi 0
            seq.write({'number_next_actual': 0})
            self.next_numbers = seq.number_next_actual

            # Menampilkan nilai yang baru di log
            logger.info("Number Next Actual after reset:", seq.number_next_actual)
        else:
            logger.warning("Sequence with code 'sale.order' not found.")

    def save(self):
        self.write({
            'format_quo': self.format_quo,
            'next_numbers': self.next_numbers,
        })
        
        seq = self.env['ir.sequence'].browse(self.sequence_id.id)
        logger.info("Settings saved successfully.", seq)
        seq.write({
            'number_next': self.next_numbers,
        })


    
