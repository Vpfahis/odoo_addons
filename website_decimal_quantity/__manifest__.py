# -*- coding: utf-8 -*-
{
    'name': 'Website Decimal Quantity',
    'version': '18.0.1.0.0',
    'category': 'My Category',
    'description': """The module enables users to select quantities in decimal 
                    values for products in Website.""",
    'author': 'Fahis',
    'depends': ['website_sale'],
    'data': [
        'views/shop_decimal_quantity_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_decimal_quantity/static/src/js/website_sale.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
