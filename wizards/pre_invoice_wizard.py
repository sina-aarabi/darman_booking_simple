from odoo import models, fields, api
import json

class PreInvoiceWizard(models.TransientModel):
    _name = 'daarman.pre.invoice.wizard'
    _description = 'Pre Invoice Wizard'

    # Service response fields
    reference_number = fields.Char('Reference Number', readonly=True)
    bill_number = fields.Char('Bill Number', readonly=True)
    payment_bill_number = fields.Char('Payment Bill Number', readonly=True)
    total_amount = fields.Float('Total Amount', readonly=True)
    discont = fields.Float('Discount', readonly=True)
    payable_amount = fields.Float('Payable Amount', readonly=True)
    vat = fields.Float('VAT', readonly=True)
    business_name = fields.Char('Business Name', readonly=True)

    # Invoice Items
    invoice_line_ids = fields.One2many('daarman.pre.invoice.line.wizard', 'wizard_id', string='Invoice Lines')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        context = self.env.context
        if context.get('pre_invoice_response'):
            result = context['pre_invoice_response']['result']
            result = json.loads(result)
            
            if result and isinstance(result, dict):
                invoice_data = result.get('result', {})
                
                res.update({
                    'reference_number': invoice_data.get('referenceNumber'),
                    'bill_number': invoice_data.get('billNumber'),
                    'payment_bill_number': invoice_data.get('paymentBillNumber'),
                    'total_amount': invoice_data.get('totalAmountWithoutDiscount'),
                    'payable_amount': invoice_data.get('payableAmount'),
                    'discont': invoice_data.get('totalAmountWithoutDiscount') - invoice_data.get('payableAmount'),
                    'vat': invoice_data.get('vat'),
                    'business_name': invoice_data.get('business', {}).get('name'),
                })

                # Process invoice items
                invoice_lines = []
                for item in invoice_data.get('invoiceItemSrvs', []):
                    product = item.get('productShortSrv', {})
                    line_vals = {
                        'product_id': product.get('id'),
                        'name': product.get('name'),
                        'description': product.get('description'),
                        'quantity': item.get('quantity'),
                        'price': product.get('price'),
                        'discount': item.get('discount', 0.0),
                        'amount': item.get('amount'),
                    }
                    invoice_lines.append((0, 0, line_vals))
                
                res['invoice_line_ids'] = invoice_lines

        return res

    def action_confirm(self):
        """Confirm and send the actual invoice"""
        
        context = self.env.context
        booking_id = context.get('booking_id')
        booking = self.env['darman.booking'].browse(booking_id) if booking_id else None
        if booking:
            booking.action_send_invoice_final()
        return {'type': 'ir.actions.act_window_close'}

