/** @odoo-module **/

import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons.prototype, {
    async onClickClearAll() {
//        console.log("Clear all button clicked");
        const order = this.pos.get_order();
        const lines = order.get_orderlines();
        for (const line of lines) {
            order.removeOrderline(line);
        }
    }
});

