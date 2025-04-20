from datetime import date
from odoo import models, fields, api



class Patients(models.Model):
    """
    Represents a patient in the hospital. Inherits from Person and adds fields
    for doctor, birthday, passport, contact person, visits, diagnosis, and age.
    """
    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.person'
    _description = 'Patient'

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Personal Doctor'
    )
    user_id = fields.Many2one(
        'res.users',
        string='User',
        help='Odoo user associated with this patient',
        ondelete='set null',
    )
    birthday_date = fields.Date(string='Birthday')
    age = fields.Integer(compute='_compute_age', store=True)
    passport = fields.Char(string='Passport')
    contact_person = fields.Char(string='Contact Person')
    visits_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='patient_id',
        string='Visits'
    )

    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='visits_id',
        string='Diagnosis History',
        compute='_compute_diagnosis_ids',
        store=False
    )


    @api.depends('birthday_date')
    def _compute_age(self):
        """
        Compute the age of the patient based on their birthday.
        """
        today = date.today()
        for record in self:
            if record.birthday_date:
                age = today.year - record.birthday_date.year
                if (today.month, today.day) < (record.birthday_date.month, record.birthday_date.day):
                    age -= 1
                record.age = age
            else:
                record.age = 0

 # Метод для кнопки переходу до історії візитів
    def action_view_visits(self):
        """
        Open a window showing the visit history for this patient.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visit History',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    # Метод для створення швидкого запису
    def action_create_visit(self):
        """
        Open a form to create a new visit for this patient.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Visit',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_patient_id': self.id},
        }

    @api.depends('visits_ids.diagnosis_ids')
    def _compute_diagnosis_ids(self):
        """
        Compute all diagnosis linked to this patient through visits.
        """
        for patient in self:
            diagnosis_set = patient.visits_ids.mapped('diagnosis_ids')
            patient.diagnosis_ids = diagnosis_set
