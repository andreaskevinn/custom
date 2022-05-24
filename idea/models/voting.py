from odoo import models, fields, api,_
from odoo.exceptions import UserError
#_ untuk translate

class voting(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'idea.voting' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel
    # (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk berlatih ttg voting'
    _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    _order = 'date desc' #defaultnya adalah id, pengaruhnya saat list view
    #id = fields.Integer() ini otomatis ada di odoo, akan jadi PK


    #membuat attribute field. Field ini punya common parameter

    name = fields.Char('Name (voting number)', default="new",size=64, required=True, index=True, readonly=True,states={})
    #kita harus punya field name ini.
    #Untuk tipe Char, selain punya common paramater, juga punya parameter khusus translate
    #Tips: untuk nama customer, nama sup, nrp, doc number itu diberi nama name, jgn pake nama field sesuai
    #peruntukannya. Di String boleh dikasi nama nrp, nama customer

    date = fields.Date('Voting date', default=fields.Date.context_today, readonly=True)
    # ini jadi nama field/kolom
    #dengan tipe data Date, parameter String ini akan jadi caption/label di form odoo
    #att pertama selalu String shg tdk perlu ditulis nama parameter-nya

    state = fields.Selection([('draft', 'Draft'), # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                            ('voted', 'Voted'),
                            ('canceled','Canceled')], 'State', required=True, readonly=False,# krn required, sebaiknya dikasi default
                            default='draft')# tuple di dalam list, nama field harus state spy bisa diakses oleh states

    vote = fields.Selection([('yes','Yes'),
                             ('no','No'),
                             ('abstain','Abstain')], 'Vote', required=True,readonly=False)

    # Description is read-only when not draft!
    #description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    #active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    confirm_date = fields.Date('Confirm date')

    # by convention, many2one fields end with '_id'
    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, ondelete='cascade', default=lambda self: self.env.user)

    idea_id = fields.Many2one('idea.idea', string='Idea', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done'), ('active', '=', 'True')]")

    idea_date = fields.Date("Idea date", related='idea_id.date')
    #sponsor_ids = fields.Many2many('res.partner', 'idea_idea_res_partner_rel', 'idea_idea_id', 'res_partner_id', 'Sponsors')
    #sponsor_ids = fields.Many2many('res.partner', string='Sponsors')

    _sql_constraints = [('name_unik', 'unique(name)', ('Ideas must be unique!'))]

    def action_canceled(self):
        self.state = 'canceled'
    def action_voted(self):
        self.state = 'voted'
    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        if self.name == 'new' or not self.name:  # kalo name nya masih default (default liat atas) or belum ada nama
            seq = self.env['ir.sequence'].search([("code", "=", "idea.voting")])
            if not seq:
                raise UserError(_("Idea.voting sequence not found, create it first"))
            for val in vals_list:
                val['name'] = seq.next_by_id()
            return super(voting,self).create(vals_list)
        #self.name = seq.next_by_id(sequence_data=self.date)  # pastikan ada date dan kalo ada tahun
        #self.name = seq.next_by_id() #kalo gaada tahun
