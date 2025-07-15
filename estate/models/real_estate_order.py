from odoo import models, fields, api

class RealEstateOrder(models.Model):
    _name = 'real_estate_order'
    _description = 'Estate'

    name = fields.Char(required=True)
    description = fields.Text()
    property_type = fields.Many2one("estate_property_type", string='Property Type', required=True)
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(required=True)
    bedrooms = fields.Integer()
    living_area = fields.Float(string='Living area(sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float(string='Garden area(sqm)')
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[('north', 'North'), ('south', 'South'), ('west', 'West'),
                                                     ('east', 'East')], )
    state = fields.Selection(string = 'Status', selection=[('new', 'New'), ('offer', 'Offer Recieved'), ('sold','Sold'), ('cancelled', 'Cancelled')],)
    active = fields.Boolean(default = True)

    sales_man = fields.Many2one('res.users',default=lambda self: self.env.user, string="Salesman")
    buyer = fields.Many2one("res.partner", string="Buyer")

    total_area = fields.Float(compute="_compute_total")

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area



