from odoo import models, fields

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Students'

    name = fields.Char(string='Name', required=True)
    student_address = fields.Text(string='Address', required=True)
    parent_name = fields.Char(string='Parent Name')
    parent_phone =  fields.Char(string='Parent Phone', required=True)
    class_id = fields.Many2one("school.class", string='Class')
    class_teacher = fields.Many2one("school.faculty", string='Class Teacher', related="class_id.class_teacher", store=True)
    subject = fields.Many2many("school.subject",string='Subjects')