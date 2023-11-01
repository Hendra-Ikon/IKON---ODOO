odoo.define('crm_ikon.contact_list_import_button', function(require) {
    "use strict";
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var TreeButton = ListController.extend({
        buttons_template: 'crm_ikon.list_import_button',
        events: _.extend({}, ListController.prototype.events, {
            'click .list_open_import_action': '_OpenImportAction',
        }),
        _OpenImportAction: function() {
             window.location.href = "/web#menu_id=113&model=res.partner&action=import"
        }
    });
    var ContactListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TreeButton,
        }),
    });
    viewRegistry.add('crm_ikon_button_list', ContactListView);
 });