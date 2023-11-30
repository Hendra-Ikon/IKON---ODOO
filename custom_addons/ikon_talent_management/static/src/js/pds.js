odoo.define('crm_ikon.access_toggle_confirm', function (require) {
    'use strict';

    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;

    // Access the 'toggle_confirm' field for CRMLead records
    rpc.query({
        model: 'crm.lead',
        method: 'read',
        args: [[], ['stage_id']],
    }).then(function (result) {
        // 'result' is an array of record data, each containing the 'toggle_confirm' field
        result.forEach(function (recordData) {
            console.log('toggle_confirm value for record ' + recordData.id + ':', recordData.toggle_confirm);
            // if (result === false) {
            //     alert("HIYAAAA")
            // }
        });
        // if (result === false) {
        //     alert("HIYAAAA")
        // }
        // console.log(result)
    });
});
