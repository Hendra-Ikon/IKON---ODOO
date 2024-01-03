// odoo.define('your_module_name.custom_widget', function (require) {
//     "use strict";
//
//     var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
//     var registry = require('web.core.registry');
//
//     var CustomResumeWidget = FieldOne2Many.extend({
//         init: function () {
//             this._super.apply(this, arguments);
//             this.fieldsToShow = ['resume_dateStart', 'resume_dateEnd', 'rsm_com_name', 'rsm_com_job_title', 'rsm_com_projectDes'];
//         },
//
//         _render: function () {
//             this._super.apply(this, arguments);
//             this._renderCustomContent();
//         },
//
//         _renderCustomContent: function () {
//             var self = this;
//             var $content = this.$('.o_field_one2many_list');
//
//             this.value.forEach(function (record) {
//                 var $row = $('<tr class="o_data_row cursor-default">');
//                 self.fieldsToShow.forEach(function (fieldName) {
//                     var $cell = $('<td>', { class: 'o_data_cell', text: record.data[fieldName] || '' });
//                     $row.append($cell);
//                 });
//                 $content.append($row);
//             });
//         },
//     });
//
//     registry.add('mycustom_resume_one2many', CustomResumeWidget);
//
//     return {
//         CustomResumeWidget: CustomResumeWidget,
//     };
// });

// /** @odoo-module */

import { registry} from "@web/core/registry";

// /** @odoo-module */
//
// import { registry} from "@web/core/registry";
// import { formatDate} from "@web/core/l10n/dates";
// import {SkillsX2ManyField} from "@hr_skills/fields/skills_one2many";
// import {CommonSkillsListRenderer} from "@hr_skills/views/skills_list_renderer";
// // import { CommonSkillsListRenderer } from "../views/skills_list_renderer";
//
//
// export class CustomResumeListRenderer extends CommonSkillsListRenderer {
//     get groupBy() {
//         return 'pds_resume';
//     }
//
//     get colspan() {
//         if (this.props.activeActions) {
//             return 3;
//         }
//         return 2;
//     }
//
//     formatDate(date) {
//         return formatDate(date);
//     }
//
//     // Override the method to customize the display of values
//     formatResumeField(record) {
//         const startDate = this.formatDate(record.data.resume_dateStart);
//         const endDate = this.formatDate(record.data.resume_dateEnd);
//         const companyName = record.data.rsm_com_name;
//         const jobTitle = record.data.rsm_com_job_title;
//
//         return `${startDate} - ${endDate} | ${companyName} | ${jobTitle}`;
//     }
//
//     getResumeField(record) {
//         return this.formatResumeField(record);
//     }
// }
// CustomResumeListRenderer.template = "ikon_talent_management.resume";
// //
// // CustomResumeListRenderer.rowsTemplate = "ikon_talent_management.ResumeListRenderer.Rows";
// // CustomResumeListRenderer.recordRowTemplate = "ikon_talent_management.ResumeListRenderer.RecordRow";
//
// export class CustomResumeX2ManyField extends SkillsX2ManyField {}
// CustomResumeX2ManyField.components = {
//     ...SkillsX2ManyField.components,
//     ListRenderer: CustomResumeListRenderer,
// };
//
// registry.category("fields")
//     .add("custom_resume_one2many", CustomResumeX2ManyField);
//
//
//
// console.log(CustomResumeListRenderer)




// odoo.define('ikon_talent_management.tes1', function (require) {
//     "use strict";
//
//     var relationalFields = require('web.relational_fields');
//     var registry = require('web.field_registry');
//     var FieldOne2ManyCustom = relationalFields.FieldOne2Many.extend({
//         _renderEdit: function () {
//             this._super.apply(this, arguments);
//             this.$('.o_form_field_one2many_list').on('click', '.o_data_row', this._onRowClicked.bind(this));
//         },
//
//         _onRowClicked: function (ev) {
//             ev.preventDefault();
//             ev.stopPropagation();
//             var recordID = $(ev.currentTarget).data('id');
//             var self = this;
//
//             if (recordID) {
//                 this._rpc({
//                     model: this.field.relation,
//                     method: 'read',
//                     args: [[recordID], ['resume_dateStart', 'resume_dateEnd', 'rsm_com_name', 'rsm_com_job_title']],
//                 }).then(function (data) {
//                     if (data && data.length) {
//                         var values = data[0];
//                         var displayValue = values['resume_dateStart'] + ' - ' + values['resume_dateEnd'] +
//                             ' | ' + values['rsm_com_name'] + ' | ' + values['rsm_com_job_title'];
//
//                         self.$('.o_data_row[data-id=' + recordID + '] .o_data_cell:first').text(displayValue);
//                     }
//                 });
//             }
//         },
//     });
//
//     registry.add('custom_one2many_field', FieldOne2ManyCustom);
//
//     return {
//         FieldOne2ManyCustom: FieldOne2ManyCustom,
//     };
//
// });

