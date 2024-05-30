
from odoo import fields, models, _
import logging
logger = logging.getLogger(__name__)
class ResUsers(models.Model):
    _inherit = "res.users"
    
    direct_active = fields.Boolean(default=False, string="Active")
    menu_id = fields.Many2one(
        comodel_name='ir.ui.menu',
        auto_join=True,
        string='Menu',
        domain=[('parent_id', '=', False)]  # Domain untuk menampilkan menu dengan parent_id = null
    )


    def dircet_check(self,uid):
        logger.info("test1", self)
        check = self.browse(uid)
        if check.direct_active:
            logger.info("check.menu_id.id", check.menu_id.id)
            return f'/web#menu_id={check.menu_id.id}'
        return '/'
    
  

        
    