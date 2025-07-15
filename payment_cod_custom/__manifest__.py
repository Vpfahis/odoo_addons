{
    'name': 'Custom COD Payment Provider',
    'version': '1.0',
    'depends': ['payment', 'website_sale', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_provider_cod_view.xml',
        # 'views/website_cart_template.xml',
        'data/payment_provider_cod_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'payment_cod_custom/static/src/js/payment_form.js',
        ],
    },
    'installable': True,
    'application': False,
}
