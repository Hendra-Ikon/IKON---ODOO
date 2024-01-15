// /** @odoo-module */
//
// import { registry } from "@web/core/registry";
//
// import { formatDate } from "@web/core/l10n/dates";
//
// import { SkillsX2ManyField } from "./skills_one2many";
// import { CommonSkillsListRenderer } from "../views/skills_list_renderer";
//
// export class ResumeListRenderer extends CommonSkillsListRenderer {
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
//     setDefaultColumnWidths() {}
// }
// ResumeListRenderer.template = 'hr_skills.ResumeListRenderer';
// ResumeListRenderer.rowsTemplate = "hr_skills.ResumeListRenderer.Rows";
// ResumeListRenderer.recordRowTemplate = "hr_skills.ResumeListRenderer.RecordRow";
//
//
// export class ResumeX2ManyField extends SkillsX2ManyField {}
// ResumeX2ManyField.components = {
//     ...SkillsX2ManyField.components,
//     ListRenderer: ResumeListRenderer,
// };
//
// registry.category("fields")
//     .add("resume_one2many", ResumeX2ManyField);



/** @odoo-module */

import { Component, useState, useEffect } from "@odoo/owl";
import { registry } from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import { ListRenderer } from "@web/views/list/list_renderer";
import {CommonSkillsListRenderer} from "@hr_skills/views/skills_list_renderer";
import {SkillsX2ManyField} from "@hr_skills/fields/skills_one2many";
import { formatDate } from "@web/core/l10n/dates";


export class CustomOne2ManyResume extends CommonSkillsListRenderer {

    get someData() {
        return ["Satu", "dua"]

    }

    get groupBy() {
        return 'rsm_com_name';
    }

    get colspan() {
        if (this.props.activeActions) {
            return 3;
        }
        return 2;
    }

    get groupedList() {
        const grouped = {};

        for (const record of this.list.records) {
            const data = record.data;
            const group = data[this.groupBy];

            if (grouped[group[1]] === undefined) {
                grouped[group[1]] = {
                    id: parseInt(group[0]),
                    name: this.env._t(''),
                    list: {
                        records: [],
                    },
                };
            }

            grouped[group[1]].list.records.push(record);
        }
        return grouped;
    }

    formatDate(date) {
        return formatDate(date);
    }

    get showTable() {
        return this.props.list.records.length;
    }

    setDefaultColumnWidths() {}

}

CustomOne2ManyResume.template = "ikon_talent_management.CustomKanbanView";
CustomOne2ManyResume.rowsTemplate = "ikon_talent_management.CustomKanbanView.Rows";
CustomOne2ManyResume.recordRowTemplate = "ikon_talent_management.CustomKanbanView.RecordRow";

// CustomOne2ManyResume.props = {
//
//     ...standardFieldProps,
// };

export class CustomResumeField extends SkillsX2ManyField {
    // async onAdd({ context, editable } = {}) {
    //     const applicantId = this.props.record.resId;
    //     return super.onAdd({
    //         editable,
    //         context: {
    //             ...context,
    //             default_employee_id: applicantId,
    //         }
    //     });
    // }
}
CustomResumeField.components = {
    // ...SkillsX2ManyField.components,
    ListRenderer: CustomOne2ManyResume,
};

registry.category("fields").add("custom_one2many_resume", CustomResumeField);

