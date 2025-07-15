from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    student_id = fields.Many2one('hostel.student', string='Linked Student')
