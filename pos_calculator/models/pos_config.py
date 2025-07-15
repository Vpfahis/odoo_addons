from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_calculator = fields.Boolean(
        string='Enable Calculator',
        default=False,
        help='Enable calculator in POS screen'
    )