from odoo import models


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _create_transaction(self, amount, provider_id, **kwargs):
        provider = self.env['payment.provider'].browse(provider_id)
        currency = self.currency_id
        country = self.partner_id.country_id
        fee = 0.0
        if provider.code == 'cash_on_delivery':
            for charge in provider.cod_charge_ids:
                if charge.min_total <= amount <= charge.max_total:
                    fee = charge.charge
                    break
        amount_with_fee = amount + fee
        return super()._create_transaction(amount=amount_with_fee, provider_id=provider_id, **kwargs)
