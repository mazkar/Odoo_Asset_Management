from odoo import models, fields, api
from odoo.exceptions import UserError

class AssetItem(models.Model):
    _name = 'x_asset.item'
    _description = 'Item Aset'

    name = fields.Char(string='Nama Aset')
    onHandQuantity = fields.Integer(string='On Hand Quantity', default=0)
    note = fields.Char(string='Note', default='-')
    location_id = fields.Many2one('stock.location', string="Lokasi", domain="[('usage','=','internal')]")

    condition_month_ids = fields.One2many(
        'x_asset.condition.month.line', 
        'item_id',
        string='Kondisi Bulanan'
    )
        

    def action_custom_route(self):
        for record in self:
            raise UserError(f"Aksi dijalankan untuk aset: {record.name}")
