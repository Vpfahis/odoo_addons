{
    'name': "School",
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
        'views/school_students.xml',
        'views/school_faculty.xml',
        'views/school_class.xml',
        'views/school_subject.xml',
        'views/school_menuitem.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
