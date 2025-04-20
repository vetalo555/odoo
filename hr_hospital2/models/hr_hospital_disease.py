from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Disease(models.Model):
    """
    Represents a disease in the hospital. Supports hierarchical structure and
    provides methods for computing full names and validation.
    """
    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text(string='Description')
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease', string='Parent Disease',
        index=True, ondelete='cascade')
    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease', inverse_name='parent_id',
        string='Sub Diseases')
    complete_name = fields.Char(
        string='Complete Name', compute='_compute_complete_name',
        recursive=True, store=True, translate=True)
    parent_path = fields.Char(index=True, unaccent=False, translate=True)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        """
        Compute the complete (hierarchical) name of the disease.
        """
        for record in self:
            if record.parent_id:
                record.complete_name = '%s / %s' % (
                    record.parent_id.complete_name, record.name)
            else:
                record.complete_name = record.name

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        """
        Ensure that no recursive disease categories are created.
        """
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))

    @api.model
    def name_create(self, name):
        """
        Create a new disease record with the given name.
        """
        record = self.create({'name': name})
        return record.id, record.display_name

    @api.depends_context('hierarchical_naming')
    def _compute_display_name(self):
        """
        Compute the display name for the disease, optionally using hierarchical naming.
        """
        if self.env.context.get('hierarchical_naming', True):
            return super()._compute_display_name()
        for record in self:
            record.display_name = record.name
