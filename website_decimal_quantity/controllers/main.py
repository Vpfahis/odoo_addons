# -*- coding: utf-8 -*-
from odoo import fields
from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound
from odoo.tools.json import scriptsafe as json_scriptsafe
from odoo.addons.payment import utils as payment_utils
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleDecimal(WebsiteSale):
    @http.route()
    def cart(self, access_token=None, revive='', **post):
        order = request.website.sale_get_order()
        if order and order.carrier_id:
            order._remove_delivery_line()
        if order and order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order()

        if order:
            cart_qty = sum(order.mapped('website_order_line.product_uom_qty'))
            request.session['website_sale_cart_quantity'] = round(cart_qty, 1)

        values = {}
        if access_token:
            abandoned_order = request.env['sale.order'].sudo().search(
                [('access_token', '=', access_token)], limit=1)
            if not abandoned_order:  # wrong token (or SO has been deleted)
                raise NotFound()
            if abandoned_order.state != 'draft':  # abandoned cart already finished
                values.update({'abandoned_proceed': True})
            elif revive == 'squash' or (
                    revive == 'merge' and not request.session.get(
                'sale_order_id')):  # restore old cart or merge with unexistant
                request.session['sale_order_id'] = abandoned_order.id
                return request.redirect('/shop/cart')
            elif revive == 'merge':
                abandoned_order.order_line.write(
                    {'order_id': request.session['sale_order_id']})
                abandoned_order.action_cancel()
            elif abandoned_order.id != request.session.get(
                    'sale_order_id'):  # abandoned cart found, user have to choose what to do
                values.update({'access_token': abandoned_order.access_token})

        values.update({
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': [],
        })
        if order:
            order.order_line.filtered(
                lambda l: not l.product_id.active).unlink()
            values['suggested_products'] = order._cart_accessories()
            values.update(self._get_express_shop_payment_values(order))

        values.update(self._cart_values(**post))
        return request.render("website_sale.cart", values)

    @http.route()
    def cart_update(
            self, product_id, add_qty=1, set_qty=0,
            product_custom_attribute_values=None,
            no_variant_attribute_values=None,
            express=False, **kwargs
    ):
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        if product_custom_attribute_values:
            product_custom_attribute_values = json_scriptsafe.loads(
                product_custom_attribute_values)

        if no_variant_attribute_values:
            no_variant_attribute_values = json_scriptsafe.loads(
                no_variant_attribute_values)

        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=float(add_qty),
            set_qty=float(set_qty),
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
            **kwargs
        )

        cart_qty = sum(sale_order.mapped('website_order_line.product_uom_qty'))
        request.session['website_sale_cart_quantity'] = round(cart_qty, 1)

        if express:
            return request.redirect("/shop/checkout?express=1")
        return request.redirect("/shop/cart")

    @http.route()
    def cart_update_json(
            self, product_id, line_id=None, add_qty=None, set_qty=None,
            display=True,
            product_custom_attribute_values=None,
            no_variant_attribute_values=None, **kw
    ):
        """
        This route is called :
            - When changing quantity from the cart.
            - When adding a product from the wishlist.
            - When adding a product to cart on the same page (without redirection).
        """
        order = request.website.sale_get_order(force_create=True)
        if order.state != 'draft':
            request.website.sale_reset()
            if kw.get('force_create'):
                order = request.website.sale_get_order(force_create=True)
            else:
                return {}

        if product_custom_attribute_values:
            product_custom_attribute_values = json_scriptsafe.loads(
                product_custom_attribute_values)

        if no_variant_attribute_values:
            no_variant_attribute_values = json_scriptsafe.loads(
                no_variant_attribute_values)

        if add_qty is not None:
            add_qty = float(add_qty)
        if set_qty is not None:
            set_qty = float(set_qty)

        values = order._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
            **kw
        )

        values['notification_info'] = self._get_cart_notification_information(
            order, [values['line_id']])
        values['notification_info']['warning'] = values.pop('warning', '')

        cart_qty = sum(order.mapped('website_order_line.product_uom_qty'))
        session_cart_qty = round(cart_qty, 1)
        request.session['website_sale_cart_quantity'] = session_cart_qty

        if not order.cart_quantity:
            request.website.sale_reset()
            return values

        values['cart_quantity'] = session_cart_qty
        values['minor_amount'] = payment_utils.to_minor_currency_units(
            order.amount_total, order.currency_id
        ),
        values['amount'] = order.amount_total

        if not display:
            return values

        values['cart_ready'] = order._is_cart_ready()
        values['website_sale.cart_lines'] = request.env[
            'ir.ui.view']._render_template(
            "website_sale.cart_lines", {
                'website_sale_order': order,
                'date': fields.Date.today(),
                'suggested_products': order._cart_accessories()
            }
        )
        values['website_sale.total'] = request.env[
            'ir.ui.view']._render_template(
            "website_sale.total", {
                'website_sale_order': order,
            }
        )
        return values

    @http.route()
    def cart_quantity(self):
        if 'website_sale_cart_quantity' not in request.session:
            order = request.website.sale_get_order()
            if order:
                cart_qty = sum(order.mapped('website_order_line.product_uom_qty'))
                request.session['website_sale_cart_quantity'] = round(cart_qty, 1)
                return request.session['website_sale_cart_quantity']
            return 0
        return request.session['website_sale_cart_quantity']