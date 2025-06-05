from odoo import models, fields

class EcoleMatiere(models.Model):
    _name = 'ecole.matiere'
    _description = 'Matiere'

    name = fields.Char(required=True)
    coefficient = fields.Integer(string='Coefficient')
    teacher_id = fields.Many2one('res.users', string='Professeur')
    ecole_matier_ids = fields.One2many('ecole.matiere.line', 'ecole_matiere_id', string="Lignes de programme")

    # product_ids = fields.One2many('product.template',  'ecole_matiere_id', string="Lignes de programme")

    # programme_matiere_ids = fields.One2many('product.template', 'ecole_matiere_id', string="Lignes de programme")

class EcoleMatiereLine(models.Model):
    _name = 'ecole.matiere.line'

    ecole_matiere_id = fields.Many2one('ecole.matiere')
    product_id = fields.Many2one('product.template')




