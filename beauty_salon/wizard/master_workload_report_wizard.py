from odoo import models, fields, api


class MasterWorkloadReportWizard(models.TransientModel):
    _name = 'master.workload.report.wizard'
    _description = 'Master Workload Report Wizard'

    date_from = fields.Date(string='Date From', required=True, default=fields.Date.context_today)
    date_to = fields.Date(string='Date To', required=True, default=fields.Date.context_today)
    master_ids = fields.Many2many('beauty.master', string='Masters')
    state = fields.Selection([
        ('planning', 'Planning'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='finished', required=True)

    @api.onchange('date_from')
    def _onchange_date_from(self):
        if self.date_from and self.date_to and self.date_from > self.date_to:
            self.date_to = self.date_from

    def action_generate_report(self):
        #Якщо майстри не вибрані, беремо всіх
        if not self.master_ids:
            self.master_ids = self.env['beauty.master'].search([])

        data = {
            'ids': self.master_ids.ids,
            'model': 'beauty.master',
            'form': {
                'date_from': self.date_from.strftime('%Y-%m-%d'),
                'date_to': self.date_to.strftime('%Y-%m-%d'),
                'master_ids': self.master_ids.ids,
                'state': self.state,
            }
        }
        return self.env.ref('beauty_salon.action_master_workload_report').report_action(
            docids=self.master_ids.ids,
            data=data
        )
