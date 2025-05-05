# from odoo import models, fields, api
#
# class SetMasterWizard(models.TransientModel):
#     _name = 'set.master.wizard'
#     _description = 'Wizard to change masters in appointments'

    # master_ids = fields.Many2many(
    #     comodel_name='beauty.master',
    #     string='Masters',
    #     required=True
    # )
    # client_ids = fields.Many2many(
    #     comodel_name='beauty.client',
    #     string='Clients',
    #     required=True
    # )
    #
    # @api.model
    # def default_get(self, fields_list):
    #     res = super().default_get(fields_list)
    #     active_ids = self.env.context.get('active_ids', [])
    #     if 'client_ids' in fields_list and active_ids:
    #         res['client_ids'] = [(6, 0, active_ids)]
    #     return res
    #
    # def action_set_master(self):
    #     for client in self.client_ids:
    #         client.write({
    #             'master_ids': [(6, 0, self.master_ids.ids)]
    #         })
    #     return {'type': 'ir.actions.act_window_close'}

from odoo import models, fields, api
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