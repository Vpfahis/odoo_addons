from odoo import models,fields, api, _
from odoo.exceptions import UserError


class HostelRoom(models.Model):
    _name = 'hostel.room'
    _description = 'Hostel Room'
    _inherit = ['mail.thread']
    _sql_constraints = [
        ('number', 'UNIQUE (number)', 'You can not have two room with the same name !')
    ]
    _rec_name = 'number'

    number = fields.Char("Room Number", default=lambda self: _('New'),
                         copy=False, readonly=True, tracking=True)
    room_type = fields.Selection(string='Room Type', selection=[('ac', 'AC'), ('non_ac', 'Non AC'),])
    num_bed = fields.Integer(string='Number of Bed', required = True)
    available_bed = fields.Integer(related="num_bed", string="Available Beds",store=True)
    rent = fields.Float(string='Rent', required = True)
    state = fields.Selection([('empty','Empty'),('partial','Partial'),('full','Full'),('cleaning','Cleaning')],default='empty',tracking=True)
    company_id = fields.Many2one('res.company',string='Company',default = lambda self:self.env.company, readonly=True)
    currency_id = fields.Many2one('res.currency',string='Currency',related = "company_id.currency_id", store= True )
    student_ids = fields.One2many('hostel.student','room',string='Students',ondelete='restrict')
    facility_ids = fields.Many2many('hostel.facility',string='Facilities')
    total_rent = fields.Float(string='Total Rent',readonly=True,compute="_compute_rent")
    pending_amount = fields.Float(string='Pending Amount',readonly = True, compute = '_compute_pending_amount')
    image = fields.Char(string='Photo')
    description = fields.Text(string='Description')

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the student model """
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = (self.env['ir.sequence'].
                                  next_by_code('hostel.room'))
        return super().create(vals_list)

    def _compute_rent(self):
        for rec in self:
            rec.total_rent = rec.rent + sum(rec.facility_ids.mapped('charge'))

    def action_monthly_invoice(self):
        product = self.env['product.product'].search([('name', '=', 'Hostel Room Rent')], limit=1)
        if not product:
            raise UserError("Product 'Hostel Room Rent' not found. Please create it first.")

        invoices = []
        for student in self.student_ids:
            if not student.partner_id:
                raise UserError(f"Student {student.name} has no related partner.")
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': student.partner_id.id,
                'student_id': student.id,
                'invoice_line_ids': [(0, 0, {
                    'product_id': product.id,
                    'quantity': 1,
                    'price_unit': self.total_rent,
                })],
            }
            invoice = self.env['account.move'].create(invoice_vals)
            invoice.action_post()
            invoices.append(invoice.id)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', invoices)],
        }

    def action_monthly_auto_invoice(self):
            rooms = self.search([])
            for room in rooms:
                room.action_monthly_invoice()

    def _compute_pending_amount(self):
        for room in self:
            pending = 0.0
            for student in room.student_ids:
                if student.partner_id:
                    invoices = self.env['account.move'].search([
                        ('move_type', '=', 'out_invoice'),
                        ('partner_id', '=', student.partner_id.id),
                        ('state', '=', 'posted'),
                        ('payment_state', '!=', 'paid')
                    ])
                    pending += sum(invoices.mapped('amount_residual'))
            room.pending_amount = pending
