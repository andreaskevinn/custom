from odoo import models, fields, api, _

class wizpemesanan(models.TransientModel):
    _name = 'wiz.ekspedisi.pemesanan'
    _description = 'class untuk menyimpan data nilai karyawan'
    _id = fields.Char()

    pemesanan_id = fields.Many2one('ekspedisi.pemesanan', String='Pemesanan')

    # semester = fields.Selection(related='kelas_id.semester')
    # tahun = fields.Char(related='kelas_id.tahun')

    # mk_id = fields.Many2one(related='kelas_id.mk_id')

    line_ids = fields.One2many('wiz.ekspedisi.pemesanan.lines', 'wiz_header_id', string='Pemesanan')

    @api.model
    def default_get(self,
                    fields_list):  # ini adalah common method, semacam constructor, akan dijalankan saat create object. Ini akan meng-overwrite default_get dari parent
        res = super(wizpemesanan, self).default_get(fields_list)
        # res  merupakan dictionary beserta value yang akan diisi, yang sudah diproses di super class (untuk create record baru)
        res['pemesanan_id'] = self.env.context['active_id']
        return res

    @api.onchange('pemesanan_id')
    def onchange_pemesanan_id(self):
        if not self.pemesanan_id:
            return
        vals = []
        line_ids = self.env['wiz.ekspedisi.pemesanan.lines']
        for rec in self.pemesanan_id.line_ids:
            line_ids += self.env['wiz.ekspedisi.pemesanan.lines'].new({
                'wiz_header_id': self.id,
                'karyawan_id': rec.karyawan_id.id,
                'ref_pemesanan_lines_id': rec.id
            })
            # cara membuat record baru di m2m atau o2m
        self.line_ids = line_ids

    def action_confirm(self):
        for rec in self.line_ids:
            rec.ref_pemesanan_lines_id.grade = rec.grade


class pemesanan_lines_wiz(models.TransientModel):
    _name = 'wiz.ekspedisi.pemesanan.lines'
    _description = 'class untuk menyimpan data nilai karyawan'

    wiz_header_id = fields.Many2one('wiz.ekspedisi.pemesanan', string='Pemesanan')
    karyawan_id = fields.Many2one('ekspedisi.karyawan', string='Karyawan', ondelete="restrict")
    ref_pemesanan_lines_id = fields.Many2one('ekspedisi.pemesanan.lines') #untuk refer ke kelas line id yang mana
    grade = fields.Selection([('★★★★★', '★★★★★'),
                              ('★★★★', '★★★★'),
                              ('★★★', '★★★'),
                              ('★★', '★★'),
                              ('★', '★')])