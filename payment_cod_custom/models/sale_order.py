from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    cod_extra_charge = fields.Float(
        "COD Extra Charge",
        compute="_compute_cod_extra_charge",
        store=True,
        help="Extra charge for Cash on Delivery payment"
    )

    @api.depends('amount_untaxed')
    def _compute_cod_extra_charge(self):
        for order in self:
            if order.payment_provider_id and order.payment_provider_id.code == 'cod':
                order.cod_extra_charge = order.payment_provider_id._cod_get_extra_charge(order.amount_untaxed)
            else:
                order.cod_extra_charge = 0.0

    @api.depends('order_line.price_total', 'cod_extra_charge')
    def _amount_all(self):
        """Override to include COD extra charge in total"""
        super()._amount_all()
        for order in self:
            if order.cod_extra_charge:
                order.amount_total += order.cod_extra_charge

    def _prepare_invoice(self):
        """Include COD charge in invoice"""
        invoice_vals = super()._prepare_invoice()
        if self.cod_extra_charge:
            # Add COD charge as an invoice line
            cod_line = {
                'name': 'COD Extra Charge',
                'quantity': 1,
                'price_unit': self.cod_extra_charge,
                'account_id': self.env.ref('account.account_account_template_current_liabilities').id,
            }
            if 'invoice_line_ids' not in invoice_vals:
                invoice_vals['invoice_line_ids'] = []
            invoice_vals['invoice_line_ids'].append((0, 0, cod_line))
        return invoice_vals
