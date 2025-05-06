from odoo.tests import common
from odoo.exceptions import ValidationError

class TestBeautyAppointment(common.TransactionCase):
    def setUp(self):
        super(TestBeautyAppointment, self).setUp()
        self.appointment_model = self.env['beauty.appointment']
        self.master_model = self.env['beauty.master']
        self.client_model = self.env['beauty.client']

    def test_appointment_creation(self):
        """Тест створення нового запису"""
        master = self.master_model.create({
            'partner_id': self.env['res.partner'].create({'name': 'Master'}).id,
            'specialization': 'hairdresser',
        })
        client = self.client_model.create({
            'partner_id': self.env['res.partner'].create({'name': 'Client'}).id,
            'date_of_birth': '1990-01-01',
        })
        appointment = self.appointment_model.create({
            'master_id': master.id,
            'client_id': client.id,
            'appointment_date': '2025-05-05 10:00:00',
            'state': 'planning',
        })
        self.assertEqual(appointment.name, 'New')
        self.assertEqual(appointment.state, 'planning')

    def test_appointment_state_change(self):
        """Тест зміни статусу запису"""
        master = self.master_model.create({
            'partner_id': self.env['res.partner'].create({'name': 'Master'}).id,
            'specialization': 'hairdresser',
        })
        client = self.client_model.create({
            'partner_id': self.env['res.partner'].create({'name': 'Client'}).id,
            'date_of_birth': '1990-01-01',
        })
        appointment = self.appointment_model.create({
            'master_id': master.id,
            'client_id': client.id,
            'appointment_date': '2025-05-05 10:00:00',
            'state': 'planning',
        })
        appointment.state = 'finished'
        self.assertEqual(appointment.state, 'finished')

    def test_appointment_constraints(self):
        """Тест перевірки обмежень при створенні запису"""
        master = self.master_model.create({
            'partner_id': self.env['res.partner'].create({'name': 'Master'}).id,
            'specialization': 'hairdresser',
            'is_available': False,
        })
        client = self.client_model.create({
            'partner_id': self.env['res.partner'].create({'name': 'Client'}).id,
            'date_of_birth': '1990-01-01',
        })
        with self.assertRaises(ValidationError):
            self.appointment_model.create({
                'master_id': master.id,
                'client_id': client.id,
                'appointment_date': '2025-05-05 10:00:00',
                'state': 'planning',
            })