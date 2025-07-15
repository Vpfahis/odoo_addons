from odoo import http
from odoo.http import request


class CODPaymentController(http.Controller):

    @http.route('/payment/cod/process', type='json', auth='public', methods=['POST'], csrf=False)
    def cod_process_payment(self, **kwargs):
        """Process COD payment"""
        try:
            provider_id = int(kwargs.get('provider_id'))
            amount = float(kwargs.get('amount'))
            currency_id = int(kwargs.get('currency_id'))
            reference = kwargs.get('reference')

            provider = request.env['payment.provider'].sudo().browse(provider_id)

            if provider.code != 'cod':
                return {'success': False, 'error': 'Invalid payment provider'}

            # Create payment transaction
            transaction_values = {
                'provider_id': provider_id,
                'reference': reference,
                'amount': amount,
                'currency_id': currency_id,
                'state': 'pending',
            }

            transaction = request.env['payment.transaction'].sudo().create(transaction_values)

            return {
                'success': True,
                'redirect_url': '/payment/status',
                'transaction_id': transaction.id
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    @http.route('/payment/cod/confirm/<int:transaction_id>', type='http', auth='user', methods=['POST'])
    def cod_confirm_payment(self, transaction_id, **kwargs):
        """Confirm COD payment (typically called by delivery personnel)"""
        transaction = request.env['payment.transaction'].browse(transaction_id)

        if transaction.provider_code == 'cod' and transaction.state == 'pending':
            transaction._cod_confirm_payment()

        return request.redirect('/my/orders')