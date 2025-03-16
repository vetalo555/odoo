from odoo import models, fields

class Doctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Doctor')
    specialty = fields.Char(string='Speciality')


