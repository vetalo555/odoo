from odoo import models, fields

class BeautyReminder(models.Model):
    _name = 'beauty.reminder'
    _description = 'Service Reminder'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    client_id = fields.Many2one('beauty.client', string='Client', required=True)
    service_id = fields.Many2one('beauty.service', string='Service', required=True)
    next_date = fields.Date(string='Next Appointment Date', required=True)
    note = fields.Text(string='Note')
    sent = fields.Boolean(string='Reminder Sent', default=False)