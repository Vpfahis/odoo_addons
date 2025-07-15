# -*- coding: utf-8 -*-
from odoo import fields, models, api


class PaymentProviderCharges(models.Model):
    _name = 'payment.provider.charges'
    _description = 'Payment Provider Charges'
    _order = 'min_amount'

    provider_id = fields.Many2one('payment.provider', string='Payment Provider', required=True, ondelete='cascade')
    min_amount = fields.Float(string='Minimum Amount', required=True, help='Minimum order amount for this charge')
    max_amount = fields.Float(string='Maximum Amount',
                              help='Maximum order amount for this charge (leave empty for no limit)')
    charge_amount = fields.Float(string='Charge Amount', required=True, help='Fixed fee applied for this amount range')

    @api.constrains('min_amount', 'max_amount')
    def _check_amounts(self):
        for record in self:
            if record.max_amount and record.min_amount > record.max_amount:
                raise models.ValidationError('Minimum amount cannot be greater than maximum amount')


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('cash_on_delivery', 'Cash on Delivery')],
                            ondelete={'cash_on_delivery': 'set default'})
    payment_provider_charges = fields.Float(string='Extra Charge',
                                            help='Fixed fee applied to transactions for this provider.')
    provider_charges_ids = fields.One2many('payment.provider.charges', 'provider_id', string='Conditional Charges')

    def _compute_payment_provider_charges(self, amount, currency=None, country=None):
        """Compute the custom fee for the transaction based on amount ranges."""
        if self.code == 'cash_on_delivery' and self.provider_charges_ids:
            for charge in self.provider_charges_ids.sorted('min_amount'):
                if amount >= charge.min_amount:
                    if not charge.max_amount or amount <= charge.max_amount:
                        return charge.charge_amount
            return 0.0
        return self.payment_provider_charges if self.payment_provider_charges else 0.0