odoo.define('crm_ikon.contact_kanban_import_button', function(require) {
    "use strict";
    var KanbanController = require('web.KanbanController');
    var KanbanView = require('web.KanbanView');
    var viewRegistry = require('web.view_registry');
    var KanbanButton = KanbanController.extend({
        buttons_template: 'crm_ikon.kanban_import_button',
        events: _.extend({}, KanbanController.prototype.events, {
            'click .kanban_open_import_action': '_OpenImportAction',
        }),
        _OpenImportAction: function() {
             window.location.href = "/web#menu_id=113&model=res.partner&action=import"
        }
    });
    var ContactKanbanView = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Controller: KanbanButton,
        }),
    });
    viewRegistry.add('crm_ikon_button_kanban', ContactKanbanView);
 });