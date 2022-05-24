from odoo import models, fields, api

class anggota(models.Model):
    _name = 'perpustakaan.anggota'
    _description = 'class anggota untuk UTS'
    _rec_name = 'name'
    #_order = 'date desc' #default=id

    id_anggota = fields.Char('ID Anggota', size=8, required=True, index=True, readonly=False)
    name = fields.Char('Nama Anggota', size=64, required=True, index=True)
    description = fields.Text('Deskripsi', readonly=True, states={'draft': [('readonly', False)]})
    active=fields.Boolean('Status Anggota: aktif / nonaktif', default=True, readonly=True, states={'draft': [('readonly', False)]})
    # gender = fields.Selection([('laki-laki', 'Laki-laki'),
    #                          ('perempuan', 'Perempuan'),
    #                          ('abstain', 'Abstain')], 'Vote', required=True, readonly=False)

    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('done', 'Done'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    pinjam_ids = fields.One2many('perpustakaan.peminjaman', 'anggota_id', string='Pinjam')

    _sql_constraints = [('name_unik', 'unique(name)', ('Ideas must be unique!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'
