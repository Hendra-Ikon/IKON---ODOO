from odoo import models,fields, api, tools
import logging

logger = logging.getLogger(__name__)

class CrmProductTemplate(models.Model):
    _inherit = "product.template"
    
    @tools.ormcache()
    def _get_default_category_id(self):
        # Deletion forbidden (at least through unlink)
        if self.is_term_payment():
            return self.env.ref('crm_ikon.service_category_02')
        return self.env.ref('crm_ikon.service_category_01')
    
    def is_term_payment(self):
        return self.env.context.get('source') == 'term_payment'
    
    
    purchase_ok = fields.Boolean(default=False)
    detailed_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service')], string='Type', default='service', required=True, readonly=True)
    product_tag_ids = fields.Many2many('product.tag', 'product_tag_product_template_rel', string='Service Tags')
    categ_id = fields.Many2one(
        'product.category', 'Service Category',
        change_default=True, default=_get_default_category_id, required=True, readonly=True)
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self.is_term_payment():
            args = args + [('type', '=', 'service'), ('categ_id', '=', self.env['product.category'].search([('complete_name', '=', 'Payment')]).id)]
        else:
            args = args + [('type', '=', 'service'), ('categ_id', '=', self.env['product.category'].search([('complete_name', '=', 'Service')]).id)]
        return super(CrmProductTemplate, self).name_search(name, args, operator, limit)
    
    @api.model
    def web_search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, count_limit=None):
        """
        Performs a search_read and a search_count.

        :param domain: search domain
        :param fields: list of fields to read
        :param limit: maximum number of records to read
        :param offset: number of records to skip
        :param order: columns to sort results
        :return: {
            'records': array of read records (result of a call to 'search_read')
            'length': number of records matching the domain (result of a call to 'search_count')
        }
        """
        
        domain.insert(0, '&')
        domain.append(['type', '=', 'service'])
        domain.insert(2, '&')
        
        if self.is_term_payment():
            domain.append(['categ_id', '=', self.env['product.category'].search([('complete_name', '=', 'Payment')]).id])
        else:
            domain.append(['categ_id', '=', self.env['product.category'].search([('complete_name', '=', 'Service')]).id])
        
        records = self.search_read(
            domain, fields, offset=offset, limit=limit, order=order)

        if not records:
            return {
                'length': 0,
                'records': []
            }
        current_length = len(records) + offset
        limit_reached = len(records) == limit
        force_search_count = self._context.get('force_search_count')
        count_limit_reached = count_limit and count_limit <= current_length
        if limit and ((limit_reached and not count_limit_reached) or force_search_count):
            length = self.search_count(domain, limit=count_limit)
        else:
            length = current_length
        return {
            'length': length,
            'records': records
        }

    @api.model
    def _post_hook_payment(self):
        payment = self.search([('name', '=', 'Down payment')])
        if payment:
            payment.name = 'Term Payment'
    
    @api.model
    def _uninstall_hook_payment(self):
        payment = self.search([('name', '=', 'Term Payment')])
        if payment:
            payment.name  = "Down payment"
            
class CrmProductProduct(models.Model):
    _inherit = "product.product"
    
    categ_name = fields.Char(related='product_tmpl_id.categ_id.complete_name', store=True) 
    
    def is_term_payment(self):
        return self.env.context.get('source') == 'term_payment'
    
    def is_downpayment(self):
        return self.env.context.get("is_downpayment")
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self.is_term_payment() and self.is_downpayment():
            args = args + [('categ_id', '=', 'Payment')]
        else:
            args = args + [('categ_id', 'in', ('Service','Payment'))]
            
        return super(CrmProductProduct, self).name_search(name, args, operator, limit)
    
    @api.model
    def web_search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, count_limit=None):
        """
        Performs a search_read and a search_count.

        :param domain: search domain
        :param fields: list of fields to read
        :param limit: maximum number of records to read
        :param offset: number of records to skip
        :param order: columns to sort results
        :return: {
            'records': array of read records (result of a call to 'search_read')
            'length': number of records matching the domain (result of a call to 'search_count')
        }
        """
        if self.is_term_payment() and self.is_downpayment():
            domain.insert(0, '&')
            domain.append(['categ_name', '=', 'Payment'])
        else:
            domain.insert(0, '&')
            domain.append(['categ_name', 'in', ('Service', 'Payment')])
            
        records = self.search_read(
            domain, fields, offset=offset, limit=limit, order=order)
        
        if not records:
            return {
                'length': 0,
                'records': []
            }
        current_length = len(records) + offset
        limit_reached = len(records) == limit
        force_search_count = self._context.get('force_search_count')
        count_limit_reached = count_limit and count_limit <= current_length
        if limit and ((limit_reached and not count_limit_reached) or force_search_count):
            length = self.search_count(domain, limit=count_limit)
        else:
            length = current_length
        return {
            'length': length,
            'records': records
        }
