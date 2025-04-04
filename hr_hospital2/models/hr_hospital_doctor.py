from odoo import models, fields

class Doctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.person'
    _description = 'Doctor'

    specialty_id = fields.Many2one(
        'hr.hospital.speciality',
        string='Speciality'
    )
    intern = fields.Boolean(string='Intern')
    doctor_mentor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Doctor Mentor',
        domain="[('intern', '=', False)]"
    )
    interns_ids = fields.One2many(
        'hr.hospital.doctor',
        'doctor_mentor_id',
        string='Interns'
    )

    patients_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='doctor_id')

    def action_create_visit(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Visit',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_doctor_id': self.id},
        }
