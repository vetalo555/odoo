from odoo import models, fields

class Patients(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    name = fields.Char(string='Patient')
    doctor_id = fields.Many2one('hr.hospital.doctor', string='Doctor_id')