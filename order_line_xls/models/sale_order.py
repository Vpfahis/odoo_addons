from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_open_import_wizard(self):
        return {
            'name': 'Import Order Lines',
            'type': 'ir.actions.act_window',
            'res_model': 'import.sale.order.line.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }
