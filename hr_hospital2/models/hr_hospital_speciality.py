from odoo import models, fields

class Speciality(models.Model):
    _name = 'hr.hospital.speciality'
    _description = 'Speciality'

    name = fields.Char()
