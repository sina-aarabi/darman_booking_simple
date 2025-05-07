from odoo.addons.website.controllers.form import WebsiteForm
from odoo.http import request

class CustomWebsiteForm(WebsiteForm):
    
    def extract_data(self, model, values):
        if model.sudo().model == 'darman.booking':
            # pop the fields since there are only useful to generate a candidate record
            partner_name = values.pop('name')
            partner_phone = values.pop('mobile', None)
            partner_type = values.pop('partner_type',None)
            
            partner = request.env['res.partner'].sudo().search([('mobile','=',partner_phone)],limit=1)
            if not partner:
                partner = request.env['res.partner'].sudo().create({
                    'name': partner_name,
                    'mobile': partner_phone,
                    'partner_type': partner_type
                    
                })

        data = super().extract_data(model, values)
        if partner:
            data['record']['partner_id'] = partner.id
        return data