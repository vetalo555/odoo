from odoo import models, fields

class BeautyService(models.Model):
    _name = 'beauty.service'
    _description = 'Beauty Service'

    name = fields.Char(string='Service name', required=True)
    list_price = fields.Float(string='List price', required=True)
    duration = fields.Float(string='Duration (hours)', required=True)