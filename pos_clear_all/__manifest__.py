{
    'name': "POS Clear all",
    'version': '18.0.1.0.0',
    'depends': ['base','web','point_of_sale','sale'],
    'author': "Fahis",
    'category': 'My Category',
    'description': """
    A module to add clear all button to POS order
    """,
    'assets': {
            'point_of_sale._assets_pos': [
                '/pos_clear_all/static/src/js/clear_order_button.js',
                '/pos_clear_all/static/src/xml/clear_order_button.xml',
                '/pos_clear_all/static/src/js/orderline_remove_button.js',
                '/pos_clear_all/static/src/xml/orderline_remove_button.xml',
            ],
    },
    'installable': True,
    'auto_install': False,
}