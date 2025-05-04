from odoo import models, fields, api

class BeautyReminder(models.Model):
    _name = 'beauty.reminder'
    _description = 'Service Reminder'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', compute='_compute_name', store=True)
    client_id = fields.Many2one('beauty.client', string='Client', required=True)
    service_id = fields.Many2one('beauty.service', string='Service', required=True)
    next_date = fields.Date(string='Next Appointment Date', required=True)
    note = fields.Text(string='Note')
    sent = fields.Boolean(string='Reminder Sent', default=False)
    active = fields.Boolean(default=True, string='Active', tracking=True)
    appointment_id = fields.Many2one('beauty.appointment', ondelete='cascade')

    @api.depends('client_id', 'service_id')
    def _compute_name(self):
        for record in self:
            if record.client_id and record.service_id:
                record.name = f"Rem: {record.client_id.name} - {record.service_id.name}"
            else:
                record.name = "New Reminder"
