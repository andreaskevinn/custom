from odoo import models, fields, api, _

class pemesanan(models.Model):
    _name = 'ekspedisi.pemesanan'
    _description = 'Pemesanan Jasa Ekspedisi'
    _rec_name = 'id'
    #_order = 'date desc' #default=id

    id = fields.Integer('Nomor Pemesanan', size=64, readonly=False , required=True, index=True, states={'draft': [('readonly', False)]})
    biayapengiriman = fields.Char('Biaya pengiriman', size=64, readonly=False ,required=True, index=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Status Pemesanan: aktif / nonaktif', default=True, readonly=False, states={'draft': [('readonly', False)]})
    jumlahmuatan = fields.Char('Jumlah muatan', size=64, readonly=False, required=True, index=True,
                                  states={'draft': [('readonly', False)]})

    date = fields.Date('Tanggal pemesanan', default=fields.Date.context_today, readonly=False)

    #admin_id = fields.Many2one('res.users', 'Admin', readonly=False, ondelete='cascade', default=lambda self: self.env.user)

    customer_id = fields.Many2one('ekspedisi.customer', string="Customer", readonly=False, ondelete='cascade', states={'draft': [('readonly', False)]})
    karyawan_id = fields.Many2one('ekspedisi.karyawan', string="Karyawan", readonly=False, ondelete='cascade',
                                  states={'draft': [('readonly', False)]})
    kendaraan_id = fields.Many2one('ekspedisi.kendaraan', string="Kendaraan", readonly=False, ondelete='cascade',
                                  states={'draft': [('readonly', False)]})
    jenisbarang_id = fields.Many2one('ekspedisi.jenisbarang', string="Jenis Barang", readonly=False, ondelete='cascade',
                                  states={'draft': [('readonly', False)]})

    line_ids = fields.One2many('ekspedisi.pemesanan.lines', 'pemesanan_id', string='Nilai', readonly=True,
                               states={'draft': [('readonly', False)]})

    state = fields.Selection(
        [('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('confirmed', 'Confirmed'),
         ('done', 'Done'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})

    karyawan_grade = fields.Selection('Nilai karyawan', related='line_ids.grade')

    _sql_constraints = [('id_pemesanan_unik', 'unique(id_pemesanan)', ('ID sudah terpakai!'))]

    totalbiaya = fields.Float('Total biaya', size=64, readonly=True, required=False, index=True)

    hargajenis = fields.Float('Harga Jenis', size=64, readonly=True, required=False, index=True)

    totalbiayafix = fields.Float(string='Total Biaya', compute='_func_onchange_jenisbarang_id', required=False)

    @api.onchange('jenisbarang_id')
    def _func_onchange_jenisbarang_id(self):
        for test in self:
            if test.jenisbarang_id:
                a = float(test.jenisbarang_id.hargajenisbarang)
                b = float(test.jumlahmuatan)
                c = float(test.biayapengiriman)
                test.totalbiaya = a * b
                test.totalbiaya = test.totalbiaya + c
                test.totalbiayafix = float(test.totalbiaya)

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

    def action_wiz_pemesanan(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Ekspedisi Pemesanan'),
            'res_model': 'wiz.ekspedisi.pemesanan',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

    class pemesanan_lines(models.Model):
        _name = 'ekspedisi.pemesanan.lines'
        _description = 'class untuk menyimpan data nilai karyawan'

        pemesanan_id = fields.Many2one('ekspedisi.pemesanan', string='Pemesanan', ondelete="cascade")
        karyawan_id = fields.Many2one('ekspedisi.karyawan', string='Karyawan', ondelete="restrict")
        grade = fields.Selection([('★★★★★', '★★★★★'),
                                  ('★★★★', '★★★★'),
                                  ('★★★', '★★★'),
                                  ('★★', '★★'),
                                  ('★', '★')])
        _sql_constraints = [('name_unik', 'unique(pemesanan_id, karyawan_id)', _('ID already exist!'))]