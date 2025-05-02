from odoo import api, fields, models

class BeautyAppointmentLine(models.Model):
    _name = 'beauty.appointment.line'
    _description = 'Appointment Line'

    appointment_id = fields.Many2one('beauty.appointment', string='Appointment', required=True, ondelete='cascade')
    service_id = fields.Many2one('beauty.service', string='Service', required=True)
    price = fields.Float(string='Price', related='service_id.list_price', store=True)
    duration = fields.Float(string='Duration', related='service_id.duration', store=True)
    qty = fields.Integer(string='Quantity', default=1)
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    @api.depends('price', 'qty')
    def _compute_total_price(self):
        for line in self:
            line.total_price = line.price * line.qty
