/** @odoo-module **/
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(Orderline.prototype, {
    setup() {
        super.setup();
        this.numberBuffer = useService("number_buffer");
    },
    async onClickClearItem() {
        console.log("Clear Item Button Clicked")
        this.numberBuffer.sendKey("Backspace");
        this.numberBuffer.sendKey("Backspace");
    }
});