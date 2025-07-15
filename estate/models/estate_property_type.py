from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = 'Property Type'

    name = fields.Char(required=True)