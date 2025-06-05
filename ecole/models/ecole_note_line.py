from odoo import models, fields, api
from odoo.exceptions import AccessError


class EcoleNoteLine(models.Model):
    _name = 'ecole.note.line'
    _description = "Détail des notes"

    student_id = fields.Many2one('res.partner', string='Élève')
    note_id = fields.Many2one('ecole.note', string="Note Globale")
    coefficient = fields.Integer('ecole.matiere', related='subject_id.coefficient', store=True)
    subject_id = fields.Many2one('ecole.matiere', string="Matière")
    note = fields.Float(string="Note")
    available_subject_ids = fields.Many2many('ecole.matiere', compute='_compute_available_subjects')

    @api.depends('note_id')
    def _compute_available_subjects(self):
        for rec in self:
            if rec.env.user.has_group('base.group_system'):
                rec.available_subject_ids = rec.env['ecole.matiere'].search([])
            else:
                rec.available_subject_ids = rec.env['ecole.matiere'].search([('teacher_id', '=', rec.env.user.id)])

    @api.model
    def create(self, vals):
        user = self.env.user
        subject = self.env['ecole.matiere'].browse(vals.get('subject_id'))
        if not user.has_group('base.group_system') and subject and subject.teacher_id != user:
            raise AccessError("Vous ne pouvez pas créer une note pour une matière que vous n'enseignez pas.")
        return super().create(vals)

    def write(self, vals):
        user = self.env.user
        subject = self.env['ecole.matiere'].browse(vals['subject_id']) if 'subject_id' in vals else self.subject_id
        if not user.has_group('base.group_system') and subject and subject.teacher_id != user:
            raise AccessError("Vous ne pouvez pas modifier une matière que vous n'enseignez pas.")
        return super().write(vals)