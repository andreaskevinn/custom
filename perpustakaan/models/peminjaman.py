from odoo import models, fields, api

class peminjaman(models.Model):
    _name = 'perpustakaan.peminjaman'
    _description = 'class peminjaman untuk UTS'
    #_rec_name = 'name'
    #_order = 'date desc' #default=id

    id_peminjaman = fields.Char('Nomor Peminjaman', size=64, readonly=True , required=True, index=True, states={'draft': [('readonly', False)]})
    #jumlah_pinjam = fields.Char('Jumlah buku dipinjam', size=64, readonly=True ,required=True, index=True, states={'draft': [('readonly', False)]})
    #active=fields.Boolean('Status Anggota: aktif / nonaktif', default=True, readonly=True, states={'draft': [('readonly', False)]})

    date = fields.Date('Tanggal pinjam', default=fields.Date.context_today, readonly=True)

    admin_id = fields.Many2one('res.users', 'Admin', readonly=True, ondelete='cascade', default=lambda self: self.env.user)

    anggota_id = fields.Many2one('perpustakaan.anggota', string="Anggota", readonly=False, ondelete='cascade', states={'draft': [('readonly', False)]}, domain="[('state','=','done')]")
    buku_id = fields.Many2one('perpustakaan.buku', string='Buku', readonly=False, ondelete='cascade', states={'draft': [('readonly', False)]}, domain="[('state','=','confirmed')]")

    datepredenda = fields.Date('Tanggal kembali', default=fields.Date.context_today, readonly=True,
                               states={'draft': [('readonly', False)]})

    tot_denda = fields.Integer("Jumlah Denda", compute="_compute_denda", store=True, default=0)

    date2 = fields.Date('Tanggal kembali sebelum denda', default=fields.Date.context_today, readonly=False)

    state = fields.Selection(
        [('draft', 'Draft'),
         ('dipinjam', 'Dipinjam'),
         ('selesai', 'Selesai'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=False, default='draft')

    _sql_constraints = [('name_unik', 'unique(name)', ('Ideas must be unique!'))]

    @api.depends('datepredenda', 'date2')
    def _compute_denda(self):
        if self.datepredenda and self.date2:
            datepredenda = fields.Datetime.from_string(self.datepredenda)
            date2 = fields.Datetime.from_string(self.date2)
            self.tot_denda = abs((date2 - datepredenda).days) * 50

    def action_dipinjam(self):
        self.state = 'dipinjam'

    def action_selesai(self):
        self.state = 'selesai'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'
