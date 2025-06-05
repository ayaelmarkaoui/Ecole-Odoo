from odoo import models, fields, api
import base64




class EcoleNote(models.Model):
    _name = 'ecole.note'
    _description = 'Note'

    student_id = fields.Many2one('res.partner', string='Élève')
    subject_id = fields.Many2one('ecole.matiere', string='Matière')
    name = fields.Char(string="Nom", default="Bulletin", readonly=True)
    email_parent = fields.Char(string="Email Parent", related='student_id.email_parent', store=True)

    teacher_id = fields.Many2one('res.users', string='Professeur' , readonly=True)
    note = fields.Float(string='Note')
    note_line_ids = fields.One2many('ecole.note.line', 'note_id', string="Lignes de note")
    moyenne = fields.Float(string="Moyenne", compute='_compute_average', store=True)
    statut = fields.Selection([
        ('passe', 'Passé'),
        ('double', 'Doublé')
    ], string="Statut", compute='_compute_average', store=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    def do_print(self):

        return self.env.ref('ecole.action_report_bulletin_report').report_action(self)

    @api.depends('note_line_ids.note', 'note_line_ids.coefficient')
    def _compute_average(self):
        for rec in self:
            total_notes = 0.0
            total_coefficients = 0.0
            for line in rec.note_line_ids:
                if line.note is not None and line.coefficient:
                    total_notes += line.note * line.coefficient
                    total_coefficients += line.coefficient

            rec.moyenne = total_notes / total_coefficients if total_coefficients else 0.0
            rec.statut = 'passe' if rec.moyenne >= 10 else 'double'

    @api.onchange('subject_id')
    def _onchange_subject_id(self):
        if self.subject_id:
            self.teacher_id = self.subject_id.teacher_id

    def send_mail(self):
        print("Début génération et envoi mail")

        report_service = self.env.ref('ecole.action_report_bulletin_report')
        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(report_service.report_name, [self.id])

        encoded_pdf = base64.b64encode(pdf_content)

        attachment_vals = {
            'name': 'bulletin.pdf',
            'type': 'binary',
            'datas': encoded_pdf,
            'store_fname': 'rapport_bulletin.pdf',
            'mimetype': 'application/pdf',
            'res_model': 'ecole.note',
            'res_id': self.id,
        }
        attachment = self.env['ir.attachment'].create(attachment_vals)

        student_name = self.student_id.name or "Votre enfant"
        moyenne = self.moyenne or 0.0
        statut = self.statut or ''

        if moyenne >= 10:
            message = f"""
                        <p>Bonjour,</p>
                        <p>Nous vous félicitons ! <strong>{student_name}</strong> a obtenu une moyenne générale de <strong>{moyenne:.2f}</strong> et a <strong>réussi ses examens</strong>.</p>
                        <p>Veuillez trouver ci-joint son bulletin scolaire.</p>
                        <p>Cordialement,<br/>L'administration</p>
                    """
        else:
            message = f"""
                        <p>Bonjour,</p>
                        <p>Nous vous informons que <strong>{student_name}</strong> a obtenu une moyenne de <strong>{moyenne:.2f}</strong> et <strong>n’a pas validé son année</strong>.</p>
                        <p>Veuillez trouver ci-joint son bulletin scolaire.</p>
                        <p>Courage et merci de votre suivi parental.</p>
                    """
        subject = 'Bulltein'
        email_from = self.env.user.email
        email_to = self.email_parent

        mail_vals = {
            'res_id': self.id,
            'model': 'ecole.note',
            'email_from': email_from,
            'email_to': email_to,
            'subject': subject,
            'body_html': message,
            'attachment_ids': [(4, attachment.id)],
            'auto_delete': False,
        }
        mail = self.env['mail.mail'].sudo().create(mail_vals)
        mail.send()

        print("Email envoyé avec succès")
        return True