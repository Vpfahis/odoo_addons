{
    'name': "Sale Order Approval",
    'version': '18.0.1.0.0',
    'depends': ['base','sale'],
    'author': "Fahis",
    'category': 'My Category',
    'description': """
    A module to approve the Sale Order if its above 25K
    """,
    # data files always loaded at installation
    'data': [
        'views/res_config_settings_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'licence' : 'LGPL-3',
}
