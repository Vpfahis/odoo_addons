# -*- coding: utf-8 -*-
{
    'name': "Payment Provider: Cash on Delivery",
    'version': '18.0.1.0.0',
    'category': 'My Category',
    'sequence': 350,
    'summary': "A payment provider for cash on delivery.",
    'description': "A payment provider for COD",
    'depends': ['base', 'payment', 'account', 'website', 'website_sale'],
    'data': [
        'data/cash_on_delivery_data.xml',
        'views/payment_provider_views.xml',
        'views/payment_method_views.xml',
        'views/website_total_form.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'payment_cash_on_delivery/static/src/js/pay_now.js',
        ],
    },
    'license': 'LGPL-3',
    'auto_install': False,
    'installable': True,
}