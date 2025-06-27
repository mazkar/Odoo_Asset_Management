from odoo import models, fields

class AssetWorkflowDefinition(models.Model):
    _name = 'asset.workflow.definition'
    _description = 'Inspection Workflow Definition'

    name = fields.Char(string='Step Name', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    workflow_id = fields.Many2one('asset.workflow', string='Workflow', required=True)
    group_id = fields.Many2one('res.groups', string='User Group', required=True)
