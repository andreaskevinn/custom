from odoo import models, fields, api, _
from odoo.exceptions import UserError

class kendaraan(models.Model):  # inherit dari Model
    _name = 'ekspedisi.kendaraan'  # atribut dari class Model
    _description = 'Data kendaraan'
    _rec_name = 'nomorpolisi'
    #_order = 'name asc'  # defaultnya adalah id, pengaruhnya saat list view
    #id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # membuat attribute field
    nomorpolisi = fields.Char('Nomor Polisi Kendaraan', size=64, required=True, index=True, readonly=False, default='',
                       states={'draft': [('readonly', False)]})
    merkkendaraan = fields.Char('Merk Kendaraan', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})
    jeniskendaraan = fields.Char('Jenis Kendaraan', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})
    tanggalbelikendaraan = fields.Date('Tanggal Beli Kendaraan', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                            ('confirmed', 'Confirmed'),
                            ('done', 'Done'),
                            ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
                            default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})

    pesan_ids = fields.One2many('ekspedisi.pemesanan', 'kendaraan_id', string='Pemesanan')

    _sql_constraints = [('nomorpolisi_unik', 'unique(nomorpolisi)', _('Kendaraan sudah terdaftar!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'