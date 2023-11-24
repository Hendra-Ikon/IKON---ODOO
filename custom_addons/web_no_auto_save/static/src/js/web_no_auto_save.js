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

// Function to handle auto-save disabling for Kanban views
const originalKanbanSetup = KanbanController.prototype.setup;

const kanbanSetup = function () {
    useSetupView({
        beforeLeave: () => {
            const kanban = this.model.root;
            const editedRecord = kanban.editedRecord;
            console.log("editedRecord", editedRecord);
            if (editedRecord && editedRecord.isDirty) {
                if (confirm("Do you want to save changes Automatically?")) {
                    // Handle saving logic for Kanban view
                    // Add your specific logic here
                } else {
                    this.onClickDiscard();
                    return true;
                }
            }
        },
    });
    originalKanbanSetup.apply(this, arguments);
};

KanbanController.prototype.setup = kanbanSetup;

