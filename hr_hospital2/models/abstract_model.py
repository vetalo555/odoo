from odoo import models, fields

class Person(models.AbstractModel):
    """
    Abstract base model for a person in the hospital module.
    Provides common fields for Doctor and Patient models.
    """
    _name = 'hr.hospital.person'
    _description = 'Abstract Person'

    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone number', translate=True)
    photo = fields.Image(
        string='Photo',
        max_width=512,
        max_height=512,
    )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')],
        string='Gender'
    )
