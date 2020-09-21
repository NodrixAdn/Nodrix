# -*- coding: utf-8 -*-
{
    'name': "BLUIT importar Productos en Ventas",

    'summary': """
        Excel/CSV""",

    'description': """
        Importación de Productos en modulo de ventas por medio de archivos excel y csv
    """,

    'author': "BLUIT Software Factory",
    'website': "http://www.bluit.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/importar_productos_ventas.xml',
        'views/templates.xml',
    ],
    'installable':True,
    'auto_install':False,
    'application':True,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
