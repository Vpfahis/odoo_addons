# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "hostel_pos_quantity",
    'version': '1.0',
    'depends': ['base', 'point_of_sale'],
    'author': "Fahis",
    'category': 'My Category',
    'sequence': '4',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'views/quantity_location.xml',
        

    ],
    'assets': {

        'point_of_sale._assets_pos': [
            'hostel_pos_quantity/static/src/xml/product_quantity.xml',


        ]

    },

    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
