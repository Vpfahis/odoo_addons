/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToElement } from "@web/core/utils/render";
import { rpc } from "@web/core/network/rpc";

function chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}

publicWidget.registry.get_latest_rooms = publicWidget.Widget.extend({
    selector: '.rooms_section',
    async willStart() {
        const result = await rpc('/get_latest_rooms', {});
        console.log("Room Data",result)
        this.rooms = result.rooms || [];
    },
    start() {
        const chunkData = chunk(this.rooms, 4);
        const el = renderToElement('hostel.room_snippet_data', {
            chunks: chunkData,
        });
        this.$el.html(el);
    },
});


