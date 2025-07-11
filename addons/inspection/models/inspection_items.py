from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class InspectionItem(models.Model):
    _name = 'inspection.item'
    _description = 'Inspection Item Detail'
    _order = 'sequence'

    inspection_id = fields.Many2one('inspection.record', string='Inspection Record', required=True, ondelete='cascade', index=True)
    sequence = fields.Integer(string='Sequence', default=10, help="Order of the inspection item.")

    task_master_id = fields.Many2one('task.master', string='Task', required=True, ondelete='restrict',
                                     help="The specific task being inspected.")
    
    location_id = fields.Many2one(related='task_master_id.location_id', string='Warehouse/Location', store=True, readonly=True)
    
    task_name = fields.Char(related='task_master_id.name', string='Task Name', readonly=True)
    task_description = fields.Text(related='task_master_id.description', string='Task Description', readonly=True)

    inspection_result = fields.Selection([
        ('baik', 'Baik'),
        ('cukup', 'Cukup'),
        ('kurang', 'Kurang'),
    ], string='Result', required=True, default='baik', help="Assessment result for this task.")

    score = fields.Integer(string='Score', compute='_compute_score', store=True, readonly=True)
    
    notes = fields.Text(string='Notes/Comments', help="Specific notes for this inspection item.")
    image = fields.Binary(string="Proof Image")
    image_filename = fields.Char(string="Image Filename")
    state = fields.Selection(related='inspection_id.state', string='Inspection State', readonly=True, store=True)
    
    @api.depends('inspection_result')
    def _compute_score(self):
        for record in self:
            if record.inspection_result == 'baik':
                record.score = 3
            elif record.inspection_result == 'cukup':
                record.score = 2
            elif record.inspection_result == 'kurang':
                record.score = 1
            else:
                record.score = 0
