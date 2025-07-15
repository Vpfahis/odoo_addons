import razorpay
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class RazorpayController(http.Controller):

    @http.route(['/payment/razorpay/verify'], type='http', auth='public', csrf=False, methods=['POST'])
    def razorpay_verify(self, **post):
        provider = request.env['payment.provider'].sudo().search([('code', '=', 'razorpay')], limit=1)
        client = razorpay.Client(auth=(provider.razorpay_key_id, provider.razorpay_key_secret))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': post.get('razorpay_order_id'),
                'razorpay_payment_id': post.get('razorpay_payment_id'),
                'razorpay_signature': post.get('razorpay_signature'),
            })
        except Exception as e:
            _logger.error("Signature verification failed: %s", e)
            return request.redirect('/shop/payment')

        tx = request.env['payment.transaction'].sudo().search([
            ('reference', '=', post.get('razorpay_order_id'))
        ], limit=1)

        if tx:
            tx._set_done()
            tx._post_process_after_done()
            return request.redirect('/shop/confirmation')
        else:
            _logger.error("Transaction not found.")
            return request.redirect('/shop/payment')
