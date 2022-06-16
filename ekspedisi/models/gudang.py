from odoo import models, fields, api, _
from odoo.exceptions import UserError

class gudang(models.Model):  # inherit dari Model
    _name = 'ekspedisi.gudang'  # atribut dari class Model
    _description = 'Data barang di gudang '
    _rec_name = 'namabarang'
    #_order = ''  # defaultnya adalah id, pengaruhnya saat list view
    #id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # membuat attribute field
    namabarang = fields.Char('Nama Barang', size=64, required=True, index=True, readonly=False, default='',
                       states={'draft': [('readonly', False)]})
    jumlahbarang = fields.Char('Sisa Jumlah Barang', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})
    tanggalpembelian = fields.Date('Tanggal Pembelian', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})
    hargabarang = fields.Char('Harga Barang (Rp.)', size=64, required=True, index=True, readonly=False, default='',
                                   states={'draft': [('readonly', False)]})
    # jumlahdiambilterakhir = fields.Char('Jumlah diambil terakhir', size=64, required=False, index=True, readonly=False, default='',
    #                           states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                            ('confirmed', 'Confirmed'),
                            ('done', 'Done'),
                            ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
                            default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})

    ambil_ids = fields.Many2many('ekspedisi.pengambilan', 'barang_id', string='Pengambilan')

    vendor_id = fields.Many2one('ekspedisi.vendor', string="Vendor", readonly=False, ondelete='cascade',
                                  states={'draft': [('readonly', False)]})

    _sql_constraints = [('namabarang_unik', 'unique(namabarang)', _('Barang sudah terdaftar!'))]

    # jumlahbarangdiambil = fields.Float(string='Jumlah barang diambil', compute='_func_onchange_barang_id', readonly=False,states={'draft': [('readonly', False)]})


    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'