from odoo import models, fields

class AssetWorkflow(models.Model):
    _name = 'asset.workflow'
    _description = 'Inspection Workflow'

    name = fields.Char(string='Workflow Name', required=True)
    description = fields.Text(string='Description')
    definition_ids = fields.One2many(
        'asset.workflow.definition', 'workflow_id', string='Workflow Steps'
    )
