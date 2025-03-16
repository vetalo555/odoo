from odoo import models, fields

class Disease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    disease = fields.Char(string='Disease')



