from odoo import models, fields, api, _
from odoo.exceptions import UserError

class pengambilan(models.Model):  # inherit dari Model
    _name = 'ekspedisi.pengambilan'  # atribut dari class Model
    _description = 'Data pengambilan barang '
    #_rec_name = 'id_pengambilan'
    #_order = 'name asc'  # defaultnya adalah id, pengaruhnya saat list view
    #id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # membuat attribute field
    id_pengambilan = fields.Char('ID Pengambilan', size=64, required=True, index=True, readonly=False, default='',
                                 states={'draft': [('readonly', False)]})
    tanggalpengambilan = fields.Date('Tanggal pengambilan', size=64, required=True, index=True, readonly=False, default='',
                       states={'draft': [('readonly', False)]})
    # jumlahbarangdiambil = fields.Float('Jumlah barang diambil', size=64, required=True, index=True, readonly=False, default='',
    #                              states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                            ('confirmed', 'Confirmed'),
                            ('done', 'Done'),
                            ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
                            default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})

    kendaraan_id = fields.Many2one('ekspedisi.kendaraan', string="Kendaraan", readonly=False, ondelete='cascade',
                                   states={'draft': [('readonly', False)]})
    barang_ids = fields.Many2many('ekspedisi.gudang', string="Barang", readonly=False, ondelete='cascade',
                                   states={'draft': [('readonly', False)]})

    _sql_constraints = [('id_pengambilan_unik', 'unique(id_pengambilan)', ('ID sudah digunakan!'))]

    # @api.onchange('barang_ids')
    # def _func_onchange_barang_id(self):
    #     for test in self:
    #         if not test.barang_ids:
    #             return {}
    #         else:
    #             test.barang_ids.jumlahbarang = test.barang_ids.jumlahbarang - test.barang_ids.jumlahbarangdiambil
    #         return {}

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'