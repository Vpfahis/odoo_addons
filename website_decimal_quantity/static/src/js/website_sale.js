/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import wSaleUtils from "@website_sale/js/website_sale_utils";
import { rpc } from "@web/core/network/rpc";
import { Component } from "@odoo/owl";

publicWidget.registry.WebsiteSale.include({

    events: Object.assign({}, publicWidget.registry.WebsiteSale.prototype.events, {
        'click .js_add_cart_json[data-type="plus"]': '_onClickIncreaseQty',
        'click .js_add_cart_json[data-type="minus"]': '_onClickDecreaseQty',
        'change .js_quantity': '_onChangeQuantity',
    }),

    // Your custom handlers for the new quantity selectors
    _onClickIncreaseQty: function(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        var $button = $(ev.currentTarget);
        var $input = $button.siblings('.js_quantity');
        var currentQty = parseFloat($input.val()) || 1.0;
        var step = parseFloat($input.attr('step')) || 0.1;
        var max = parseFloat($input.attr('max')) || Infinity;
        var newQty = Math.min(currentQty + step, max);
        $input.val(newQty.toFixed(1)).trigger('change');
    },

    _onClickDecreaseQty: function(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        var $button = $(ev.currentTarget);
        var $input = $button.siblings('.js_quantity');
        var currentQty = parseFloat($input.val()) || 1.0;
        var step = parseFloat($input.attr('step')) || 0.1;
        var min = parseFloat($input.attr('min')) || 0;
        var newQty = Math.max(currentQty - step, min);
        $input.val(newQty.toFixed(1)).trigger('change');
    },

    _onChangeQuantity: function(ev) {
        var $input = $(ev.currentTarget);
        if ($input.data('line-id')) {
            return this._onChangeCartQuantity(ev);
        }
        var value = parseFloat($input.val());
        var min = parseFloat($input.attr('min')) || 0;
        var max = parseFloat($input.attr('max')) || Infinity;

        if (isNaN(value) || value < min) {
            value = min;
        } else if (value > max) {
            value = max;
        }
        value = Math.round(value * 10) / 10;
        $input.val(value.toFixed(1));
    },
    _onClickAddCartJSON(ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.closest('.input-group').find("input");
        var min = parseFloat($input.data("min") || 0);
        var max = parseFloat($input.data("max") || Infinity);
        var previousQty = parseFloat($input.val() || 0);
        var quantity = ($link.has(".fa-minus").length ? -0.1 : 0.1) + previousQty;
        var newQt = quantity > min ? (quantity < max ? quantity : max) : min;
        if (newQt !== previousQty) {
            var newQty = parseFloat(newQt.toFixed(1));
            $input.val(newQty).trigger('change');
        }
        return false;
    },

    _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
        $($dom_optional).toArray().forEach((elem) => {
            $(elem).find('.js_quantity').text(value);
            productIDs.push($(elem).find('span[data-product-id]').data('product-id'));
        });
        $input.data('update_change', true);

        rpc("/shop/cart/update_json", {
            product_id: parseInt($input.data('product-id'), 10),
            set_qty: parseFloat(value),
            line_id: line_id || false,
            display: true,
        }).then((data) => {
            $input.data('update_change', false);
            var check_value = parseFloat($input.val());
            if (isNaN(check_value)) {
                check_value = 1;
            }
            if (Math.abs(value - check_value) > 0.001) {
                $input.trigger('change');
                return;
            }
            if (!data.cart_quantity) {
                return window.location = '/shop/cart';
            }

            var displayQuantity = parseFloat(data.quantity);
            var formattedQuantity = displayQuantity % 1 === 0 ? displayQuantity.toString() : displayQuantity.toFixed(1);

            $input.val(displayQuantity);
            $('.js_quantity[data-line-id='+line_id+']').val(displayQuantity).text(formattedQuantity);

            if (data.cart_quantity) {
                var cartQty = parseFloat(data.cart_quantity);
                var formattedCartQty = cartQty % 1 === 0 ? cartQty.toString() : cartQty.toFixed(1);
                data.cart_quantity = formattedCartQty;
            }

            wSaleUtils.updateCartNavBar(data);
            wSaleUtils.showWarning(data.notification_info.warning);
            Component.env.bus.trigger('cart_amount_changed', [data.amount, data.minor_amount]);
        });
    },

    _onChangeCartQuantity: function (ev) {
        ev.preventDefault();
        var $input = $(ev.currentTarget);
        if ($input.data('update_change')) {
            return;
        }
        var value = parseFloat($input.val() || 0);
        if (isNaN(value)) {
            value = 1;
        }
        var $dom = $input.closest('tr');
        var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
        var line_id = parseInt($input.data('line-id'), 10);
        var productIDs = [parseInt($input.data('product-id'), 10)];
        this._changeCartQuantity($input, value, $dom_optional, line_id, productIDs);
    },
});