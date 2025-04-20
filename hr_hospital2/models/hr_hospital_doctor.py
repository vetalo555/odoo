from odoo import models, fields

class Doctor(models.Model):
    """
    Represents a doctor in the hospital. Inherits from Person and adds fields
    for speciality, mentor, interns, patients, and visits.
    """
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.person'
    _description = 'Doctor'

    specialty_id = fields.Many2one(
        'hr.hospital.speciality',
        string='Speciality'
    )
    user_id = fields.Many2one(
        'res.users',
        string='User',
        help='Odoo user associated with this patient',
        ondelete='set null',
    )
    intern = fields.Boolean(string='Intern')
    doctor_mentor_id = fields.Many2one('hr.hospital.doctor', string='Doctor Mentor', domain="[('intern', '=', False)]")
    interns_ids = fields.One2many('hr.hospital.doctor', 'doctor_mentor_id', string='Interns')
    patients_ids = fields.One2many('hr.hospital.patient', 'doctor_id', string='Patients')
    visits_ids = fields.One2many('hr.hospital.visit', 'doctor_id', string='Visits')

    def action_create_visit(self):
        """
        Open a form to create a new visit for this doctor.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Visit',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_doctor_id': self.id},
        }
