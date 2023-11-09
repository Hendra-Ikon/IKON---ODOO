odoo.define('crm_ikon.LogDetail', function (require) {
    'use strict';
    let __exports = {};

    const { registerPatch } = require('@mail/model/model_core');
    const { clear } = require('@mail/model/model_field_command');
    const rpc = require('web.rpc');

    let logDetailData = [];

    registerPatch({
        name: 'Chatter',
        recordMethods: {
            onClickDetailLog: async function () {
                if (this.composerView && this.composerView.composer.isLog) {
                    this.update({ composerView: clear() });
                } else {
                    await this.showLogDetail();
                    this.update({ showLogDetailData: true });
                }
            },
            showLogDetail: async function () {
                let currentURL = window.location.hash;
                let idIndex = currentURL.indexOf('id=');
                if (idIndex !== -1) {
                    let idValue = currentURL.slice(idIndex + 3);
                    let saleOrderId = idValue.split('&')[0];

                    logDetailData = await rpc.query({
                        model: 'log.detail.sale', // Replace with the appropriate model name
                        method: 'search_read',
                        domain: [['sale_order_line_id', '=', parseInt(saleOrderId)]],
                        fields: ['name', 'price_old', 'price_new', 'change_date'],
                        limit: 10,
                    });

                    console.log(logDetailData);
                    this.logDetailData = JSON.stringify(logDetailData); 
                } else {
                    console.log("Parameter 'id' not found in the URL.");
                }
            },
        },
    });

    return __exports;
});
