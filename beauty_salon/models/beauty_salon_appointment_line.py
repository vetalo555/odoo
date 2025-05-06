from odoo import api, fields, models

class BeautyAppointmentLine(models.Model):
    _name = 'beauty.appointment.line'
    _description = 'Appointment Line'

    appointment_id = fields.Many2one('beauty.appointment', string='Appointment', required=True, ondelete='cascade')
    service_id = fields.Many2one('beauty.service', string='Service', required=True)
    price = fields.Float(string='Price', related='service_id.list_price', store=True)
    duration = fields.Float(string='Duration', related='service_id.duration', store=True)
    qty = fields.Integer(string='Quantity', default=1)
    discount = fields.Float(string='Discount (%)', compute='_compute_discount', store=True)
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)
    appointment_state = fields.Selection(related='appointment_id.state', store=True)
    #Client bonuses
    client_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        domain="[('is_company', '=', False)]",
        related='appointment_id.client_id.partner_id',
        store=True,
    )

    #Filters and group by date in view
    date_filter = fields.Selection(
        selection=lambda self: [(str(d), str(d)) for d in self._get_dates()],
        string="Filter by Day",
        compute="_compute_date_filter",
        store=True
    )

    #Filters and group by date in view
    @api.model
    def _get_dates(self):
        dates = self.env['beauty.appointment'].search([]).mapped('appointment_date')
        return sorted(set(d.date() for d in dates if d))

    #Filters and group by date in view
    @api.depends('appointment_id.appointment_date')
    def _compute_date_filter(self):
        for record in self:
            record.date_filter = str(record.appointment_id.appointment_date.date()) if record.appointment_id else False

    @api.depends('appointment_id.client_id', 'appointment_id.state')
    def _compute_discount(self):
        for line in self:
            client = line.appointment_id.client_id
            appointment = line.appointment_id

            if not client or not appointment or not appointment.id:
                line.discount = 0.0
                continue

            # Рахуємо завершені візити, виключаючи поточний
            past_appointments = self.env['beauty.appointment'].search([
                ('client_id', '=', client.id),
                ('state', '=', 'finished'),
                ('id', '!=', appointment.id),
            ])
            visits = len(past_appointments)

            if visits < 4:
                line.discount = 0.0
            else:
                line.discount = min((visits // 5) * 5.0, 10.0)

    @api.depends('price', 'qty', 'discount')
    def _compute_total_price(self):
        for line in self:
            discount_multiplier = (100 - line.discount) / 100
            line.total_price = line.price * line.qty * discount_multiplier

