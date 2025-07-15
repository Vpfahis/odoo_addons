from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PaymentCODChargeCondition(models.Model):
    _name = 'payment.cod.charge.condition'
    _description = "COD Charge Condition"
    _order = 'min_amount'

    provider_id = fields.Many2one(
        'payment.provider',
        required=True,
        ondelete="cascade",
        domain=[('code', '=', 'cod')]
    )
    min_amount = fields.Float("Minimum Amount", required=True, default=0.0)
    max_amount = fields.Float("Maximum Amount", required=True)
    extra_charge = fields.Float("Extra Charge", required=True, default=0.0)

    @api.constrains('min_amount', 'max_amount')
    def _check_amount_range(self):
        for record in self:
            if record.min_amount >= record.max_amount:
                raise ValidationError("Minimum amount must be less than maximum amount.")

    @api.constrains('min_amount', 'max_amount', 'provider_id')
    def _check_overlapping_conditions(self):
        for record in self:
            overlapping = self.search([
                ('provider_id', '=', record.provider_id.id),
                ('id', '!=', record.id),
                '|',
                '&', ('min_amount', '<=', record.min_amount), ('max_amount', '>=', record.min_amount),
                '&', ('min_amount', '<=', record.max_amount), ('max_amount', '>=', record.max_amount)
            ])
            if overlapping:
                raise ValidationError("Amount ranges cannot overlap for the same provider.")
