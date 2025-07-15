from odoo import models, fields, api
import ast


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approved_by_user_ids = fields.Many2many('res.users', string="Approved By")
    show_approve_button = fields.Boolean(compute='_compute_approval')
    is_fully_approved = fields.Boolean(compute='_compute_approval')
    needs_approval = fields.Boolean(compute='_compute_approval')

    @api.model
    def create(self, vals):
        order = super().create(vals)
        config = self.env['ir.config_parameter'].sudo()
        enabled = config.get_param('spotter_sale_order_approval.enable_approval', 'False') == 'True'
        approvers = ast.literal_eval(config.get_param('spotter_sale_order_approval.approval_user_ids', '[]') or '[]')

        if enabled and order.amount_total >= 25000 and order.create_uid.id in approvers:
            order.approved_by_user_ids = [(4, order.create_uid.id)]

        return order

    def action_approve_order(self):
        if self.env.user not in self.approved_by_user_ids:
            self.approved_by_user_ids = [(4, self.env.user.id)]

    @api.depends('approved_by_user_ids', 'amount_total')
    def _compute_approval(self):
        config = self.env['ir.config_parameter'].sudo()
        enabled = config.get_param('spotter_sale_order_approval.enable_approval', 'False') == 'True'
        user_ids_str = config.get_param('spotter_sale_order_approval.approval_user_ids', '[]')
        try:
            approver_ids = ast.literal_eval(user_ids_str) if user_ids_str else []
        except (ValueError, SyntaxError):
            approver_ids = []

        for order in self:
            is_required = enabled and order.amount_total >= 25000
            approved_ids = order.approved_by_user_ids.ids

            order.is_fully_approved = (
                    not is_required or all(uid in approved_ids for uid in approver_ids)
            )

            order.show_approve_button = (
                    is_required and
                    self.env.user.id in approver_ids and
                    self.env.user.id not in approved_ids and
                    order.create_uid and self.env.user.id != order.create_uid.id
            )

            order.needs_approval = (
                    is_required and
                    not order.is_fully_approved
            )

    def action_confirm(self):
        for order in self:
            if not order.is_fully_approved:
                raise models.UserError("This order requires approval before it can be confirmed.")
        return super().action_confirm()

    def action_quotation_send(self):
        for order in self:
            if not order.is_fully_approved:
                raise models.UserError("This order requires approval before it can be send to customer.")
        return super().action_quotation_send()