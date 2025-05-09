from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Visits(models.Model):
    """
    Represents a visit in the hospital. Stores information about doctor, patient,
    visit status, dates, and diagnosis. Includes validation logic.
    """
    _name = 'hr.hospital.visit'
    _description = 'Visit'
    description = fields.Text(string='Description')

    status = fields.Selection(selection=[
        ('planned', 'Planned'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled')],
        string='Status', required=True, default='planned'
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

    @api.constrains('visit_planned_datetime','doctor_id', 'visit_finished_datetime')
    def _check_visit_date(self):
        """
        Prevent modification of date/time or doctor for finished visits.
        """
        for record in self:
            if record.status == 'finished':
                raise ValidationError(_("You cannot modify the date/time or doctor of a completed visit."))

    @api.constrains('diagnosis_ids')
    def toggle_active(self):
        """
        Prevent modification of visit if there are diagnosis linked.
        """
        for record in self:
            if record.diagnosis_ids:
                raise ValidationError(_("You cannot modify the visit if there are diagnosis."))

    def unlink(self):
        """
        Prevent deletion of visits that have diagnosis linked.
        """
        for record in self:
            if record.diagnosis_ids:
                raise ValidationError(_("You cannot delete the visit if there are diagnosis."))
        return super(Visits, self).unlink()


    @api.constrains('doctor_id', 'patient_id', 'visit_planned_datetime')
    def _check_unique_appointment(self):
        """
        Ensure that a patient cannot have multiple appointments with the same doctor on the same day.
        """
        for record in self:
            if record.visit_planned_datetime:
                visit = [
                    ('id', '!=', record.id),
                    ('patient_id', '=', record.patient_id.id),
                    ('doctor_id', '=', record.doctor_id.id),
                    ('visit_planned_datetime', '>=', record.visit_planned_datetime.replace(hour=0, minute=0, second=0)),
                    ('visit_planned_datetime', '<', record.visit_planned_datetime.replace(hour=23, minute=59, second=59))
                ]
                if self.search_count(visit) > 0:
                    raise ValidationError(_("Patient already has an appointment with this doctor on this day!"))
