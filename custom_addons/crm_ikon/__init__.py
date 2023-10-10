from . import models

from odoo import api, SUPERUSER_ID

def _post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.groups']._post_hook_groups()
    env['product.template']._post_hook_payment()
    env['ir.ui.menu']._install_hook_menuitem()

def _uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.groups']._uninstall_hook_groups()
    env['ir.ui.menu']._uninstall_hook_menuitem()
    env['ir.actions.actions']._uninstall_hook_action_name()
    env['product.template']._uninstall_hook_payment()
    env['crm.stage']._uninstall_hook_stage()
    env['crm.team']._uninstall_hook_team()