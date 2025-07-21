{
    'name': "Hostel",
    'version': '18.0.1.0.0',
    'depends': ['base','web','mail','product','sale','website'],
    'author': "Cybrosys",
    'category': 'My Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/hostel_security.xml',
        'security/ir.model.access.csv',
        'report/report_templates.xml',
        'report/report_action.xml',
        'data/ir_sequence_data.xml',
        'data/hostel_facility_data.xml',
        'data/hostel_product_demo.xml',
        'data/ir_cron_data.xml',
        # 'data/automated_action.xml',
        'wizard/student_report_wizard_views.xml',
        'wizard/leave_report_wizard_views.xml',
        'views/hostel_room_view.xml',
        'views/hostel_student_view.xml',
        'views/hostel_facility_view.xml',
        'views/hostel_student_leave_view.xml',
        'views/hostel_account_move_view.xml',
        'views/hostel_cleaning_service_view.xml',
        'views/hostel_menu.xml',
        'views/website_form.xml',
        'views/snippets/room_snippet_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hostel/static/src/js/action_manager.js',
        ],
        'web.assets_frontend': [
            '/hostel/static/src/xml/room_snippet_content.xml',
            '/hostel/static/src/js/room_snippet.js',
        ],
    },

    'installable': True,
    'auto_install': True,
    'application': True,
}
