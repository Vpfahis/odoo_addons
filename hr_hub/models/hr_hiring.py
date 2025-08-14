# -*- coding: utf-8 -*-
from odoo import fields, models, api
import ast


class HrHiring(models.Model):
    _name = 'hr.hiring'
    _description = 'New Hiring'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char('Name', required=True, )
    email = fields.Char('Personal Email', required=True, )
    phone = fields.Char('Personal Number', required=True, )
    country_id = fields.Many2one('res.country', string='Nationality', required=True, )
    department_id = fields.Many2one('hr.department', string='Department', required=True, )
    job_id = fields.Many2one('hr.job', string='Job Position', required=True, )
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    wage = fields.Monetary('Wage', required=True, )
    housing_allowance = fields.Monetary('Housing Allowance', required=True, )
    transportation_allowance = fields.Monetary('Transportations Allowance', required=True)
    other_allowances = fields.Monetary('Other Allowance', required=True)
    state = fields.Selection(
        [('draft', 'New'), ('hr_review', 'HR Review'),
         ('done', 'Approved')], string='Status', default='draft', required=True, )
    check_readonly = fields.Boolean('Check Readonly', compute='_compute_check_readonly')



    @api.depends('state')
    def _compute_check_readonly(self):
        for rec in self:
           rec.check_readonly = rec.state != 'draft'


    def action_review(self):
        self.state = 'hr_review'
        config = self.env['ir.config_parameter'].sudo()
        user_ids_str = config.get_param('hr_hub.hr_hiring_reviewer_ids', '[]')

        try:
            user_ids = ast.literal_eval(user_ids_str) if user_ids_str else []
        except (ValueError, SyntaxError):
            user_ids = []

        for user_id in user_ids:
            self.activity_schedule(
                'mail.mail_activity_data_todo',  # or a custom one if needed
                user_id=user_id,
                note='Please review the hiring application: %s' % self.name,
                summary='Review Hiring Application',
            )

    def action_review_approve(self):
        self.state = 'done'
        config = self.env['ir.config_parameter'].sudo()
        user_ids_str = config.get_param('hr_hub.hr_hiring_reviewer_ids', '[]')

        try:
            user_ids = ast.literal_eval(user_ids_str) if user_ids_str else []
        except (ValueError, SyntaxError):
            user_ids = []

        if self.env.uid not in user_ids:
            raise self.env.user._user_error("You are not authorized to approve this review.")

            # Search for this user's activity only
        activity = self.env['mail.activity'].search([
            ('res_model', '=', 'hr.hiring'),
            ('res_id', '=', self.id),
            ('user_id', '=', self.env.uid),
            ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id),
        ], limit=1)

        if activity:
            activity.action_feedback(feedback="Reviewed and approved by %s." % self.env.user.name)



