from odoo import models, fields, api

class AssetConditionMonthLine(models.Model):
    _name = 'x_asset.condition.month.line'
    _description = 'Detail Kondisi Bulanan Aset'

    condition_month_id = fields.Many2one('x_asset.condition.month', string='Parent')
    item_id = fields.Many2one('x_asset.item', string='Item Aset', required=True)
    jumlah = fields.Integer(
        string='On Hand Quantity',
        compute='_compute_on_hand_qty',
        store=True,
        readonly=True
    )
    total_display = fields.Char(
        string='Total',
        compute='_compute_total_display',
        store=False
    )

    note = fields.Char(string='Note')
    @api.depends('item_id.onHandQuantity')
    def _compute_on_hand_qty(self):
        for rec in self:
            rec.jumlah = rec.item_id.onHandQuantity if rec.item_id else 0


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
    total = fields.Integer(
        string='Jumlah',
        compute='_compute_jumlah',
        store=True,
        readonly=True
    )

    @api.depends('kondisi_baik', 'kondisi_rusak')
    def _compute_jumlah(self):
        for rec in self:
            rec.total = (rec.kondisi_baik or 0) + (rec.kondisi_rusak or 0)
    keterangan = fields.Text(string='Keterangan')


    @api.depends('total', 'jumlah')
    def _compute_total_display(self):
        for rec in self:
            if rec.total != rec.jumlah:
                # Tambahkan simbol agar menonjol
                rec.total_display = f"⚠ {rec.total}"
            else:
                rec.total_display = str(rec.total)
    # @api.model_create_multi
    # def create(self, vals_list):
    #     return super().create(vals_list)
    # @api.onchange('item_id')
    # def _onchange_item_id(self):
    #     for rec in self:
    #         if rec.item_id:
    #             rec.jumlah = rec.item_id.qty  # pastikan 'qty' adalah field jumlah aset

    