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
    keterangan = fields.Text(string='Keterangan')
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
    def action_submit(self):
        for rec in self:
            total = (rec.kondisi_baik or 0) + (rec.kondisi_rusak or 0)
            if total != rec.jumlah:
                # Tambahkan warning via chatter (log note)
                rec.message_post(
                    body="⚠️ Jumlah kondisi tidak sesuai dengan jumlah aset. Proses akan masuk ke approval."
                )
                rec.state = 'on_approval'
                rec.current_approval_index = 0
            else:
                rec.state = 'approved'

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


    approval_route_ids = fields.Many2many('approval.route.line', string='Approval Routes')
    current_approval_index = fields.Integer(string='Current Approval Index', default=0)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('on_approval', 'On Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    def action_submit(self):
        for rec in self:
            rec.state = 'on_approval'
            rec.current_approval_index = 0

    def action_approve(self):
        for rec in self:
            if rec.state != 'on_approval':
                raise ValidationError("Record is not under approval.")
            route_lines = sorted(rec.approval_route_ids, key=lambda x: x.sequence)
            if rec.current_approval_index >= len(route_lines):
                raise ValidationError("No more approval steps.")

            current_route = route_lines[rec.current_approval_index]
            group = current_route.group_id

            # Cari external ID dari group
            group_ext_id = group.get_external_id().get(group.id)
            if not group_ext_id:
                raise ValidationError(f"Group {group.name} doesn't have an external ID defined.")

            if not self.env.user.has_group(group_ext_id):
                raise ValidationError("You are not authorized to approve this step.")

            rec.current_approval_index += 1
            if rec.current_approval_index == len(route_lines):
                rec.state = 'approved'

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'


    def _show_submit_button(self):
            return self.state == 'draft'

    def _show_approve_button(self):
            return self.state == 'on_approval'

    def _show_reject_button(self):
            return self.state == 'on_approval'
