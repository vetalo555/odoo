from odoo import models, fields, api


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Wizard to generate disease report'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
        required=False,
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases',
        required=False,
    )
    date_from = fields.Date(string='From Date', required=True)
    date_to = fields.Date(string='To Date', required=True)

    @api.model
    def action_generate_report(self):
        domain = []
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        elif self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))
        elif self.date_from:
            domain.append(('date', '>=', self.date_from))
        elif self.date_to:
            domain.append(('date', '<=', self.date_to))
        diagnosis_records = self.env['hr.hospital.diagnosis'].search(domain)
        return diagnosis_records