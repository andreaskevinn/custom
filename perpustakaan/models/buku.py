from odoo import models, fields, api

class buku(models.Model):
    _name = 'perpustakaan.buku'
    _description = 'class buku untuk UTS'
    _rec_name = 'judul'
    #_order = 'date desc' #default=id

    judul = fields.Char('Judul Buku', size=64, readonly=True, required=True, index=True,
                        states={'draft': [('readonly', False)]})
    id_buku = fields.Char('ID Buku', size=8, readonly=True , required=True, index=True, states={'draft': [('readonly', False)]})
    pengarang = fields.Char('Pengarang', size=64, readonly=True ,required=True, index=True, states={'draft': [('readonly', False)]})
    penerbit = fields.Char('Penerbit', size=64, readonly=True , required=True, index=True, states={'draft': [('readonly', False)]})
    #active=fields.Boolean('Status Anggota: aktif / nonaktif', default=True, readonly=True, states={'draft': [('readonly', False)]})

    # anggota_id = fields.Many2one('perpustakaan.anggota', string='Idea', readonly=True, ondelete="cascade",
    #                           states={'draft': [('readonly', False)]},
    #                           domain="[('state', '=', 'done'), ('active', '=', 'True')]")

    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('recorded', 'Recorded'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    _sql_constraints = [('name_unik', 'unique(name)', ('Ideas must be unique!'))]

    def test_buku(self):
        print("test buku")
        # test
        t = self.env.context
        print(t.get('keterangan'))

    def action_recorded(self):
        self.state = 'recorded'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'
