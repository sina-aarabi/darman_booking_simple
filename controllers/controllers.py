# -*- coding: utf-8 -*-
# from odoo import http


# class DarmanBookingSimple(http.Controller):
#     @http.route('/darman_booking_simple/darman_booking_simple', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/darman_booking_simple/darman_booking_simple/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('darman_booking_simple.listing', {
#             'root': '/darman_booking_simple/darman_booking_simple',
#             'objects': http.request.env['darman_booking_simple.darman_booking_simple'].search([]),
#         })

#     @http.route('/darman_booking_simple/darman_booking_simple/objects/<model("darman_booking_simple.darman_booking_simple"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('darman_booking_simple.object', {
#             'object': obj
#         })

