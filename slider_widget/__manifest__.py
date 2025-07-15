{
    'name': "Slider Widget",
    'version': '18.0.1.0.0',
    'depends': ['base','product'],
    'author': "Fahis",
    'category': 'My Category',
    'description': """
    A module to add the slider widget to choose the integer value
    """,
    'data': [
        'views/product_product.xml',
    ],
    'assets':{
        'web.assets_backend': [
            'slider_widget/static/src/js/custom_slider_widget.js',
            'slider_widget/static/src/xml/custom_slider_widget.xml'
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'licence' : 'LGPL-3',
}
