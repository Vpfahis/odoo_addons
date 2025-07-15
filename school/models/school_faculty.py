from odoo import models, fields

class SchoolFaculty(models.Model):
    _name = 'school.faculty'
    _description = 'Faculty'

    name = fields.Char(string='Name', required=True)
    faculty_address = fields.Char(string='Address')
    faculty_phone = fields.Char(string='Phone', required=True)
