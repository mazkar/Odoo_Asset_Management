from odoo import models, fields, api
from odoo.exceptions import UserError

class PressenceItem(models.Model):
    _name = 'x_pressence.task'
    _description = 'Pressence Task'

    name = fields.Char(string='Task Description', required=True)
 