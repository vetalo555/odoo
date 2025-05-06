from odoo.tests import common

class TestBeautyClient(common.TransactionCase):
    def setUp(self):
        super(TestBeautyClient, self).setUp()
        self.client_model = self.env['beauty.client']
        self.partner_model = self.env['res.partner']

    def test_create_client(self):
        """Тест створення нового клієнта"""
        partner = self.partner_model.create({
            'name': 'Test Client',
            'email': 'test@client.com',
        })
        client = self.client_model.create({
            'partner_id': partner.id,
            'date_of_birth': '1990-01-01',
        })
        self.assertEqual(client.name, 'Test Client')
        self.assertEqual(client.date_of_birth, '1990-01-01')

