# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request, route
from odoo.addons.website_sale.controllers.product_configurator import WebsiteSaleProductConfiguratorController


class WebsiteSaleDecimal(WebsiteSaleProductConfiguratorController):

    @route()
    def website_sale_product_configurator_update_cart(
            self, main_product, optional_products, **kwargs):

        order_sudo = request.website.sale_get_order(force_create=True)
        if order_sudo.state != 'draft':
            request.session['sale_order_id'] = None
            order_sudo = request.website.sale_get_order(force_create=True)
        values = order_sudo._cart_update(
            product_id=main_product['product_id'],
            add_qty=float(main_product['quantity']),
            product_custom_attribute_values=main_product['product_custom_attribute_values'],
            no_variant_attribute_value_ids=[
                int(value_id) for value_id in main_product['no_variant_attribute_value_ids']
            ],
            **kwargs,
        )
        line_ids = {main_product['product_template_id']: values['line_id']}

        if optional_products and values['line_id']:
            for option in optional_products:
                option_values = order_sudo._cart_update(
                    product_id=option['product_id'],
                    add_qty=float(option['quantity']),
                    product_custom_attribute_values=option['product_custom_attribute_values'],
                    no_variant_attribute_value_ids=[
                        int(value_id) for value_id in option['no_variant_attribute_value_ids']
                    ],
                    linked_line_id=line_ids[option['parent_product_template_id']],
                    **kwargs,
                )
                line_ids[option['product_template_id']] = option_values['line_id']

        values['notification_info'] = self._get_cart_notification_information(
            order_sudo, line_ids.values()
        )

        cart_qty = sum(order_sudo.mapped('website_order_line.product_uom_qty'))
        values['cart_quantity'] = round(cart_qty, 1)
        request.session['website_sale_cart_quantity'] = round(cart_qty, 1)

        return values