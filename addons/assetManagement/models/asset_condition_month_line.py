from odoo import models, fields

class AssetConditionMonthLine(models.Model):
    _name = 'x_asset.condition.month.line'
    _description = 'Detail Kondisi Bulanan Aset'

    condition_month_id = fields.Many2one('x_asset.condition.month', string='Parent')
    item_id = fields.Many2one('x_asset.item', string='Item Aset', required=True)
    jumlah = fields.Integer(string='Jumlah')
    month_id = fields.Many2one(
    'x_asset.condition.month',
    string='Form Induk',
    ondelete='cascade',
)
    lokasi_nama = fields.Char(
    string="Lokasi",
    related='item_id.location_id.name',
    store=True
)
    bulan_tahun = fields.Char(
    string='Bulan - Tahun',
    related='month_id.bulan_tahun',
    store=True
)
    asset_id = fields.Many2one(
    'x_asset.item',
    string='Aset',
    related='item_id',
    store=True,
    readonly=True,
)
    tanggal = fields.Date(
    string='Tanggal',
    related='month_id.tanggal',
    store=True
)
    kondisi_baik = fields.Integer(string='Kondisi Baik')
    kondisi_rusak = fields.Integer(string='Kondisi Rusak')
    keterangan = fields.Text(string='Keterangan')