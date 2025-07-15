from odoo import fields, models
import razorpay

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('razorpay', "Razorpay")], ondelete={'razorpay': 'set default'})

    razorpay_key_id = fields.Char(string="Razorpay Key ID")
    razorpay_key_secret = fields.Char(string="Razorpay Secret Key")

    def _get_supported_payment_method_codes(self):
        return super()._get_supported_payment_method_codes() + ['razorpay']

    def _get_specific_rendering_values(self, processing_values):
        if self.code == 'razorpay':
            return self.razorpay_form_generate_values(processing_values)
        return super()._get_specific_rendering_values(processing_values)

    def razorpay_form_generate_values(self, values):
        self.ensure_one()
        client = razorpay.Client(auth=(self.razorpay_key_id, self.razorpay_key_secret))

        # resolve currency object from ID if needed
        currency = self.env['res.currency'].browse(values['currency_id'])

        amount_in_paise = int(values['amount'] * 100)
        order_data = {
            'amount': amount_in_paise,
            'currency': currency.name,
            'receipt': values['reference'],
            'payment_capture': 1
        }

        order = client.order.create(data=order_data)

        values.update({
            'razorpay_order_id': order['id'],
            'razorpay_key_id': self.razorpay_key_id,
            'amount': amount_in_paise,
        })
        return values
