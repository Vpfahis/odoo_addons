from odoo import models, fields, api

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """Override to handle COD specific rendering"""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code == 'cod':
            res.update({
                'cod_extra_charge': processing_values.get('cod_extra_charge', 0.0),
            })
        return res

    def _process_notification_data(self, notification_data):
        """Process COD payment notification"""
        super()._process_notification_data(notification_data)
        if self.provider_code == 'cod':
            # COD payments are confirmed upon delivery
            self._set_pending()

    def _cod_confirm_payment(self):
        """Confirm COD payment (to be called when delivery is confirmed)"""
        self.ensure_one()
        if self.provider_code == 'cod' and self.state == 'pending':
            self._set_done()