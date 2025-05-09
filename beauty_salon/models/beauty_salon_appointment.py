from odoo import models, fields, api

class BeautyAppointment(models.Model):
    _name = 'beauty.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    appointment_date = fields.Datetime(string='Appointment Date', required=True, tracking=True)
    client_id = fields.Many2one('beauty.client', string='Client', required=True, tracking=True)
    master_id = fields.Many2one('beauty.master', string='Master', required=True, tracking=True)
    line_ids = fields.One2many('beauty.appointment.line', 'appointment_id', string='Services')
    state = fields.Selection([
        ('planning', 'Planning'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled')
    ], string='Status', tracking=True)

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', 'New') == 'New':
    #         vals['name'] = self.env['ir.sequence'].next_by_code('beauty.appointment') or 'New'
    #     return super().create(vals)
    # @api.model
    # def create(self, vals):
    #     # Перевіряємо, чи поле name ще не задано
    #     if not vals.get('name'):
    #         # Отримуємо наступне значення з послідовності
    #         vals['name'] = self.env['ir.sequence'].next_by_code('beauty.appointment') or 'New'
    #     return super(BeautyAppointment, self).create(vals)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('beauty.appointment') or 'New'
        appointment = super().create(vals)

        # Якщо створений запис має статус "planning", створюємо нагадування
        if appointment.state == 'planning' and appointment.line_ids:
            for line in appointment.line_ids:
                self.env['beauty.reminder'].create({
                    'client_id': appointment.client_id.id,
                    'service_id': line.service_id.id,
                    'next_date': appointment.appointment_date,
                    'note': 'Автоматичне нагадування про заплановану послугу.',
                    'sent': False,
                })

        return appointment