from odoo import models, fields


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('c_o_d', 'COD')],
                            ondelete={'c_o_d': 'set default'})

    cod_charge_ids = fields.One2many(
        'cod.charge.rule', 'provider_id', string="COD Charges by Range"
    )


class CODChargeRule(models.Model):
    _name = 'cod.charge.rule'
    _description = 'COD Charge Based on Order Total'

    provider_id = fields.Many2one('payment.provider', required=True, ondelete='cascade')
    min_total = fields.Float(string='Min Order Total', required=True)
    max_total = fields.Float(string='Max Order Total', required=True)
    charge = fields.Monetary(string='COD Charge', required=True)
    currency_id = fields.Many2one('res.currency', required=True, default=lambda self: self.env.company.currency_id)
