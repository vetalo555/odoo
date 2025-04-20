# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestHospitalModels(TransactionCase):
    """
    Test suite for the main models of the hr_hospital2 module.
    Covers Doctor, Patient, and Disease models.
    """

    def setUp(self):
        """
        Set up test data: create a doctor, a patient linked to the doctor, and a disease.
        """
        super().setUp()
        # Create a doctor
        self.doctor = self.env['hr.hospital.doctor'].create({
            'name': 'Test Doctor',
            'speciality': 'Cardiology',
            'intern': False,
        })
        # Create a patient
        self.patient = self.env['hr.hospital.patient'].create({
            'name': 'Test Patient',
            'birthday_date': '1990-01-01',
            'personal_doctor_id': self.doctor.id,
        })
        # Create a disease
        self.disease = self.env['hr.hospital.disease'].create({
            'name': 'Test Disease',
        })

    def test_doctor_speciality(self):
        """
        Ensure that the doctor's speciality is set correctly upon creation.
        """
        self.assertEqual(self.doctor.speciality, 'Cardiology')

    def test_patient_doctor_relation(self):
        """
        Ensure that the patient is correctly linked to their personal doctor.
        """
        self.assertEqual(self.patient.personal_doctor_id, self.doctor)

    def test_disease_name(self):
        """
        Ensure that the disease name is stored and retrieved correctly.
        """
        self.assertEqual(self.disease.name, 'Test Disease')
