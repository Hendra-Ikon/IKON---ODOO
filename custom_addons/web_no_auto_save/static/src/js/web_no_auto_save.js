/** @odoo-module **/
import {useSetupView} from "@web/views/view_hook";
import {FormController} from "@web/views/form/form_controller";
import {ListController} from "@web/views/list/list_controller";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import {FormStatusIndicator} from "@web/views/form/form_status_indicator/form_status_indicator";

const {useRef, toRaw, toColumn} = owl;

const oldSetup = FormController.prototype.setup;
const oldKanbanSetup = KanbanController.prototype.setup;
const oldonPagerUpdated = FormController.prototype.onPagerUpdate;
console.log("web_no_auto_save loaded");

const Formsetup = function () {
    console.log("setup from CIUSTOM");

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
    const result = oldSetup.apply(this, arguments);

    return result;
};
FormController.prototype.setup = Formsetup;

const onPagerUpdate = await function () {
    this.model.root.askChanges();

    if (this.model.root.isDirty) {
        console.log("leaving without saving..")
        // if (confirm("Do you want to save changes Automatically?")) {
        //     return oldonPagerUpdated.apply(this, arguments);
        // }
        this.discard();
        return true;
    }
    return oldonPagerUpdated.apply(this, arguments);
};

//assign setup to FormController

FormController.prototype.onPagerUpdate = onPagerUpdate;

// FormStatusIndicator.template = 'web_no_auto_save.FormStatusIndicator';

const ListSuper = ListController.prototype.setup;
const Listsetup = function () {
    console.log("setup from List CIUSTOM");

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
    const result = ListSuper.apply(this, arguments);
    return result;
};
ListController.prototype.setup = Listsetup;

const KanbanSetup = function () {
    console.log("setup from Kanban Custom");

    const rootRef = useRef("root");
    useSetupView({
        rootRef: this.rootRef,
        // if (model ) {
        //
        // }
        beforeLeave: () => {
            // confirm("Halooo")
            console.log("Take it here")
            if (this.model.root.isDirty) {
                console.log("leaving without saving...")
                // Handle leaving without saving in the Kanban view.
                return true;
            }
        },
    });

    const result = oldKanbanSetup.apply(this, arguments);
    return result;
};

KanbanController.prototype.setup = function () {
    const result = KanbanSetup.apply(this, arguments);
    console.log("State is in CRM LEAD")
    // Check if the model is for CRM leads
    if (this.model.modelName === "crm.lead") {
        // Disable auto-save for CRM leads specifically

        this.renderer.arch.attrs.on_change = 'onChange';

        // Add a custom method to save manually after drag and drop
        this.onSaveAfterDragDrop = async function () {
            // Add your custom logic to save manually after drag and drop
            console.log("Manually save after drag and drop");
            await this.saveRecord();
        };

        // Override the default method for saving after a card is dropped
        this.onCardDropped = async function (ev) {
            await this._super.apply(this, arguments);
            await this.onSaveAfterDragDrop();
        };
    }

    return result;
};
