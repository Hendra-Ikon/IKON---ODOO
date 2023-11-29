odoo.define('your_module.date_custom', function (require) {
    'use strict';

    var core = require('web.core');
    var Widget = require('web.Widget');
    var fieldRegistry = require('web.field_registry');
    var $ = core.$;

    var CustomDatePicker = Widget.extend({
        start: function () {
            this.$el.datepicker({
                format: 'mm/yyyy',
                autoclose: true,
                todayHighlight: true,
                clearBtn: true
            });

            // Customize initialization if needed
            this.$el.datepicker('setViewMode', 'months');
            this.$el.datepicker('setStartDate', '01/1900');
            this.$el.datepicker('setEndDate', '12/2100');
        },
    });

    fieldRegistry.add('date', CustomDatePicker);

    return CustomDatePicker;
});
