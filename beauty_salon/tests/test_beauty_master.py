from odoo.tests import common
from odoo.exceptions import ValidationError


class TestBeautyMaster(common.TransactionCase):
    def setUp(self):
        super(TestBeautyMaster, self).setUp()
        self.master_model = self.env['beauty.master']
        self.partner_model = self.env['res.partner']

    def test_create_master(self):
        """Тест створення нового майстра"""
        partner = self.partner_model.create({
            'name': 'Test Master',
            'email': 'test@master.com',
        })
        master = self.master_model.create({
            'partner_id': partner.id,
            'specialization': 'hairdresser',
            'is_available': True,
        })
        self.assertEqual(master.name, 'Test Master')
        self.assertEqual(master.specialization, 'hairdresser')

    def test_master_unavailable(self):
        """Тест переведення майстра в стан недоступності"""
        master = self.master_model.create({
            'partner_id': self.partner_model.create({'name': 'Test'}).id,
            'specialization': 'hairdresser',
            'is_available': True,
        })
        master.is_available = False
        self.assertFalse(master.is_available)

    def test_master_specialization_required(self):
        """Тест перевірки обов'язковості спеціалізації"""
        with self.assertRaises(ValidationError):
            self.master_model.create({
                'partner_id': self.partner_model.create({'name': 'Test'}).id,
                'specialization': False,
                'is_available': True,
            })
