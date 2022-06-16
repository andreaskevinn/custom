from odoo import models, fields, api, _
from odoo.exceptions import UserError

class vendor(models.Model):  # inherit dari Model
    _name = 'ekspedisi.vendor'  # atribut dari class Model
    _description = 'Data Vendor '
    _rec_name = 'namavendor'
    #_order = 'name asc'  # defaultnya adalah id, pengaruhnya saat list view
    #id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # membuat attribute field
    id_vendor = fields.Char('ID vendor', size=64, required=True, index=True, readonly=False, default='',
                                 states={'draft': [('readonly', False)]})
    namavendor = fields.Char('Nama Vendor', size=64, required=True, index=True, readonly=False, default='',
                       states={'draft': [('readonly', False)]})
    notelpvendor = fields.Char('No Telp Vendor', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})
    alamat = fields.Char('Alamat Vendor', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                            ('confirmed', 'Confirmed'),
                            ('done', 'Done'),
                            ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
                            default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})

    barang_ids = fields.One2many('ekspedisi.gudang', 'vendor_id', string='Barang')

    _sql_constraints = [('id_vendor_unik', 'unique(id_vendor)', ('ID sudah digunakan!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'