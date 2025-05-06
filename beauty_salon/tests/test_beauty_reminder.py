from odoo.tests import common

class TestBeautyReminder(common.TransactionCase):
    def setUp(self):
        super(TestBeautyReminder, self).setUp()
        self.reminder_model = self.env['beauty.reminder']
        self.client_model = self.env['beauty.client']
        self.service_model = self.env['beauty.service']

    def test_create_reminder(self):
        """Тест створення нагадування"""
        client = self.client_model.create({
            'partner_id': self.env['res.partner'].create({'name': 'Client'}).id,
            'date_of_birth': '1990-01-01',
        })
        service = self.service_model.create({
            'name': 'Test Service',
            'list_price': 100.0,
            'duration': 1.0,
        })
        reminder = self.reminder_model.create({
            'client_id': client.id,
            'service_id': service.id,
        })
