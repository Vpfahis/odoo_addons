from ast import literal_eval
from odoo import fields, api, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    quantity_available = fields.Float("Quantity location", compute='_compute_location_quantities')
    qty_per_location_tooltip = fields.Char("Qty Per Location Tooltip", compute='_compute_location_quantities')


    def _compute_location_quantities(self):
        config = self.env['ir.config_parameter'].sudo()
        show_qty = config.get_param('res.config.settings.quantity_location', default='False') == 'True'
        location_ids_str = config.get_param('res.config.settings.select_location_ids', default='[]')
        location_ids = literal_eval(location_ids_str)
        location_map = {loc.id: loc.display_name for loc in self.env['stock.location'].browse(location_ids)}

        for product in self:
            if not show_qty or not location_ids:
                product.quantity_available = 0.0
                product.qty_per_location_tooltip = ""
                continue

            quants = self.env['stock.quant'].search([
                ('product_id', '=', product.id),
                ('location_id', 'in', location_ids),
            ])

            total_qty = 0.0
            tooltip_lines = []
            for loc_id in location_ids:
                loc_quants = quants.filtered(lambda q: q.location_id.id == loc_id)
                available_qty = sum(loc_quants.mapped('available_quantity'))
                tooltip_lines.append(f"{location_map.get(loc_id, 'Unknown')}: {int(available_qty)}")
                total_qty += available_qty

            product.quantity_available = total_qty
            product.qty_per_location_tooltip = '\n'.join(tooltip_lines)

    @api.model
    def _load_pos_data_fields(self, config_id):
        """This function will add the fields to the function"""
        result = super()._load_pos_data_fields(config_id)
        result += ['quantity_available', 'qty_per_location_tooltip']
        return result