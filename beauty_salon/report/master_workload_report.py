from datetime import datetime, timedelta
from odoo import models, fields



class MasterWorkloadReport(models.AbstractModel):
    _name = 'report.beauty_salon.master_workload_report'
    _description = 'Master Workload Report'

    def _get_appointments_data(self, master, date_from, date_to, state):
        appointments = self.env['beauty.appointment'].search([
            ('master_id', '=', master.id),
            ('appointment_date', '>=', date_from),
            ('appointment_date', '<=', date_to),
            ('state', '=', state)
        ])

        # Групуємо записи по датах
        result = {}
        for app in appointments:
            date_str = app.appointment_date.strftime('%Y-%m-%d')
            if date_str not in result:
                result[date_str] = {'count': 0, 'hours': 0.0}
            result[date_str]['count'] += 1
            # Сумуємо тривалість всіх послуг в записі (тривалість вже в годинах)
            result[date_str]['hours'] += sum(line.duration for line in app.line_ids)
        return result

    def _get_report_values(self, docids, data=None):
        if not data:
            return {}

        # Отримуємо параметри з data або з docids
        if data and data.get('form'):
            date_from = datetime.strptime(data['form']['date_from'], '%Y-%m-%d').date()
            date_to = datetime.strptime(data['form']['date_to'], '%Y-%m-%d').date()
            state = data['form']['state']
            master_ids = data['form'].get('master_ids', [])
        else:
            # Якщо дані не передані через візард, використовуємо значення за замовчуванням
            date_from = fields.Date.today()
            date_to = fields.Date.today()
            state = 'finished'
            master_ids = docids if docids else []

        # Отримуємо майстрів
        if master_ids:
            masters = self.env['beauty.master'].browse(master_ids)
        else:
            masters = self.env['beauty.master'].search([])

        # Підготовка даних для звіту
        masters_data = []
        for master in masters:
            appointments_data = self._get_appointments_data(master, date_from, date_to, state)

            # Створюємо список дат для відображення
            dates_data = []
            current_date = date_from
            while current_date <= date_to:
                date_str = current_date.strftime('%Y-%m-%d')
                date_data = appointments_data.get(date_str, {'count': 0, 'hours': 0.0})
                dates_data.append({
                    'date': current_date.strftime('%d/%m/%Y'),
                    'count': date_data['count'],
                    'hours': round(date_data['hours'], 1)
                })
                current_date += timedelta(days=1)

            masters_data.append({
                'master': master,
                'dates': dates_data,
                'total_count': sum(d['count'] for d in dates_data),
                'total_hours': round(sum(d['hours'] for d in dates_data), 1)
            })

        return {
            'doc_ids': docids,
            'doc_model': 'beauty.master',
            'docs': masters_data,
            'date_from': date_from.strftime('%d/%m/%Y'),
            'date_to': date_to.strftime('%d/%m/%Y'),
            'company': self.env.company,
            'datetime': datetime,
        }
