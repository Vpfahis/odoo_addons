{
    'name': "Order Line xls",
    'version': '18.0.1.0.0',
    'depends': ['base','sale'],
    'author': "Cybrosys",
    'category': 'My Category',
    'description': """
    A module to import order lines from xls sheet
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/import_xls_sale_order_view.xml',
        'wizard/import_sale_order_line_wizard_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
