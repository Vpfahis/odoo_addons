from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HostelFacility(models.Model):
    _name = 'hostel.facility'
    _description = 'Hostel facility'

    name = fields.Char(string='Name', required = True)
    charge = fields.Float(string='Charge', required = True)
    company_id = fields.Many2one('res.company', string='Company', default = lambda self:self.env.company, readonly=True)

    @api.constrains('charge')
    def _check_charge(self):
        for record in self:
            if record.charge <= 0:
                raise ValidationError("Charge must be greater than 0.")

