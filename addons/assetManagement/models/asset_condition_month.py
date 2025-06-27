from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AssetConditionMonth(models.Model):
    _name = 'x_asset.condition.month'
    _description = 'Kondisi Bulanan Aset'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    item_id = fields.Many2one(
        'x_asset.item',
        string='Item Aset',
        required=True,
        ondelete='cascade',
        domain="[('onHandQuantity', '>', 0)]"
    )
    tanggal = fields.Date(string='Tanggal', required=True)
    jumlah = fields.Integer(string='Jumlah', readonly=True)
    kondisi_baik = fields.Integer(string='Kondisi Baik')
    kondisi_rusak = fields.Integer(string='Kondisi Rusak')
    justification = fields.Text(string='Justifikasi')
    bulan_tahun = fields.Char(string='Bulan - Tahun', compute='_compute_bulan_tahun', store=True)
    inspect_by = fields.Many2one('res.users', string='Inspected By', readonly=True)

    @api.depends('tanggal')
    def _compute_bulan_tahun(self):
        for record in self:
            if record.tanggal:
                record.bulan_tahun = record.tanggal.strftime('%B %Y')
            else:
                record.bulan_tahun = ''

    @api.onchange('item_id')
    def _onchange_item_id(self):
        for record in self:
            if record.item_id:
                record.jumlah = record.item_id.onHandQuantity
            else:
                record.jumlah = 0

    @api.constrains('kondisi_baik', 'kondisi_rusak', 'jumlah')
    def _check_kondisi_total(self):
        for record in self:
            total = (record.kondisi_baik or 0) + (record.kondisi_rusak or 0)
            _logger.debug(
                "[CHECK] kondisi_baik=%s, kondisi_rusak=%s, jumlah=%s",
                record.kondisi_baik, record.kondisi_rusak, record.jumlah
            )
            if total != record.jumlah:
                raise ValidationError("Jumlah kondisi baik + rusak harus sama dengan total jumlah aset.")

    @api.model
    def create(self, vals):
        # Isi inspect_by jika belum ada
        if not vals.get('inspect_by'):
            vals['inspect_by'] = self.env.uid

        # Hitung jumlah dari item jika belum ada
        if 'jumlah' not in vals and vals.get('item_id'):
            item = self.env['x_asset.item'].browse(vals['item_id'])
            vals['jumlah'] = item.onHandQuantity

        return super().create(vals)

    def write(self, vals):
        # Jika item_id berubah, update juga jumlah
        if 'item_id' in vals:
            item = self.env['x_asset.item'].browse(vals['item_id'])
            vals['jumlah'] = item.onHandQuantity
        return super().write(vals)
