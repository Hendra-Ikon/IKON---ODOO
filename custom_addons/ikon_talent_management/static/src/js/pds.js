odoo.define('your_module_name.my_script', function (require) {
    "use strict";

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var rpc = require('web.rpc');

    console.log("***************************")
    var _t = core._t;

    core.bus.on('model.hr.applicant', this, function (ev) {
        console.log("Event triggered:", ev);

        // Handle changes in the "hr.applicant" model
        var changedRecordIds = ev.data.ids;

        // Check if the changed records include the desired record(s) based on your logic
        // For example, you may want to check if a specific field like "stage_id" has changed
        alert("Before rpc.query");
        console.log(">>>>>>>>>><<<<<<<<<<<<<")
        rpc.query({
            model: 'hr.applicant',
            method: 'search_read',
            args: [changedRecordIds, ['stage_id']],
        }).then(function (records) {
            alert("Inside rpc.query callback");
            var recordsWithStageChange = records.filter(function (record) {
                // Customize this condition based on your logic
                let desiredStageId = "PDS Submission";
                return record.stage_id && record.stage_id[0] === desiredStageId;
            });

            if (recordsWithStageChange.length > 0) {
                // Perform actions or trigger the dialog as needed
                console.log("STAGE CHANGES")

                showDialog();
            }
        });
    });

    function showDialog() {
        var dialog = new Dialog(this, {
            title: _t('My Dialog Title'),
            size: 'medium',
            buttons: [
                {text: _t('OK'), classes: 'btn-primary', click: _onOK, close: true},
                {text: _t('Close'), classes: 'btn-secondary', close: true},
            ],
            $content: $('<div>').text(_t('Dialog content goes here.')),
        });

        dialog.open();
    }

    function _onOK() {
        // Handle OK button click
        console.log("OK button clicked!");
        // Add your custom logic here
    }
});


// odoo.define('your_module_name.my_script', function (require) {
//     "use strict";
//
//     var publicWidget = require('web.public.widget');
//     var core = require('web.core');
//     var Dialog = require('web.Dialog');
//
//     var _t = core._t;
//
//     publicWidget.registry.my_script = publicWidget.Widget.extend({
//         selector: '.my-script-selector',
//
//         start: function () {
//             console.log("**** UWUW ****")
//             this.$el.on('click', this._onClick.bind(this));
//         },
//
//         _onClick: function () {
//             this.showDialog();
//         },
//
//
//         showDialog: function () {
//             var self = this;
//
//             var dialog = new Dialog(this, {
//                 title: _t('My Dialog Title'),
//                 size: 'medium',
//                 buttons: [
//                     {text: _t('OK'), classes: 'btn-primary', click: this._onOK.bind(this), close: true},
//                     {text: _t('Close'), classes: 'btn-secondary', close: true},
//                 ],
//                 $content: $('<div>').text(_t('Dialog content goes here.')),
//             });
//
//             dialog.open();
//         },
//
//
//
//         _onOK: function () {
//             // Handle OK button click
//             console.log("OK button clicked!");
//             // Add your custom logic here
//         },
//     });
//
//     return publicWidget.registry.my_script;
// });
//
// //
// //
