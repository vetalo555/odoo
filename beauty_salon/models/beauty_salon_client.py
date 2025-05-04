from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Client(models.Model):
    _name = 'beauty.client'
    _description = 'Beauty Salon Client'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', string="Related Partner", required=True, ondelete='cascade')
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    discount = fields.Float(string='Discount (%)',compute='_compute_discount', default=0.0)
    visit_count = fields.Integer(string='Total Visits', compute='_compute_visit_count', store=True)
    appointment_ids = fields.One2many('beauty.appointment', 'client_id')
    appointment_history_ids = fields.One2many(
        'beauty.appointment',
        'client_id',
        string='Appointment History',
        readonly = True
    )
    master_ids = fields.Many2many(
        comodel_name='beauty.master',
        string='Personal Masters',
        relation='beauty_client_master_rel',
        column1='client_id',
        column2='master_id',
    )

    @api.depends('appointment_ids.state')
    def _compute_visit_count(self):
        for client in self:
            client.visit_count = self.env['beauty.appointment'].search_count([
                ('client_id', '=', client.id),
                ('state', '=', 'finished')
            ])
    @api.depends('visit_count')
    def _compute_discount(self):
        for client in self:
            if client.visit_count >= 10:
                client.discount = 10.0
            elif client.visit_count >= 5:
                client.discount = 5.0
            else:
                client.discount = 0.0

    def action_create_appointment(self):
        """
        Open a form to create a new appointment for this client.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Appointment',
            'res_model': 'beauty.appointment',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_client_id': self.id},
        }