from odoo import models, fields

class Doctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.person'
    _description = 'Doctor'

    specialty_id = fields.Many2one('hr.hospital.speciality', string='Speciality')
    intern = fields.Boolean(string='Intern')
    doctor_mentor_id = fields.Many2one('hr.hospital.doctor', string='Doctor Mentor', domain="[('intern', '=', False)]")





