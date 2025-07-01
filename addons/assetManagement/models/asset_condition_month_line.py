
from odoo import models, fields, api

class AssetConditionMonthLine(models.Model):
    _name = 'x_asset.condition.month.line'
    _description = 'Detail Kondisi Bulanan Aset'
    _order = 'sequence, id'

    sequence = fields.Integer()
    month_id = fields.Many2one('x_asset.condition.month', string='Monthly Inspection', ondelete='cascade')
    asset_id = fields.Many2one('x_asset.item', string='Nama Barang', required=True)
    
    lokasi_nama = fields.Char(related='asset_id.location_id.name', string='Nama Lokasi', store=True)  # ← aman

    kondisi_baik = fields.Integer(string='Kondisi Baik')
    kondisi_rusak = fields.Integer(string='Kondisi Rusak')
    jumlah = fields.Integer(string='Jumlah', compute='_compute_jumlah', store=True)

    @api.depends('kondisi_baik', 'kondisi_rusak')
    def _compute_jumlah(self):
        for rec in self:
            rec.jumlah = (rec.kondisi_baik or 0) + (rec.kondisi_rusak or 0)
