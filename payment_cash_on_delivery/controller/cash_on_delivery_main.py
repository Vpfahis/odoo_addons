# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class CashOnDeliveryController(http.Controller):
    @http.route('/shop/payment/cod_charges', type='json', auth='public', website=True, csrf=False)
    def update_cod_charges(self, provider_id=None, payment_method_code=None):
        order = request.website.sale_get_order()
        if order and provider_id and payment_method_code == 'cash_on_delivery':
            order.set_cod_charges(int(provider_id))
            return {
                'cod_charges': order.cod_charges,
                'amount_total': order.amount_total,
                'currency_symbol': order.currency_id.symbol or '$'
            }
        if order:
            order.set_cod_charges(0)
        return {
            'cod_charges': 0.0,
            'amount_total': order.amount_total if order else 0.0,
            'currency_symbol': order.currency_id.symbol if order else '$'
        }

    @http.route('/payment/cash_on_delivery/verify_payment', type='json', auth='public')
    def cod_verify_payment(self, reference):
        """This function check the state and verify the state of cod"""
        payment = request.env['payment.transaction'].sudo().search(
            [('reference', '=', reference)], limit=1)
        if payment:
            print(payment.read())
            if payment.provider_code == 'cash_on_delivery' and payment.reference == reference:
                payment._set_done()
                # order = payment.sale_order_ids
                # if order and order.state == 'draft':
                #     order.action_confirm()

                print(payment.payment_method_id.read())
                return {'warning': f"Payment status: {payment.state}"}
        return {'error': f"No transaction found with reference: {reference}"}


