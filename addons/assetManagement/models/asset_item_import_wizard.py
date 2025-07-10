import base64
import io
import openpyxl
from odoo import models, fields, api
from odoo.exceptions import UserError

class AssetItemImportWizard(models.TransientModel):
    _name = 'asset.item.import.wizard'
    _description = 'Import Item Aset dari Excel'

    file = fields.Binary(string="File Excel", required=True)
    filename = fields.Char(string="Nama File")

    def action_import(self):
        try:
            wb = openpyxl.load_workbook(io.BytesIO(base64.b64decode(self.file)))
            sheet = wb.active

            header = [cell.value for cell in sheet[1]]
            required_fields = ['name', 'onHandQuantity', 'note', 'location_name']
            for rf in required_fields:
                if rf not in header:
                    raise UserError(f"Kolom '{rf}' tidak ditemukan di file Excel.")

            for row in sheet.iter_rows(min_row=2, values_only=True):
                row_data = dict(zip(header, row))

                location_name = str(row_data.get('location_name')).strip()
                if not location_name:
                    raise UserError(f"Nama lokasi tidak boleh kosong. Periksa baris dengan aset: {row_data.get('name')}")

                location = self.env['stock.location'].search([('name', '=', location_name)], limit=1)
                if not location:
                    location = self.env['stock.location'].create({
                        'name': location_name,
                        'usage': 'internal'
                    })

                self.env['x_asset.item'].create({
                    'name': row_data.get('name'),
                    'onHandQuantity': int(row_data.get('onHandQuantity') or 0),
                    'note': row_data.get('note') or '-',
                    'location_id': location.id,
                })

        except Exception as e:
            raise UserError(f"Terjadi kesalahan saat mengimpor: {str(e)}")
