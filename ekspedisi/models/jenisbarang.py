from odoo import models, fields, api, _
from odoo.exceptions import UserError

class jenisbarang(models.Model):  # inherit dari Model
    _name = 'ekspedisi.jenisbarang'  # atribut dari class Model
    _description = 'Data Jenis Barang dan Harga '
    _rec_name = 'combination'
    #_order = 'name asc'  # defaultnya adalah id, pengaruhnya saat list view
    #id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # membuat attribute field
    namajenisbarang = fields.Char('Nama Jenis Barang', size=64, required=True, index=True, readonly=False, default='',
                       states={'draft': [('readonly', False)]})
    satuanbarang = fields.Char('Satuan Jenis Barang', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})
    bentukbarang = fields.Char('Bentuk Jenis Barang', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})
    hargajenisbarang = fields.Char('Harga Jenis Barang per satuan (Rp.)', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                            ('confirmed', 'Confirmed'),
                            ('done', 'Done'),
                            ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
                            default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})

    pesan_ids = fields.One2many('ekspedisi.pemesanan', 'jenisbarang_id', string='Pemesanan')

    _sql_constraints = [('namajenisbarang_unik', 'unique(namajenisbarang)', _('Jenis barang sudah terdaftar!'))]

    combination = fields.Char(string='Combination', compute='_compute_fields_combination')

    @api.depends('namajenisbarang', 'satuanbarang')
    def _compute_fields_combination(self):
        for test in self:
            test.combination = test.namajenisbarang + ' - ' + test.satuanbarang


    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'