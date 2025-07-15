# -*- coding: utf-8 -*-
{
    'name': "Payment Provider: Cash on Delivery",
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "A payment provider for cash on delivery throughout India.",
    'description': " ",
    'depends': ['base', 'payment', 'account', 'website', 'website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/cash_on_delivery_data.xml',
        'views/payment_provider_views.xml',
        'views/website_total_form.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'cod_payment/static/src/js/pay_now.js',
        ],
        'web.assets_qweb': [
            'cod_payment/static/src/views/templates.xml',
        ],
    },
    'license': 'LGPL-3',
    'auto_install': False,
    'installable': True,
}
