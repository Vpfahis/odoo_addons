from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    cod_charges = fields.Monetary(string='COD Charges', currency_field='currency_id', default=0.0)

    @api.depends('amount_untaxed', 'amount_tax', 'cod_charges')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = order.amount_untaxed + order.amount_tax + order.cod_charges

    def set_cod_charges(self, provider_id):
        cod_charges = 0.0
        if not provider_id:
            self.write({'cod_charges': cod_charges})
            return

        provider = self.env['payment.provider'].browse(provider_id)
        if provider.code == 'cash_on_delivery':
            for charge in provider.cod_charge_ids:
                if charge.min_total <= self.amount_untaxed <= charge.max_total:
                    cod_charges = charge.charge
                    break
        self.write({'cod_charges': cod_charges})
        _logger.info("Applied COD charges: %s on order %s (total: %s)", cod_charges, self.name, self.amount_untaxed)
