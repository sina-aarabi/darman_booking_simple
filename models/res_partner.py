from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection([
        ('fanap', 'گروه فناپ'),
        ('pasargad_financial', 'گروه مالی بانک پاسارگاد'),
        ('pasargad_club', 'باشگاه مشتریان بانک پاسارگاد')
    ], string='نوع همکار', tracking=True)