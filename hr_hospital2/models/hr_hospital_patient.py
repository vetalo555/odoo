from datetime import date
from odoo import models, fields, api



class Patients(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.person'
    _description = 'Patient'

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Personal Doctor'
    )
    birthday_date = fields.Date(string='Birthday')
    age = fields.Integer(compute='_compute_age', store=True)
    passport = fields.Char(string='Passport')
    contact_person = fields.Char(string='Contact Person')

    @api.depends('birthday_date')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birthday_date:
                age = today.year - record.birthday_date.year
                if (today.month, today.day) < (record.birthday_date.month, record.birthday_date.day):
                    age -= 1
                record.age = age
            else:
                record.age = 0
