from odoo import models, fields, api, _
from odoo.exceptions import UserError

class karyawan(models.Model):  # inherit dari Model
    _name = 'ekspedisi.karyawan'  # atribut dari class Model
    _description = 'Data Karyawan'
    _rec_name = 'namakaryawan'
    #_order = 'name asc'  # defaultnya adalah id, pengaruhnya saat list view
    #id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # membuat attribute field
    idkaryawan = fields.Char('ID Karyawan', size=64, required=True, index=True, readonly=False, default='',
                       states={'draft': [('readonly', False)]})
    namakaryawan = fields.Char('Nama Karyawan', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})
    usiakaryawan = fields.Char('Usia Karyawan', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})
    alamatkaryawan = fields.Char('Alamat Karyawan', size=64, required=True, index=True, readonly=False, default='',
                         states={'draft': [('readonly', False)]})
    notelpkaryawan = fields.Char('No telp Karyawan', size=64, required=True, index=True,
                                 readonly=False, default='',
                                 states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                            ('confirmed', 'Confirmed'),
                            ('done', 'Done'),
                            ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
                            default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})

    pesan_ids = fields.One2many('ekspedisi.pemesanan', 'karyawan_id', string='Pemesanan')

    _sql_constraints = [('idkaryawan_unik', 'unique(idkaryawan)', _('ID Karyawan sudah terpakai!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'