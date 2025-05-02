from odoo import models, fields


class Master(models.Model):
    _name = 'beauty.master'
    _description = 'Beauty Salon Master'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', string="Related Partner", required=True, ondelete='cascade')
    specialization = fields.Selection([
        ('hairdresser', 'Hairdresser'),
        ('manicure ', 'Manicure '),
        ('pedicure ', 'Pedicure '),
        ('beautician ', 'Beautician '),
        ('masseur ', 'Masseur '),
    ], string='Specialization', tracking=True
    )
    is_available = fields.Boolean(string="Available", default=True, tracking=True)