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
    create_date = fields.Datetime(string='Creation Date', readonly=True)

    disease_type_id = fields.Many2one(
        'hr.hospital.disease', string='Disease Type',
        related='disease_id.parent_id', store=True)

    diagnosis_count = fields.Integer(
        string="Diagnoses Count",
        default=1,
        readonly=True
    )
