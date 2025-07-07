from odoo import models, fields, api

class TaskInspection(models.Model):
    _name = 'task.inspection'
    _description = 'Task Daily Inspection'

    name = fields.Char(string='Inspection Name', required=True)
    date = fields.Date(string='Inspection Date', default=fields.Date.context_today, required=True)
    inspector_id = fields.Many2one('res.users', string='Inspector', default=lambda self: self.env.user)
    task_item_ids = fields.One2many('task.inspection.item', 'inspection_id', string='Inspection Items')
    notes = fields.Text(string='Notes')

class TaskInspectionItem(models.Model):
    _name = 'task.inspection.item'
    _description = 'Task Inspection Item'

    inspection_id = fields.Many2one('task.inspection', string='Inspection', required=True, ondelete='cascade')
    task_item_id = fields.Many2one('task.item', string='Task Item', required=True)
    status = fields.Selection([
        ('ok', 'OK'),
        ('not_ok', 'Not OK'),
        ('n/a', 'N/A')
    ], string='Status', required=True)
    remarks = fields.Char(string='Remarks')