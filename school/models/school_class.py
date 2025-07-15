from odoo import models, fields

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'Class'

    name = fields.Char(string='Class Name', required=True)
    class_teacher = fields.Many2one("school.faculty",string='Class Teacher', required=True)
