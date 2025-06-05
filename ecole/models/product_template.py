from odoo import models, fields

class ProductTemplate(models.Model):
      _inherit = 'product.template'

      is_school_product = fields.Boolean(string = "Est un produit scolaire", default=False)
