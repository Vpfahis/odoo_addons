{
    'name': "Estate",
    'version': '18.0.1.0.0',
    'depends': ['base','web'],
    'author': "Fahis",
    'category': 'My Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/mymodule_view.xml',
        'views/mymodule_menu.xml',
        'views/property_type.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
