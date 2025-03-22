from odoo import models, fields

class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    visits_id = fields.Many2one(
        'hr.hospital.visit',
        string='Visits'
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Diseases'
    )
    subscribe = fields.Text(string='Subscribe')
    approved = fields.Boolean(string='Approved')

