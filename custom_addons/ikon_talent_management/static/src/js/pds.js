odoo.define('ikon_talent_management.pds', ['web.core', 'web.Dialog', 'web.ajax', 'web.Widget'], function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Dialog = require('web.Dialog');

    var _t = core._t;

    var PopupWidget = Widget.extend({
        start: function () {
            var self = this;

            // Create a simple dialog
            var dialog = new Dialog(self, {
                title: _t("Popup Title"),
                size: 'medium',
                buttons: [
                    {text: _t("Close"), classes: 'btn-secondary', close: true},
                ],
            });

            // Add content to the dialog
            dialog.$el.append($('<div>', {class: 'popup-content'}).text("This is the content of your popup."));

            // Show the dialog
            dialog.open();

            return this._super.apply(this, arguments);
        },
    });

    core.addons['web.Dialog'] = Dialog;
    core.addons['web.Widget'] = Widget;

    core.action_registry.add('ikon_talent_management.pds', PopupWidget);

    return PopupWidget;
});

// odoo.define('ikon_talent_management.pds', function (require) {
//     "use strict";
//
//     var core = require('web.core');
//     var Widget = require('web.Widget');
//     var Dialog = require('web.Dialog');
//
//     var PdsPopup = Widget.extend({
//         events: {
//             'click .show-modal-button': '_onShowModalClick',
//         },
//
//         init: function (parent, options) {
//             this._super.apply(this, arguments);
//             this.appendTo = options.appendTo || 'body';
//         },
//
//         start: function () {
//             this.$el.appendTo(this.appendTo);
//             return this._super.apply(this, arguments);
//         },
//
//         _onShowModalClick: function () {
//             var modalContent = `
//                 <div class="modal-content">
//                     <span class="close-modal">&times;</span>
//                     <p>This is your popup modal content.</p>
//                 </div>
//             `;
//
//             Dialog.alert(this, modalContent, {
//                 title: 'Popup Modal',
//                 buttons: [
//                     { text: core._t('Close'), close: true, click: function () {} },
//                 ],
//             });
//         },
//     });
//
//     core.action_registry.add('ikon_talent_management.pds', PdsPopup);
//
//      return {
//         PdsPopup: PdsPopup,
//         Dialog: Dialog, // Add this line to declare the dependency
//         core: core,
//         Widget: Widget,
//     };
// });
