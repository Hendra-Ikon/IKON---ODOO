/** @odoo-module */

// import { BasicModel } from "@web/views/js/core/basic_model";
// import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";



export class CustomOne2ManyResume extends Component {

    val = ["Satu", "Dua"]

    // setup() {
    //
    // }
    /**
     * @param {Object} state
     * @param {Object} param1
     *
     *
     */
    constructor(state, { update }) {
        super(state, { update });
        this.update = update;
    }

    get data() {
        return this.props.data;
    }

    /**
     * @param {Array} newValue
     */
    onChange(newValue) {
        this.props.update(newValue);
    }
}


// console.log(data)

CustomOne2ManyResume.template = "ikon_talent_management.CustomKanbanView"
// CustomOne2ManyResume.template = xml`
// <div>TEST</div>
// <t t-foreach="val" t-as="record" t-key="record.id">
//     <div>
//         <span t-esc="record.resume_dateStart"/>
//         <span t-esc="record.resume_dateEnd"/>
//         <span t-esc="record.rsm_com_name"/>
//         <span t-esc="record.rsm_com_job_title"/>
//         <!-- Add more fields as needed -->
//     </div>
// </t>
// `;

// CustomOne2ManyResume.defaultProps = {
//     value: "Haiiiiiii"
// }

CustomOne2ManyResume.props = {
    value: { type: Array},
    // update: { type: Function, optional: true },
    ...standardFieldProps,
};

registry.category("fields").add("custom_one2many_resume", CustomOne2ManyResume);

