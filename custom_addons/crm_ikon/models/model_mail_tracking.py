from datetime import datetime

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)



class MailTrackingCustom(models.Model):
    _inherit = 'mail.tracking.value'
    _description = 'Mail Tracking Value'
    _rec_name = 'field'
    _order = 'tracking_sequence asc'

    name_service = fields.Char(string='Service Name')

    # @api.model
    # def create_tracking_values(self, initial_value, new_value, col_name, col_info, tracking_sequence, model_name, name_services="yess"):
    #     # ... (metode create_tracking_values yang telah dijelaskan sebelumnya)
    #     pass

    # def _message_log(self, body='', subject=None, message_type='notification', subtype_id=None, partner_ids=None):
    #     if body:
    #         self.message_post(body=body, subject=subject, message_type=message_type, subtype_id=subtype_id, partner_ids=partner_ids)

    #     return True
    
    # def _message_log(self, body='', subject=None, message_type='notification', subtype_id=None, partner_ids=None):
    #     # Metode ini digunakan untuk mengirim pesan log dan merekamnya dalam benang percakapan
    #     # Di sini Anda dapat menambahkan log yang ingin Anda kirim

    #     if body:
    #         self.message_post(
    #             body=body,
    #             subject=subject,
    #             message_type=message_type,
    #             subtype_id=subtype_id,
    #             partner_ids=partner_ids,
    #         )

    #     return True
    
    @api.model
    def create_tracking_values(self, initial_value, new_value, col_name, col_info, tracking_sequence, model_name, name_services="yess"):
        tracked = True
        name_service = name_services
        # _logger.info("test",name_service)
        print("=================",name_service)
        field = self.env['ir.model.fields']._get(model_name, col_name)
        if not field:
            return {}

        values = {'field': field.id, 'field_desc': col_info['string'], 'field_type': col_info['type'], 'tracking_sequence': tracking_sequence}

        if col_info['type'] in ['integer', 'float', 'char', 'text', 'datetime', 'monetary']:
            values.update({
                
                'old_value_%s' % col_info['type']: initial_value,
                'new_value_%s' % col_info['type']: new_value
            })
        elif col_info['type'] == 'date':
            values.update({
                'name_service': name_service,
                'old_value_datetime': initial_value and fields.Datetime.to_string(datetime.combine(fields.Date.from_string(initial_value), datetime.min.time())) or False,
                'new_value_datetime': new_value and fields.Datetime.to_string(datetime.combine(fields.Date.from_string(new_value), datetime.min.time())) or False,
            })
        elif col_info['type'] == 'boolean':
            values.update({
                'name_service': name_service,
                'old_value_integer': initial_value,
                'new_value_integer': new_value
            })
        elif col_info['type'] == 'selection':
            values.update({
                'name_service': name_service,
                'old_value_char': initial_value and dict(col_info['selection']).get(initial_value, initial_value) or '',
                'new_value_char': new_value and dict(col_info['selection'])[new_value] or ''
            })
        elif col_info['type'] == 'many2one':
            values.update({
                'name_service': name_service,
                'old_value_integer': initial_value and initial_value.id or 0,
                'new_value_integer': new_value and new_value.id or 0,
                'old_value_char': initial_value and initial_value.sudo().name_get()[0][1] or '',
                'new_value_char': new_value and new_value.sudo().name_get()[0][1] or ''
            })
        else:
            tracked = False

        # Tambahkan name_service dari sale_order_line
        
        if tracked:
            return values
        return {}
    
    

    def _get_display_value(self, prefix):
            assert prefix in ('new', 'old')
            result = []
            for record in self:
                
                if record.field_type in ['integer', 'float', 'char', 'text', 'monetary']:
                    result.append(record[f'{prefix}_value_{record.field_type}'])
                elif record.field_type == 'datetime':
                    if record[f'{prefix}_value_datetime']:
                        new_datetime = record[f'{prefix}_value_datetime']
                        result.append(f'{new_datetime}Z')
                    else:
                        result.append(record[f'{prefix}_value_datetime'])
                elif record.field_type == 'date':
                    if record[f'{prefix}_value_datetime']:
                        new_date = record[f'{prefix}_value_datetime']
                        result.append(fields.Date.to_string(new_date))
                    else:
                        result.append(record[f'{prefix}_value_datetime'])
                elif record.field_type == 'boolean':
                    result.append(bool(record[f'{prefix}_value_integer']))
                else:
                    result.append(record[f'{prefix}_value_char'])
            _logger.info("oke",result)
            return result

    def _get_old_display_value(self):
        # grep : # old_value_integer | old_value_datetime | old_value_char
        return self._get_display_value('old')

    def _get_new_display_value(self):
        # grep : # new_value_integer | new_value_datetime | new_value_char
        return self._get_display_value('new')