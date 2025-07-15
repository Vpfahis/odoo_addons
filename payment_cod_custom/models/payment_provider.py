from odoo import fields, models, api


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('cod', "Cash on Delivery")],
        ondelete={'cod': 'set default'}
    )

    cod_charge_condition_ids = fields.One2many(
        'payment.cod.charge.condition',
        'provider_id',
        string="COD Charge Conditions"
    )

    def _cod_get_extra_charge(self, amount_total):
        """Calculate extra charge based on order amount"""
        self.ensure_one()
        if self.code != 'cod':
            return 0.0

        for condition in self.cod_charge_condition_ids.sorted('min_amount'):
            if condition.min_amount <= amount_total <= condition.max_amount:
                return condition.extra_charge
        return 0.0

    @api.model
    def _get_compatible_providers(self, company_id, partner_id, amount, currency_id=None, **kwargs):
        """Override to ensure COD provider is available"""
        providers = super()._get_compatible_providers(
            company_id, partner_id, amount, currency_id, **kwargs
        )
        return providers