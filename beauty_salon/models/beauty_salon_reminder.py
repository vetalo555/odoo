from datetime import datetime
from odoo import models, fields, api


class BeautyReminder(models.Model):
    """
       Represents a service reminder for clients.
       Manages appointment reminders and notification system.
       """
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
    appointment_id = fields.Many2one('beauty.appointment', ondelete='cascade', string='Related Appointment')
    appointment_state = fields.Selection(related='appointment_id.state', store=True, string='Appointment Status')
    appointment_date = fields.Datetime(related='appointment_id.appointment_date', store=True, string='Appointment Date')
    master_id = fields.Many2one(related='appointment_id.master_id', store=True, string='Master')

    @api.depends('client_id', 'service_id', 'appointment_id')
    def _compute_name(self):
        """
                Computes the name/title for the reminder.
                Format: "Rem: [Client Name] - [Service Name] - [Appointment Reference]"
                """
        for record in self:
            if record.client_id and record.service_id:
                if record.appointment_id:
                    record.name = f"Rem: {record.client_id.name} - {record.service_id.name} - {record.appointment_id.name}"
                else:
                    record.name = f"Rem: {record.client_id.name} - {record.service_id.name}"
            else:
                record.name = "New Reminder"

    @api.model
    def _send_reminders(self):
        """Відправляє нагадування клієнтам"""
        # Отримуємо поточний час
        now = datetime.now()
        # Знаходимо нагадування, які потрібно відправити сьогодні
        reminders = self.search([
            ('next_date', '=', now.date()),
            ('sent', '=', False),
            ('active', '=', True),
            ('appointment_id.state', '=', 'planning')
        ])

        for reminder in reminders:
            # Формуємо повідомлення
            message = f"Доброго дня, {reminder.client_id.name}!Нагадуємо вам про запис в Beauty Salon"



            # Відправляємо повідомлення
            reminder.message_post(
                body=message,
                subject=f"Нагадування про запис",
                partner_ids=[reminder.client_id.id],
                message_type='email'
            )

            # Помічаємо нагадування як відправлене
            reminder.sent = True

    @api.model
    def _cron_send_reminders(self):
        """Періодичне виконання відправки нагадувань"""
        # Виконуємо відправку тільки в 9:00
        now = datetime.now()
        if now.hour == 9 and now.minute == 0:
            self._send_reminders()

    @api.model
    def create(self, vals):
        reminder = super().create(vals)
        # Якщо створюється нагадування без пов'язаного запису, намагаємось знайти його
        if not vals.get('appointment_id') and vals.get('client_id') and vals.get('service_id'):
            appointment = self.env['beauty.appointment'].search([
                ('client_id', '=', vals['client_id']),
                ('line_ids.service_id', '=', vals['service_id']),
                ('state', '=', 'planning')
            ], limit=1)
            if appointment:
                reminder.appointment_id = appointment.id
        return reminder

    def write(self, vals):
        res = super().write(vals)
        # Якщо змінюється клієнт або сервіс, оновлюємо пов'язаний запис
        if 'client_id' in vals or 'service_id' in vals:
            for record in self:
                appointment = self.env['beauty.appointment'].search([
                    ('client_id', '=', record.client_id.id),
                    ('line_ids.service_id', '=', record.service_id.id),
                    ('state', '=', 'planning')
                ], limit=1)
                if appointment:
                    record.appointment_id = appointment.id
                    # Оновлюємо дату та нотатку
                    record.next_date = appointment.appointment_date
                    record.note = f'Нагадування про запис на {appointment.name}'
        return res

    @api.onchange('appointment_id')
    def _onchange_appointment_id(self):
        for record in self:
            if record.appointment_id:
                # Оновлюємо сервіс з першої лінії запису
                service = record.appointment_id.line_ids[0].service_id if record.appointment_id.line_ids else False
                if service:
                    record.service_id = service.id
                record.next_date = record.appointment_id.appointment_date
                record.note = f'Нагадування про запис на {record.appointment_id.name}'
