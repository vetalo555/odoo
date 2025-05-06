from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

class BeautyAppointment(models.Model):
    """
        Represents a beauty salon appointment.
        Manages client bookings, master assignments, and service scheduling.
        """
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
    ], string='Status', required=True, tracking=True)
    # For appoinment history in client view
    service_ids = fields.Many2many('beauty.service', compute="_compute_services")


    @api.depends('line_ids.service_id')
    def _compute_services(self):
        """
                    Computes the list of services for this appointment.
                    This is used to display the appointment history in the client view.
                    """
        for record in self:
            record.service_ids = record.line_ids.mapped('service_id')

    @api.model
    def create(self, vals):
        """
                Creates a new appointment record.
                Automatically generates a unique reference number and creates reminders for planning appointments.

                :param vals: Dictionary of field values
                :return: Created appointment record
                """
        if not vals.get('name'):
            # Отримуємо наступний номер
            sequence = self.env['ir.sequence'].search([('code', '=', 'beauty.appointment')], limit=1)
            if not sequence:
                # Створюємо послідовність, якщо її немає
                sequence = self.env['ir.sequence'].create({
                    'name': 'Beauty Appointment Sequence',
                    'code': 'beauty.appointment',
                    'prefix': 'APT-',
                    'padding': 3,
                    'company_id': False
                })
            vals['name'] = sequence.next_by_id()

        appointment = super().create(vals)

        # Якщо створений запис має статус "planning", створюємо нагадування
        if appointment.state == 'planning' and appointment.line_ids:
            for line in appointment.line_ids:
                reminder = self.env['beauty.reminder'].create({
                    'client_id': appointment.client_id.id,
                    'service_id': line.service_id.id,
                    'next_date': appointment.appointment_date,
                    'note': f'Нагадування про запис на {appointment.name}',
                    'sent': False,
                    'appointment_id': appointment.id
                })
                # Оновлюємо існуючі нагадування для цього клієнта та послуги
                existing_reminders = self.env['beauty.reminder'].search([
                    ('client_id', '=', appointment.client_id.id),
                    ('service_id', '=', line.service_id.id),
                    ('id', '!=', reminder.id)
                ])
                existing_reminders.write({
                    'active': False,
                    'note': f'Замінено новим нагадуванням для {appointment.name}'
                })

        return appointment

    @api.onchange('state')
    def _deactivate_reminders(self):
        """Автоматично деактивує нагадування, якщо статус змінюється з 'planning'"""
        if self.state != 'planning':
            reminders = self.env['beauty.reminder'].search([('client_id', '=', self.client_id.id)])
            reminders.write({'active': False})  # Деактивація записів

    def unlink(self):
        """Видаляє відповідні записи в beauty.reminder, коли видаляється beauty.appointment"""
        for record in self:
            reminders = self.env['beauty.reminder'].search([
                ('appointment_id', '=', record.id),
                ('active', '=', True)
            ])
            if reminders:
                reminders.unlink()
        return super().unlink()

    def write(self, vals):
        """Перевірка, чи запис не має статусу 'finished' або 'cancelled'"""
        for rec in self:
            if rec.state in ['finished', 'cancelled']:
                # Дозволяємо змінювати тільки поле state, якщо запис вже має статус 'finished' або 'cancelled'
                if vals and (len(vals) > 1 or 'state' not in vals):
                    raise ValidationError(
                        _('Cannot modify an appointment that is marked as "Finished" or "Cancelled".'))

        # Якщо змінюється дата запису, оновлюємо пов'язані нагадування
        if 'appointment_date' in vals:
            for rec in self:
                reminders = self.env['beauty.reminder'].search([
                    ('appointment_id', '=', rec.id),
                    ('active', '=', True)
                ])
                reminders.write({
                    'next_date': vals['appointment_date']
                })

        return super().write(vals)

    @api.constrains('master_id', 'client_id', 'appointment_date')
    def _check_appointment_constraints(self):
        """
                Validates appointment constraints:
                - Checks if master is available
                - Prevents double booking of masters
                - Prevents double booking of clients
                """
        for rec in self:
            if not rec.master_id.is_available:
                raise ValidationError(_("Cannot assign an inactive master."))

            # Перевірка: той самий майстер уже має запис на цю дату і час
            duplicates = self.search([
                ('id', '!=', rec.id),
                ('master_id', '=', rec.master_id.id),
                ('appointment_date', '=', rec.appointment_date),
                ('state', '=', 'planning')
            ])
            if duplicates:
                raise ValidationError(_("This master already has an appointment at this date and time."))

            # Перевірка: клієнт уже записаний на той самий час
            client_conflicts = self.search([
                ('id', '!=', rec.id),
                ('client_id', '=', rec.client_id.id),
                ('appointment_date', '=', rec.appointment_date),
                ('state', '=', 'planning')
            ])
            if client_conflicts:
                raise ValidationError(_("This client already has an appointment at this date and time."))
