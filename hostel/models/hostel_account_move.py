from odoo import models, fields,_
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    student_id = fields.Many2one('hostel.student', string='Student')

    def action_post(self):
        res = super().action_post()
        template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
        if not template:
            raise UserError("Invoice email template not found.")

        for invoice in self:
            student = invoice.student_id
            if (
                    invoice.move_type == 'out_invoice' and
                    student and student.email and student.receive_mail
            ):
                template.send_mail(
                    invoice.id,
                    force_send=True,
                    email_values={'email_to': student.email}
                )

        return res
