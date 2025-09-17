from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

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
            ('invioced', 'Invoiced'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        default='draft',
        required=True,
        readonly=True,
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

    def action_accept(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Only draft bookings can be accepted'))
            rec.state = 'confirmed'
            rec.message_post(body=_('Booking accepted.'))

    def action_decline(self):
        for rec in self:
            if rec.state not in ('draft', 'confirmed'):
                raise UserError(_('Only draft or confirmed bookings can be declined'))
            rec.state = 'cancelled'
            rec.message_post(body=_('Booking declined.'))

    def action_mark_done(self):
        for rec in self:
            if rec.state != 'invioced':
                raise UserError(_('Only invoiced bookings can be marked as done'))
            rec.state = 'done'
            rec.message_post(body=_('Booking marked as done.'))

    def action_set_to_draft(self):
        for rec in self:
            if rec.state != 'cancelled':
                raise UserError(_('Only cancelled bookings can be reset to draft'))
            rec.state = 'draft'
            rec.message_post(body=_('Booking reset to draft.'))

    def action_send_invoice(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed bookings can be invoiced'))
        user = self.partner_id.user_ids and self.partner_id.user_ids[0] or None
        # Read mobile number from user (prefer user.partner mobile), fallback to booking mobile
        mobile = getattr(user, 'mobile', False) or getattr(user.partner_id, 'mobile', False) or self.mobile
        pod_user_id = getattr(user, 'pod_user_id', False)

        if not mobile:
            raise ValidationError(_('User mobile number is required to send invoice'))
        if not pod_user_id:
            raise ValidationError(_('User POD User ID (pod_user_id) is not set'))

        # Retrieve the invoice issuance service
        service = self.env.ref('daarman_api.invoice_issuance', raise_if_not_found=False)
        if not service:
            raise UserError(_('Service "invoice_issuance" not found. Update the daarman_api module.'))

        # Build request payload based on service sample structure
        request_data = {
            "apiKey": "",
            "productEntityId": "",
            "providerParameters": {
                "body": {
                    "products": [311681],
                    "quantities": [1],
                    "paymentType": "sms",
                    "Mobile": mobile,
                    "guildCode": "TOURISM_GUILD",
                    "userId": str(pod_user_id),
                },
                "Client-Id": "676ccqa26c4dd390c6dbf690c42626",
                "Access-Token": "6175279446-6d2c1e0a75324f43a3c0e0c6af07cabb.XzIwMjU1",
                "invoiceTypeUniqueId": "hotel-flight",
            },
        }

        # Send via helper method on daarman.service
        response = service.call(data=request_data)

        # Log to chatter and notify user
        ref = response.get('referenceNumber', '') if isinstance(response, dict) else ''
        message = _('Invoice issuance requested%s') % (f' (Ref: {ref})' if ref else '')
        self.message_post(body=message)
        self.state = 'invioced'

        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'display_notification',
        #     'params': {
        #         'title': _('Success'),
        #         'message': message,
        #         'type': 'success',
        #         'sticky': False,
        #     }
        # }

