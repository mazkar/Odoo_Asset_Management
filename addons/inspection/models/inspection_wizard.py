from odoo import fields, models, api, _
from odoo.exceptions import UserError

class CreateDailyInspectionWizard(models.TransientModel):
    _name = 'inspection.create.daily.wizard'
    _description = 'Wizard to Create Daily Inspection Record'

    inspector_id = fields.Many2one('res.users', string='Inspector', default=lambda self: self.env.user, required=True)
    inspection_date = fields.Datetime(string='Inspection Date', required=True, default=fields.Datetime.now)
    
    filter_location_ids = fields.Many2many('stock.warehouse', string='Lokasi Inspeksi',
                                           default=lambda self: self._get_default_all_locations(),
                                           help="Pilih lokasi yang akan dilakukan inspeksi.")

    @api.model
    def _get_default_all_locations(self):
        """
        Returns the IDs of all stock.warehouse records to be pre-selected by default.
        """
        # Pastikan model 'stock.warehouse' tersedia (modul 'stock' harus terinstal)
        if 'stock.warehouse' in self.env:
            return self.env['stock.warehouse'].search([]).ids # Mencari semua record dan mengambil list ID-nya
        return [] # Kembalikan list kosong jika model tidak ditemukan (misal modul stock belum terinstal)


    def action_create_inspection_record(self):
        """
        Create a new inspection record and its items based on selected locations (filter) and active tasks.
        """
        self.ensure_one()
        
        inspection_record_vals = {
            'date': self.inspection_date,
            'inspector_id': self.inspector_id.id,
            'state': 'draft',
        }
        new_inspection = self.env['inspection.record'].create(inspection_record_vals)

        active_tasks_domain = [('active', '=', True)]
        # Jika ada filter lokasi di wizard, tambahkan ke domain ini
        if self.filter_location_ids:
            # Domain untuk filter tasks yang location_id-nya ada di filter_location_ids
            active_tasks_domain.append(('location_id', 'in', self.filter_location_ids.ids))

        active_tasks = self.env['task.master'].search(active_tasks_domain)

        if not active_tasks:
            new_inspection.unlink() # Hapus header jika tidak ada item yang dibuat
            raise UserError(_("No active inspection tasks found (or no tasks matching your filter). Please define tasks in Task Master."))

        inspection_items_vals = []
        for task in active_tasks:
            inspection_items_vals.append({
                'inspection_id': new_inspection.id,
                'task_master_id': task.id,
                # location_id akan otomatis terisi dari task.location_id karena related field
            })
        
        if inspection_items_vals:
            self.env['inspection.item'].create(inspection_items_vals)

        # Arahkan pengguna ke form inspection record yang baru dibuat
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Daily Inspection'),
            'res_model': 'inspection.record',
            'res_id': new_inspection.id,
            'view_mode': 'form',
            'target': 'current',
        }