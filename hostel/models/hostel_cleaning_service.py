from odoo import models, fields, api
from odoo.exceptions import UserError


class HostelCleaningService(models.Model):
    _name = 'hostel.cleaning.service'
    _description = 'Cleaning Service'
    _inherit = ['mail.thread']
    _rec_name = 'room_id'

    room_id = fields.Many2one('hostel.room',string='Room',required=True)
    start_time = fields.Float(string='Start Time')
    cleaning_staff = fields.Many2one('res.users',string='Cleaning Staff',readonly=True)
    state = fields.Selection([('new','New'),('assigned','Assigned'),('done','Done')],default='new',tracking=True)
    company_id = fields.Many2one('res.company',string='Company',default = lambda self:self.env.company, readonly=True)
    previous_room_state = fields.Selection([('empty', 'Empty'),('partial', 'Partial'),('full', 'Full'),('cleaning', 'Cleaning')], string="Previous Room State", readonly=True)

    @api.model
    def create(self, vals):
        room = self.env['hostel.room'].browse(vals.get('room_id'))
        if room:
            vals['previous_room_state'] = room.state
            room.state = 'cleaning'
        return super().create(vals)

    def action_cleaning_assign(self):
        for record in self:
            if record.cleaning_staff:
                raise UserError('Already assigned to %s' % record.cleaning_staff.name)
            record.cleaning_staff = self.env.user
            record.state = 'assigned'

    def action_cleaning_complete(self):
        for record in self:
            record.state = 'done'
            if record.room_id and record.previous_room_state:
                record.room_id.state = record.previous_room_state
