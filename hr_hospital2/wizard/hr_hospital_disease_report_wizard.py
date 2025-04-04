from odoo import models, fields


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Wizard to generate disease report for a month'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases',
    )
    date_from = fields.Date(string='From Date', required=True)
    date_to = fields.Date(string='To Date', required=True)

    def generate_report(self):
        # Створюємо домен для фільтрації діагнозів
        domain = []

        # Якщо вибрані лікарі, додаємо фільтр по лікарях
        if self.doctor_ids:
            domain.append(('visits_id.doctor_id', 'in', self.doctor_ids.ids))

        # Якщо вибрані хвороби, додаємо фільтр по хворобах
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        # Додаємо фільтр по датах
        if self.date_from:
            domain.append(('create_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('create_date', '<=', self.date_to))

        # if self.date_from:
        #     domain.append(('visits_id.visit_finished_datetime', '>=', self.date_from))
        # if self.date_to:
        #     domain.append(('visits_id.visit_finished_datetime', '<=', self.date_to))


        return {
            'type': 'ir.actions.act_window',
            'name': 'Disease Report',
            'res_model': 'hr.hospital.diagnosis',
            'view_mode': 'tree,form',
            'domain': domain,
            'target': 'current',
        }
