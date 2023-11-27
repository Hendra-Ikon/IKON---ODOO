/** @odoo-module **/
import { useSetupView } from "@web/views/view_hook";
import { FormController } from "@web/views/form/form_controller";
import { ListController } from "@web/views/list/list_controller";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { FormStatusIndicator } from "@web/views/form/form_status_indicator/form_status_indicator";

const { useRef } = owl;

// Function to handle auto-save disabling for Form views
const formSetup = function () {
    const rootRef = useRef("root");
    useSetupView({
        beforeLeave: () => {
            if (this.model.root.isDirty) {
                console.log("leaving without saving...")
                $('.o_form_button_cancel').trigger('click')
                return true;
            }
        },
    });
    const result = FormController.prototype.setup.apply(this, arguments);
    return result;
};
FormController.prototype.setup = formSetup;

// Function to handle auto-save disabling for List views
const listSetup = function () {
    useSetupView({
        rootRef: this.rootRef,
        beforeLeave: () => {
            const list = this.model.root;
            const editedRecord = list.editedRecord;
            console.log("editedRecord", editedRecord);
            if (editedRecord && editedRecord.isDirty) {
                if (confirm("Do you want to save changes Automatically?")) {
                    if (!list.unselectRecord(true)) {
                        throw new Error("View can't be saved");
                    }
                } else {
                    this.onClickDiscard();
                    return true;
                }
            }
        },
    });
    const result = ListController.prototype.setup.apply(this, arguments);
    return result;
};
ListController.prototype.setup = listSetup;

// // Function to handle auto-save disabling for Kanban views
// const originalKanbanSetup = KanbanController.prototype.setup;
//
// const kanbanSetup = function () {
//     useSetupView({
//         beforeLeave: () => {
//             const kanban = this.model.root;
//             const editedRecord = kanban.editedRecord;
//             console.log("editedRecord", editedRecord);
//             if (editedRecord && editedRecord.isDirty) {
//                 if (confirm("Do you want to save changes Automatically?")) {
//                     // Handle saving logic for Kanban view
//                     // Add your specific logic here
//                 } else {
//                     this.onClickDiscard();
//                     return true;
//                 }
//             }
//         },
//     });
//     originalKanbanSetup.apply(this, arguments);
// };
//
// KanbanController.prototype.setup = kanbanSetup;
//


// /** @odoo-module **/
// odoo.define('your_module_name.your_js_file_name', function (require) {
//     "use strict";
//
//     var AbstractField = require('web.AbstractField');
//     var field_registry = require('web.field_registry');
//
//     var YourCustomField = AbstractField.extend({
//         init: function () {
//             this._super.apply(this, arguments);
//         },
//         _render: function () {
//             this._rpc({
//                 model: 'crm.lead',
//                 method: 'get_toggle_confirm_value',
//                 args: [this.recordData.id.value],
//             }).then(function (result) {
//                 console.log("Toggle Confirm Value:", result);
//                 // Now you can use the result as needed
//             });
//         },
//     });
//
//     field_registry.add('your_custom_field', YourCustomField);
//
//     return YourCustomField;
// });



// import {useSetupView} from "@web/views/view_hook";
// import {FormController} from "@web/views/form/form_controller";
// import {ListController} from "@web/views/list/list_controller";
// import { KanbanController } from "@web/views/kanban/kanban_controller";
// import Dialog from 'web.Dialog';
// import {FormStatusIndicator} from "@web/views/form/form_status_indicator/form_status_indicator";
// import core from 'web.core';
//
// const _t = core._t;
//
// const {useRef, toRaw, toColumn} = owl;
//
// const oldSetup = FormController.prototype.setup;
// const oldKanbanSetup = KanbanController.prototype.setup;
// const oldonPagerUpdated = FormController.prototype.onPagerUpdate;
// console.log("web_no_auto_save loaded");
//
// const Formsetup = function () {
//     console.log("setup from CIUSTOM");
//
//     const rootRef = useRef("root");
//     useSetupView({
//         beforeLeave: () => {
//             if (this.model.root.isDirty) {
//                 console.log("leaving without saving...")
//                 $('.o_form_button_cancel').trigger('click')
//                 return true;
//             }
//         },
//     });
//     const result = oldSetup.apply(this, arguments);
//
//     return result;
// };
// FormController.prototype.setup = Formsetup;
//
// const onPagerUpdate = await function () {
//     this.model.root.askChanges();
//
//     if (this.model.root.isDirty) {
//         console.log("leaving without saving..")
//         // if (confirm("Do you want to save changes Automatically?")) {
//         //     return oldonPagerUpdated.apply(this, arguments);
//         // }
//         this.discard();
//         return true;
//     }
//     return oldonPagerUpdated.apply(this, arguments);
// };
//
// //assign setup to FormController
//
// FormController.prototype.onPagerUpdate = onPagerUpdate;
//
// // FormStatusIndicator.template = 'web_no_auto_save.FormStatusIndicator';
//
// const ListSuper = ListController.prototype.setup;
// const Listsetup = function () {
//     console.log("setup from List CIUSTOM");
//
//     useSetupView({
//         rootRef: this.rootRef,
//         beforeLeave: () => {
//             const list = this.model.root;
//             const editedRecord = list.editedRecord;
//             console.log("editedRecord", editedRecord);
//             if (editedRecord && editedRecord.isDirty) {
//                 if (confirm("Do you want to save changes Automatically?")) {
//                     if (!list.unselectRecord(true)) {
//                         throw new Error("View can't be saved");
//                     }
//                 } else {
//                     this.onClickDiscard();
//                     return true;
//                 }
//             }
//         },
//     });
//     const result = ListSuper.apply(this, arguments);
//     return result;
// };
// ListController.prototype.setup = Listsetup;
//
// const KanbanSetup = function () {
//     console.log("setup from Kanban Custom");
//
//     const rootRef = useRef("root");
//     useSetupView({
//         rootRef: this.rootRef,
//         // if (model ) {
//         //
//         // }
//         beforeLeave: () => {
//             // confirm("Halooo")
//             console.log("Take it here")
//             if (this.model.root.isDirty) {
//                 console.log("leaving without saving...")
//                 // Handle leaving without saving in the Kanban view.
//                 return true;
//             }
//         },
//     });
//
//     const result = oldKanbanSetup.apply(this, arguments);
//     return result;
// };
//
// KanbanController.prototype.setup = function () {
//     const result = KanbanSetup.apply(this, arguments);
//
//     console.log("State is in CRM LEAD");
//
//     // Save the original setup method for later use
//     const originalSetup = this.setup;
//
//     // Override the setup method
//     this.setup = function () {
//         // Call the original setup method
//         originalSetup.apply(this, arguments);
//
//         // Listen for changes in the stage_id field
//         this.model.on('change:data', this, function () {
//             const stageId = this.model.data[this.modelName][0].data.stage_id.res_id;
//
//             // Check if the dragged element is a CRM Opportunity card
//             const isOpportunityCard = this.$buttons.hasClass('o_crm_lead_kanban') && this.modelName === 'crm.lead';
//
//             if (isOpportunityCard) {
//                 console.log("Stage ID is changed to:", stageId);
//
//                 // Adding a customized confirmation dialog
//                 const confirmationDialog = new Dialog(this, {
//                     title: "Confirmation",
//                     size: 'medium',
//                     $content: $('<div>', { html: "Are you sure you want to proceed?" }),
//                     buttons: [{
//                         text: _t("Cancel"),
//                         classes: 'btn-secondary',
//                         click: function () {
//                             // User clicked "Cancel"
//                             console.log("User canceled. Reloading the page without saving changes.");
//                             location.reload(); // Reload the page without saving changes
//                         },
//                     }, {
//                         text: _t("Proceed"),
//                         classes: 'btn-primary',
//                         click: function () {
//                             // User clicked "Proceed"
//                             console.log("User confirmed. Proceeding with the original functionality.");
//                             // You can add your original functionality here
//
//                             // Close the dialog
//                             confirmationDialog.close();
//                         },
//                     }],
//                 });
//
//                 // Open the confirmation dialog
//                 confirmationDialog.open();
//             }
//         });
//     };
//
//     return result;
// };


// KanbanController.include({
//     setup: function () {
//         const result = this._super.apply(this, arguments);
//
//         // Check if the dragged element is a CRM Opportunity card
//         const isOpportunityCard = this.$buttons.hasClass('o_crm_lead_kanban') && this.modelName === 'crm.lead';
//
//         if (isOpportunityCard) {
//             console.log("State is in CRM LEAD");
//
//             // Adding a customized confirmation dialog
//             const confirmationDialog = new Dialog(this, {
//                 title: "Confirmation",
//                 size: 'medium',
//                 $content: $('<div>', { html: _t("Are you sure you want to proceed?") }),
//                 buttons: [{
//                     text: _t("Cancel"),
//                     classes: 'btn-secondary',
//                     click: function () {
//                         // User clicked "Cancel"
//                         console.log("User canceled. Reloading the page without saving changes.");
//                         location.reload(); // Reload the page without saving changes
//                     },
//                 }, {
//                     text: _t("Proceed"),
//                     classes: 'btn-primary',
//                     click: function () {
//                         // User clicked "Proceed"
//                         console.log("User confirmed. Proceeding with the original functionality.");
//                         // You can add your original functionality here
//
//                         // Close the dialog
//                         confirmationDialog.close();
//                     },
//                 }],
//             });
//
//             // Open the confirmation dialog
//             confirmationDialog.open();
//         }
//
//         return result;
//     },
// });


