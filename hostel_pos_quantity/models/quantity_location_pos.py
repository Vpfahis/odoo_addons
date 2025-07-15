from ast import literal_eval
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    """Extension of 'res.config.settings' for configuring delivery settings."""
    _inherit = 'res.config.settings'

    quantity_location = fields.Boolean(
        string='Product Quantity in Location',
        help='This field is used to enable setting Category Discount in settings'
    )

    select_location_ids = fields.Many2many(
        'stock.location',
        'res_config_settings_pos_category_rel',
        'res_config_settings_id',
        'pos_category_id',
        domain="[('usage','=','internal')]",
        string='Category',
        help='Set the selected categories'
    )

    @api.model
    def get_values(self):
        """Get the values from settings."""

        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        quantity_location = icp_sudo.get_param('res.config.settings.quantity_location', default='False')
        select_location_ids = icp_sudo.get_param('res.config.settings.select_location_ids', default='[]')

        res.update(
            quantity_location=quantity_location == 'True',
            select_location_ids=[(6, 0, literal_eval(select_location_ids))] if select_location_ids else False,

        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.quantity_location', str(self.quantity_location)
        )
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.select_location_ids', str(self.select_location_ids.ids)
        )

        return res

class PosConfig(models.Model):
    _inherit = 'pos.config'

    quantity_location = fields.Boolean(
        string='Show Product Quantity',
        compute='_compute_quantity_location',
        help='Show product quantity badges in POS interface'
    )

    def _compute_quantity_location(self):
        quantity_location_param = self.env['ir.config_parameter'].sudo().get_param(
            'res.config.settings.quantity_location', default='False'
        )
        for config in self:
            config.quantity_location = quantity_location_param == 'True'