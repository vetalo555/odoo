from odoo.tests import common

class TestBeautyService(common.TransactionCase):
    def setUp(self):
        super(TestBeautyService, self).setUp()
        self.service_model = self.env['beauty.service']

    def test_create_service(self):
        """Тест створення нової послуги"""
        service = self.service_model.create({
            'name': 'Test Service',
            'list_price': 100.0,
            'duration': 1.0,
        })
        self.assertEqual(service.name, 'Test Service')
        self.assertEqual(service.list_price, 100.0)
        self.assertEqual(service.duration, 1.0)
