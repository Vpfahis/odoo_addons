# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    cod_charges = fields.Float(string="COD Charges", default=0.0)

    def _compute_amounts(self):
        super()._compute_amounts()
        for order in self:
            order.amount_total += order.cod_charges

    def set_cod_charges(self, provider_id):
        cod_charges = 0.0
        if provider_id:
            provider = self.env['payment.provider'].browse(provider_id)
            if provider and provider.code == 'cash_on_delivery':
                order_amount = self.amount_total - self.cod_charges
                cod_charges = provider._compute_payment_provider_charges(order_amount)
        self.write({'cod_charges': cod_charges})
        self._compute_amounts()