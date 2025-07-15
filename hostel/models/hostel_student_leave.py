from odoo import models, fields



class HostelStudentField(models.Model):
    _name = 'hostel.student.leave'
    _description = 'Student Leave'
    _inherit = ['mail.thread']
    _rec_name = 'student_id'

    student_id =fields.Many2one('hostel.student',string='Student',required=True,ondelete='cascade')
    leave_date = fields.Date(string='Leave Date',required = True)
    arrival_date = fields.Date(string='Arrival Date')
    state = fields.Selection([('new','New'),('approved','Approved')],default='new',tracking=True)
    company_id = fields.Many2one('res.company', string='Company', default = lambda self:self.env.company, readonly=True)


    def approve(self):
        for leave in self:
            leave.state = 'approved'
            room = leave.student_id.room
            if not room:
                continue

            all_on_leave = all(
                self.env['hostel.student.leave'].search_count([
                    ('student_id', '=', student.id),
                    ('state', '=', 'approved'),
                    ('leave_date', '<=', leave.leave_date),
                    ('arrival_date', '>=', leave.leave_date)
                ]) > 0
                for student in room.student_ids
            )

            if all_on_leave:
                existing = self.env['hostel.cleaning.service'].search([
                    ('room_id', '=', room.id),
                    ('state', 'in', ['new', 'assigned'])
                ], limit=1)
                if not existing:
                    self.env['hostel.cleaning.service'].create({'room_id': room.id})
                    room.state = 'cleaning'

