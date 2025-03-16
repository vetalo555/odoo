from odoo import models, fields

class Visits(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Visit'

    doctor_id = fields.Many2one('hr.hospital.doctor', string='Doctor_id')
    patient_id = fields.Many2one('hr.hospital.patient', string='Patient_id')
    date = fields.Date(string='Date')
    disease_id = fields.Many2one(comodel_name = 'hr.hospital.disease', string='Disease_id')