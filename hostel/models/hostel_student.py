from datetime import date

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HostelStudent(models.Model):
    _name = 'hostel.student'
    _description = 'Student Info'
    _inherit = ['mail.thread','mail.activity.mixin']
    _sql_constraints = [
        ('student_id', 'UNIQUE (student_id)', 'You can not have two student with the same Student ID !')
    ]

    name = fields.Char(string='Name', required = True)
    student_id = fields.Char("Student ID", default=lambda self: _('New'),
       copy=False, readonly=True, tracking=True)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State',
                                             domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    dob = fields.Date(string='DOB')
    room = fields.Many2one('hostel.room', string='Room')
    email = fields.Char(string='Email')
    image = fields.Char(string='Photo')
    receive_mail = fields.Boolean(string='Receive Mail', default=True)
    age = fields.Integer(string='Age',compute="_compute_age")
    company_id = fields.Many2one('res.company', string='Company', default = lambda self:self.env.company, readonly=True)
    partner_id = fields.Many2one('res.partner', readonly=True,
                                 string='Partner', help='Partner-related data of the student')
    active = fields.Boolean(default = True)
    payment_state = fields.Selection([('pending','Pending'), ('done','Done')], string = 'Invoice state computed', compute='_compute_payment_state')
    payment_state_stored = fields.Selection(
        [('pending', 'Pending'), ('done', 'Done')],
        string='Invoice State',
        store=True,
        readonly=True,
    )
    monthly_amount = fields.Float(related = 'room.total_rent', string='Monthly Rent')
    user_id = fields.Many2one('res.users', string='User', readonly =True)
    invoice_ids = fields.One2many('account.move', 'student_id', string="Invoices")

    @api.model
    def create(self, vals):
        partner_vals = {
            'name': vals.get('name'),
            'email' : vals.get('email'),
            'street' : vals.get('street'),
            'street2': vals.get('street2'),
            'zip': vals.get('zip'),
            'city': vals.get('city'),
            'state_id': vals.get('state_id'),
            'country_id': vals.get('country_id'),
            'country_code': vals.get('country_code'),
        }
        partner = self.env['res.partner'].create(partner_vals)
        vals['partner_id'] = partner.id

        #sequence for student_id
        if vals.get('student_id', _('New')) == _('New'):
            vals['student_id'] = self.env['ir.sequence'].next_by_code('hostel.student')

        return super(HostelStudent, self).create(vals)

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            if rec.dob:
                today = date.today()
                birth_date = fields.Date.from_string(rec.dob)
                rec.age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                rec.age = 0

    def action_alot_room(self):
        if self.room:
            raise UserError('A room has already been allocated.')

        available_rooms = self.env['hostel.room'].search([
            ('state', 'in', ['empty', 'partial']),
            ('available_bed', '>', 0)
        ], limit=1)

        if available_rooms:
            room = available_rooms[0]
            self.room = room

            if room.available_bed == 1:
                room.state = 'full'
            else:
                room.state = 'partial'

            room.available_bed -= 1
        else:
            raise UserError('No available rooms to allocate.')

    def action_vacate_room(self):
        if not self.room:
            raise UserError('No room allocated to vacate')

        room = self.room
        room.available_bed += 1

        if room.available_bed == room.num_bed:
            room.state = 'empty'
        else:
            room.state = 'partial'

        self.room = False
        self.active = False

        if room.state == 'empty':
            self.env['hostel.cleaning.service'].create({'room_id': room.id})
            room.state = 'cleaning'

    invoice_count = fields.Integer(string="Invoice Count", compute='_compute_invoice_count')

    def _compute_invoice_count(self):
        for student in self:
            count = self.env['account.move'].search_count([
                ('student_id', '=', student.id),
                ('move_type', '=', 'out_invoice')
            ])
            student.invoice_count = count

    def action_view_student_invoices(self):
        return {
            'name': _('Invoices'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id), ('move_type', '=', 'out_invoice')],
            'context': {'create': False}
        }

    @api.depends('room')  # you might want to add dependencies on invoice changes as well
    def _compute_payment_state(self):
        for student in self:
            invoices = self.env['account.move'].search([
                ('student_id', '=', student.id),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
            ])
            if not invoices:
                val = False
            elif all(inv.payment_state == 'paid' for inv in invoices):
                val = 'done'
            else:
                val = 'pending'
            student.payment_state = val
            student.payment_state_stored = val

    def action_create_user(self):
        for rec in self:
            if not rec.email:
                raise UserError("Email is required to create a user.")

            user_vals = {
                'name': rec.name,
                'login': rec.email,
                'partner_id': rec.partner_id.id,
                'student_id': rec.id,
            }
            user = self.env['res.users'].create(user_vals)
            rec.user_id = user






