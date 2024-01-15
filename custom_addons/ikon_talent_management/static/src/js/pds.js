// odoo.define('crm_ikon.access_toggle_confirm', function (require) {
//     'use strict';
//
//     var core = require('web.core');
//     var rpc = require('web.rpc');
//
//     var _t = core._t;
//
//     // Access the 'toggle_confirm' field for CRMLead records
//     rpc.query({
//         model: 'crm.lead',
//         method: 'read',
//         args: [[], ['stage_id']],
//     }).then(function (result) {
//         // 'result' is an array of record data, each containing the 'toggle_confirm' field
//         result.forEach(function (recordData) {
//             console.log('toggle_confirm value for record ' + recordData.id + ':', recordData.toggle_confirm);
//
//         });
//
//     });
// });

// import public_widget from "../../../../../addons/web/static/src/legacy/js/public/public_widget";
//

odoo.define('ikon_talent_management.Many2many_tag', function (require) {
    console.log("LOADED")
    var PublicWidget = require('web.public.widget');
    var NewData = PublicWidget.Widget.extend({
        selector: '.new-get_data', start: function () {
            $('.js-many2many-tag').select2();
        },
    });
    PublicWidget.registry.Many2many_tag = NewData;
    return NewData;
});
