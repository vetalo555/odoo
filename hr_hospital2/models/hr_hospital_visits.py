from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Visits(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Visit'

    status = fields.Selection(selection=[
        ('planned', 'Planned'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled')],
        string='Status'
    )
    visit_planned_datetime = fields.Datetime(string='Visit Planned Date')
    visit_finished_datetime = fields.Datetime(string='Visit Finished Date')

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Doctor'
    )
    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string='Patient'
    )

    diagnosis_ids = fields.One2many(
        comodel_name = 'hr.hospital.diagnosis',
        inverse_name = 'visits_id',
        string='Diagnosis'
    )

    @api.constrains('visit_planed_datetime','doctor_id', 'visit_finished_datetime')
    def _check_visit_date(self):
        for record in self:
            if record.status == 'finished':
                raise ValidationError("You cannot modify the date/time or doctor of a completed visit.")


