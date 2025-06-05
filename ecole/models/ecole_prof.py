from odoo import models, fields

class EcoleProf(models.Model):

    _inherit = "res.users"

    matiere_id = fields.Many2one('ecole.matiere', string="Matière", required=False)
    eleve_ids = fields.Many2many('res.partner',
        string='Élèves'
    )
    