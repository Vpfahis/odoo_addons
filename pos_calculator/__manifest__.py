{
    'name': "POS Calculator",
    'version': '18.0.1.0.0',
    'depends': ['base','web','point_of_sale'],
    'author': "FahisVP",
    'category': 'My Category',
    'description': """
    A module to add calculator to the POS screen
    """,
    'data': [
        'views/pos_config_views.xml',
    ],
    'assets': {
            'point_of_sale._assets_pos': [
                'pos_calculator/static/src/js/calculator_widget.js',
                'pos_calculator/static/src/xml/calculator_widget.xml',
                'pos_calculator/static/src/css/calculator_widget.css',
            ],
        },
    'installable': True,
    'auto_install': False,
    'application': False,
    'licence' : 'LGPL-3',
}