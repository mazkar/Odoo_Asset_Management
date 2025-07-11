from odoo import fields, models, api

class TaskMaster(models.Model):
    _name = "task.master"
    _description = "Task Master"

    name = fields.Char(string="Task Name", required=True)
    description = fields.Text(string="Task Description")
    location_id = fields.Many2one('stock.warehouse', string='Default Warehouse/Location',
                                  help="The default warehouse or location where this task is typically performed. "
                                       "This will be pre-filled in inspection items.")
 
    sequence = fields.Integer(string="Sequence", help="Used to order tasks")   
    active = fields.Boolean(string="Active", default=True)
 