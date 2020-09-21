# -*- coding: utf-8 -*-
# from odoo import http


# class BluitImportarProductosVentas(http.Controller):
#     @http.route('/bluit_importar_productos_ventas/bluit_importar_productos_ventas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bluit_importar_productos_ventas/bluit_importar_productos_ventas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bluit_importar_productos_ventas.listing', {
#             'root': '/bluit_importar_productos_ventas/bluit_importar_productos_ventas',
#             'objects': http.request.env['bluit_importar_productos_ventas.bluit_importar_productos_ventas'].search([]),
#         })

#     @http.route('/bluit_importar_productos_ventas/bluit_importar_productos_ventas/objects/<model("bluit_importar_productos_ventas.bluit_importar_productos_ventas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bluit_importar_productos_ventas.object', {
#             'object': obj
#         })
