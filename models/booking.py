from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DarmanBooking(models.Model):
    _name = 'darman.booking'
    _description = 'Booking Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Add inheritance for chatter functionality

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    name = fields.Char(string='Partner Name', compute='_compute_partner_details', store=True, readonly=True)
    mobile = fields.Char(string='Mobile Number', compute='_compute_partner_details', store=True, readonly=True)
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        default='draft',
        required=True,
        tracking=True  # Enable tracking for the state field
    )
    description = fields.Text(string='Description')  # New description field
    partner_type = fields.Selection(
        related='partner_id.partner_type',
        string='نوع همکار',
        store=True,
        readonly=True
    )

    adult_count = fields.Integer(
        string='Adults (12+ years)',
        required=True,
        default=1,
        tracking=True,
        help='Number of adults (12 years and older)'
    )
    
    child_count = fields.Integer(
        string='Children (2-11 years)',
        default=0,
        tracking=True,
        help='Number of children (between 2 and 11 years)'
    )
    
    infant_count = fields.Integer(
        string='Infants (0-2 years)',
        default=0,
        tracking=True,
        help='Number of infants (under 2 years)'
    )
    
    total_guests = fields.Integer(
        string='Total Guests',
        compute='_compute_total_guests',
        store=True,
        help='Total number of guests'
    )

    @api.depends('partner_id')
    def _compute_partner_details(self):
        for record in self:
            record.name = record.partner_id.name if record.partner_id else ''
            record.mobile = record.partner_id.mobile if record.partner_id else ''

    @api.depends('adult_count', 'child_count', 'infant_count')
    def _compute_total_guests(self):
        for record in self:
            record.total_guests = record.adult_count + record.child_count + record.infant_count

    @api.constrains('adult_count', 'child_count', 'infant_count')
    def _check_guest_counts(self):
        for record in self:
            if record.adult_count < 1:
                raise ValidationError(_('At least one adult is required'))
            if any(count < 0 for count in [record.adult_count, record.child_count, record.infant_count]):
                raise ValidationError(_('Number of guests cannot be negative'))
            if record.total_guests > 10:
                raise ValidationError(_('Maximum 10 guests allowed per booking'))

