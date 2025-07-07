from odoo import models, fields, api

class CleaningTaskMaster(models.Model):
    _name = 'cleaning.task.master'
    _description = 'Cleaning Task Master'

    name = fields.Char(string='Task Name', required=True)
    code = fields.Char(string='Task Code', required=True, copy=False, index=True)
    description = fields.Text(string='Description')
    is_active = fields.Boolean(string='Active', default=True)
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('other', 'Other')
    ], string='Frequency', default='daily')
    notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Task Code must be unique!')
    ]