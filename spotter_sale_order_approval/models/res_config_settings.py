from odoo import models, fields, api
import ast


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_approval = fields.Boolean(
        string="Enable Sale Order Approval",
        config_parameter="spotter_sale_order_approval.enable_approval"
    )

    approval_user_ids = fields.Many2many(
        'res.users',
        string="Approver(s) ",
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        config = self.env['ir.config_parameter'].sudo()
        user_ids_str = config.get_param('spotter_sale_order_approval.approval_user_ids', '[]')

        try:
            user_ids = ast.literal_eval(user_ids_str) if user_ids_str else []
        except (ValueError, SyntaxError):
            user_ids = []

        res.update({
            'approval_user_ids': [(6, 0, user_ids)],
        })
        return res

    def set_values(self):
        super().set_values()
        config = self.env['ir.config_parameter'].sudo()
        user_ids = self.approval_user_ids.ids
        config.set_param('spotter_sale_order_approval.approval_user_ids', str(user_ids))