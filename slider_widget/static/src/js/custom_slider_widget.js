/** @odoo-module **/
import { Component } from "@odoo/owl";
import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { debounce } from "@web/core/utils/timing";

export class RangeSliderField extends Component {
  static template = 'FieldRangeSlider';
  setup() {
    const { min, max, step } = this.__owl__.parent.props.fieldInfo.options || {};
    this.state = useState({
        value: this.props.record.data[this.props.name],
        min: min ?? 0,
        max: max ?? 100,
        step: step ?? 1,
    });
    this._debouncedWrite = debounce(this._writeToServer.bind(this), 300);
  }
  getValue(e) {
        this.state.value = e.target.value;
        this._debouncedWrite();
  }
   _writeToServer() {
        const config = this.env.model.config;
        this.env.model.orm.write(config.resModel,
                                [config.resId], {
                                [this.props.name]: this.state.value,
        });
   }
}
export const rangeSliderField = {
   component: RangeSliderField,
   displayName: "RangeSliderField",
   supportedTypes: ["int"],
};
registry.category("fields").add("range_slider", rangeSliderField);