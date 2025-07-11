from odoo import  fields, models, api
from odoo.exceptions import ValidationError

class InspectionRecord(models.Model):
    _name = "inspection.record"
    _description = "Inspection Record"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "date desc, name"
    
    name = fields.Char(string="Inspection Name", copy=False, readonly=True)

    date = fields.Date(string="Inspection Date", required=True, default=fields.Date.context_today)
    inspector_id = fields.Many2one(
        'res.users',
        string="Inspector",
        required=True,
        default=lambda self: self.env.user.id
    )
    inspection_item_ids = fields.One2many('inspection.item', 'inspection_id', string='Inspection Items')

    notes = fields.Text(string='General Notes', help="Any general remarks about this inspection.")

    total_score = fields.Float(string='Total Score', compute='_compute_total_score', store=True)

    acknowledged_by_id = fields.Many2one('res.users', string='Acknowledged By', readonly=True, tracking=True,
                                         help="The user who acknowledged this inspection record.")
    acknowledgement_date = fields.Datetime(string='Acknowledgement Date', readonly=True, tracking=True,
                                           help="Date and time when the inspection record was acknowledged.")
    cleaning_personnel_id = fields.Many2one(
        'hr.employee', string='Penanggung Jawab Cleaning Service',
        help="Karyawan yang bertanggung jawab untuk membersihkan area yang diperiksa.")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], string='Status', default='draft', tracking=True)
    
    start_inspection_date = fields.Datetime(
        string='Start Inspection Date')
    end_inspection_date = fields.Datetime(
        string='End Inspection Date')
    
    @api.model
    def _get_default_name(self):
        today = fields.Date.context_today(self)
        yymm = today.strftime('%y%m')
        domain = [
            ('name', 'like', yymm),
        ]
        count = self.search_count(domain) + 1
        running_number = str(count).zfill(3)
        return f"{yymm}{running_number}"

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals.get('name') == '':
            vals['name'] = self._get_default_name()
        return super(InspectionRecord, self).create(vals)
    
    @api.depends('inspection_item_ids.score')
    def _compute_total_score(self):
        for record in self:
            record.total_score = sum(item.score for item in record.inspection_item_ids if item.score)

    @api.constrains('date')
    def _check_inspection_date(self):
        for record in self:
            if record.date and record.date > fields.Date.today():
                raise ValidationError(("Inspection Date cannot be in the future."))

    def action_start_inspection(self):
        self.ensure_one()
        if self.state == 'draft':
            self.state = 'in_progress'
            self.start_inspection_date = fields.Datetime.now()

    def action_complete_inspection(self):
        self.ensure_one()
        if self.state == 'in_progress':
            self.state = 'completed'
            self.end_inspection_date = fields.Datetime.now()
            self.inspector_id = self.env.user.id  # Set the inspector to the current user
            # Opsional: Logika tambahan setelah completed, misal notifikasi

    def action_cancel_inspection(self):
        self.ensure_one()
        if self.state in ['draft', 'in_progress']:
            self.state = 'canceled'

    def action_acknowledge_inspection(self):
        self.ensure_one()
        if self.state == 'completed' and not self.acknowledged_by_id:
            self.write({
                'acknowledged_by_id': self.env.user.id,
                'acknowledgement_date': fields.Datetime.now(),
            })
            self.message_post(body=("Inspection record has been acknowledged by %s.") % self.env.user.name)
        else:
            raise ValidationError(("This inspection record cannot be acknowledged at this moment."))