from odoo import models, fields

class Person(models.AbstractModel):
    _name = 'hr.hospital.person'
    _description = 'Abstract Person'

    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone number')
    photo = fields.Image(
        max_width=512,
        max_height=512,
    )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')],
        string='Gender'
    )
