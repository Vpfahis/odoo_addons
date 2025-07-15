from odoo import fields,models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    quality_level = fields.Integer("Quality Level")