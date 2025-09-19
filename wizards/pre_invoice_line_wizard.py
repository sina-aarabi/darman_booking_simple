from odoo import models, fields

class PreInvoiceLineWizard(models.TransientModel):
    _name = 'daarman.pre.invoice.line.wizard'
    _description = 'Pre Invoice Line Wizard'

    wizard_id = fields.Many2one('daarman.pre.invoice.wizard', string='Wizard')
    product_id = fields.Integer('Product ID')
    name = fields.Char('Product Name')
    description = fields.Text('Description')
    quantity = fields.Integer('Quantity')
    price = fields.Float('Price')
    amount = fields.Float('Amount')
    discount = fields.Float('Discount')