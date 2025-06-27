from odoo import models, fields, api
from odoo.exceptions import UserError

class AssetItem(models.Model):
    _name = 'x_asset.item'
    _description = 'Item Aset'

    name = fields.Char(string='Nama Aset')
    onHandQuantity = fields.Integer(string='On Hand Quantity', default=0)
    note = fields.Char(string='Note',default='-')
    condition_month_ids = fields.One2many(
        'x_asset.condition.month',
        'item_id',
        string='Kondisi Bulanan'
    )

    def action_custom_route(self):
        for record in self:
            # Misalnya kita hanya ingin tampilkan pesan
            raise UserError(f"Aksi dijalankan untuk aset: {record.name}")
