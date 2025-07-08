
from odoo import models, fields

class ApprovalRouteLine(models.Model):
    _name = 'approval.route.line'
    _description = 'Approval Route Line'

    name = fields.Char(string="Name", required=True)
    group_id = fields.Many2one('res.groups', string="User Group", required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    
