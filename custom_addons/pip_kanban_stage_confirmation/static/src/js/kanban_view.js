odoo.define('pip_kanban_stage_confirmation.kanban_change_stage_confirmation', function (require) {
    'use strict';

    var KanbanController = require("web.KanbanController");
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var _t = core._t;

    const page = window.location === "http://localhost:8042/web#action=313&active_id=1&model=crm.lead&view_type=kanban&menu_id=193";
    KanbanController.include({
        if(page) {
            alert("HUAHUAHUA")
        },
        // confirmation pop up when drag n drop kanban to stage
        _onAddRecordToColumn: function (ev) {

            var self = this;
            var record = ev.data.record;
            var column = ev.target;
            Dialog.confirm(self, _t("Are you sure want to change stage " + ev.target.title.toUpperCase() + "?"), {
                confirm_callback: function() {
                    self.alive(self.model.moveRecord(record.db_id, column.db_id, self.handle))
                        .then(function (column_db_ids) {
                            return self._resequenceRecords(column.db_id, ev.data.ids)
                                .then(function () {
                                    _.each(column_db_ids, function (db_id) {
                                        var data = self.model.get(db_id);
                                        self.renderer.updateColumn(db_id, data);
                                    });
                                });
                        }).guardedCatch(self.reload.bind(self));
                },
                cancel_callback: function() {
                    self.reload();
                },
                title: _t('Caution'),
            });
        },
    });
});
