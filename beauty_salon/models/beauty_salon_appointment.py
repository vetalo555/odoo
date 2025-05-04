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
    ], string='Status', required=True, tracking=True)
    service_ids = fields.Many2many('beauty.service', compute="_compute_services")

    @api.depends('line_ids.service_id')
    def _compute_services(self):
        for record in self:
            record.service_ids = record.line_ids.mapped('service_id')

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

    @api.onchange('state')
    def _deactivate_reminders(self):
        """Автоматично деактивує нагадування, якщо статус змінюється з 'planning'"""
        if self.state != 'planning':
            reminders = self.env['beauty.reminder'].search([('client_id', '=', self.client_id.id)])
            reminders.write({'active': False})  # Деактивація записів

    # def write(self, vals):
    #     """Оновлює дані в beauty.reminder при зміні запису в beauty.appointment, включаючи line_ids"""
    #     result = super().write(vals)
    #
    #     for record in self:
    #         reminders = self.env['beauty.reminder'].search([('client_id', '=', record.client_id.id)])
    #
    #         # Якщо змінено `line_ids`, оновлюємо нагадування
    #         if 'line_ids' in vals:
    #             new_services = record.line_ids.mapped('service_id.id')
    #
    #             # Видалення нагадувань, якщо послуги більше не існують
    #             reminders_to_delete = reminders.filtered(lambda r: r.service_id.id not in new_services)
    #             if reminders_to_delete:
    #                 reminders_to_delete.unlink()
    #
    #             # Додавання нових нагадувань
    #             existing_services = reminders.mapped('service_id.id')
    #             for line in record.line_ids:
    #                 if line.service_id.id not in existing_services:
    #                     self.env['beauty.reminder'].create({
    #                         'client_id': record.client_id.id,
    #                         'service_id': line.service_id.id,
    #                         'next_date': record.appointment_date,
    #                         'note': 'Автоматичне нагадування про оновлену послугу.',
    #                         'sent': False,
    #                     })
    #
    #         # Оновлення існуючих нагадувань, якщо змінено загальні дані
    #         if reminders:
    #             update_vals = {}
    #             for field in vals:
    #                 if field in reminders._fields:
    #                     update_vals[field] = vals[field]
    #
    #             if update_vals:
    #                 reminders.write(update_vals)
    #
    #     return result

    def unlink(self):
        """Видаляє відповідні записи в beauty.reminder, коли видаляється beauty.appointment"""
        for record in self:
            reminders = self.env['beauty.reminder'].search([('client_id', '=', record.client_id.id)])
            if reminders:
                reminders.unlink()  # Видалення пов'язаних нагадувань
        return super().unlink()

    # def write(self, vals):
    #     res = super().write(vals)
    #     if 'state' in vals and vals['state'] == 'finished':
    #         for appointment in self:
    #             appointment.client_id._compute_visit_count()
    #             appointment.client_id._compute_discount()
    #     return res
