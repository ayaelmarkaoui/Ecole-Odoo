from odoo import models, fields

class EcoleEleve(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string='Est un élève', default=False)
    email_parent = fields.Char(string='Email parents')
