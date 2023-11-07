/** @odoo-module **/
import { registerPatch } from '@mail/model/model_core';
import { registerModel } from '@mail/model/model_core';
import { attr, one } from '@mail/model/model_field';
import { clear, insert, link } from '@mail/model/model_field_command';

/** @odoo-module **/
var rpc = require('web.rpc');
registerPatch({
    name: 'Chatter',
    recordMethods: {
        onClickDetailLog: async function () {
            if (this.composerView && this.composerView.composer.isLog) {
                this.update({ composerView: clear() });
            } else {
                this.showLogDetail();
            }
        },
        showLogDetail() {
            this.update({ composerView: {} });
            this.composerView.composer.update({ isLog: true });
            this.focus();
        },
    }
});
