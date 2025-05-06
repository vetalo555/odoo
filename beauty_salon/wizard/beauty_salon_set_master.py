from odoo import models, fields
from odoo.exceptions import UserError
from odoo.tools.translate import _

class ChangeMasterWizard(models.TransientModel):
    _name = 'change.master.wizard'
    _description = 'Change Master in Appointment'

    appointment_ids = fields.Many2many('beauty.appointment', string="Appointments", required=True)
    new_master_id = fields.Many2one('beauty.master', string="New Master", required=True)

    def apply_change(self):
        self.ensure_one()
        if self.appointment_ids.state != 'planning':
            raise UserError(_("You can't change Master in finished or cancelled appointments."))
        for appointment in self.appointment_ids:
            appointment.master_id = self.new_master_id
