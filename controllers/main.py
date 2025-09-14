from odoo.addons.website.controllers.form import WebsiteForm
from odoo.http import request

class CustomWebsiteForm(WebsiteForm):

    def extract_data(self, model, values):
        partner = None
        if model.sudo().model == 'darman.booking':
            # Pop the fields since they are only useful to generate or update a partner record
            partner_name = values.pop('name', None)
            partner_phone = values.pop('mobile', None)
            partner_type = values.pop('partner_type', None)

            if partner_name or partner_phone:
                # Find existing partner by mobile
                partner = request.env['res.partner'].sudo().search([('mobile', '=', partner_phone)], limit=1)
                if partner:
                    # Update existing partner with provided data (if different and not empty)
                    update_vals = {}
                    if partner_name and partner_name.strip() and partner_name != partner.name:
                        update_vals['name'] = partner_name.strip()
                    if partner_type and getattr(partner, 'partner_type', None) != partner_type:
                        update_vals['partner_type'] = partner_type
                    if update_vals:
                        partner.sudo().write(update_vals)
                else:
                    # Create a new partner if none found
                    partner = request.env['res.partner'].sudo().create({
                        'name': (partner_name or partner_phone or 'Portal Guest'),
                        'mobile': partner_phone,
                        'partner_type': partner_type,
                    })

        data = super().extract_data(model, values)
        if partner:
            data['record']['partner_id'] = partner.id
        return data