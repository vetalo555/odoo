from odoo import models, fields


class Client(models.Model):
    _name = 'beauty.client'
    _description = 'Beauty Salon Client'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', string="Related Partner", required=True, ondelete='cascade')
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    loyalty_points = fields.Integer(string="Loyalty Points", default=0, tracking=True)
    client_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        required=True,
        tracking=True,
    )
