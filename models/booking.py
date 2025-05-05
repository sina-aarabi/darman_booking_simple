from odoo import models, fields, api

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

    @api.depends('partner_id')
    def _compute_partner_details(self):
        for record in self:
            record.name = record.partner_id.name if record.partner_id else ''
            record.mobile = record.partner_id.mobile if record.partner_id else ''

    @api.model
    def create(self, vals):
        # Custom logic before creating the record
        if 'description' in vals and not vals['description']:
            vals['description'] = 'No description provided.'
        
        # Call the super method to create the record
        record = super(DarmanBooking, self).create(vals)
        
        # Custom logic after creating the record
        # Example: Log a message
        record.message_post(body="Booking record created successfully.")
        
        return record