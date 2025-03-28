from odoo import models, fields, api


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Wizard to generate disease report'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
        required=True,
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases',
        required=True,
    )
    date_from = fields.Date(string='From Date', required=True)
    date_to = fields.Date(string='To Date', required=True)


    # def action_generate_report(self, *args):
    #     print(args)
    #     print(self)
    #     print(self.doctor_ids, self.disease_ids, self.date_from, self.date_to)
    #     domain = []
    #
    #     if self.doctor_ids:
    #         domain.append(('doctor_id', 'in', self.doctor_ids.ids))
    #     if self.disease_ids:
    #         domain_disease.append(('disease_id', 'in', self.disease_ids.ids))
    #         diagnosis_list = [self.env['hr.hospital.diagnosis'].search(domain_disease)]
    #         print (type(diagnosis_list), 'TPI')
    #         domain.append(('diagnosis_ids', 'in', diagnosis_list))
    #         print(diagnosis_list, 'TTTT')
    #     if self.date_from:
    #         domain.append(('visit_finished_datetime', '>=', self.date_from))
    #     if self.date_to:
    #         domain.append(('visit_finished_datetime', '<=', self.date_to))
    #     diagnosis_records = self.env['hr.hospital.visit'].search(domain)
    #
    #     print(diagnosis_records)
    #     return diagnosis_records
    def generate_report(self):
        domain = []
        if self.doctor_ids:
            domain.append(('visits_id.doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))
        if self.date_from:
            domain.append(('visits_id.visit_finished_datetime', '>=', self.date_from))
        if self.date_to:
            domain.append(('visits_id.visit_finished_datetime', '<=', self.date_to))
        diagnosis_records = self.env['hr.hospital.diagnosis'].search(domain)
        print(diagnosis_records)
        return diagnosis_records