{
    'name': 'Beauty Salon Management',
    'version': '17.0.1.0.0',
    'summary': 'Manage beauty salon, appointments, clients and services',
    'description': """
Beauty Salon Management
=======================
This module allows you to manage your beauty salon business.
Main features:
- Master schedule management
- Client appointments
- Service catalog
- Reminders for recurring services
- Reports on master workload and services provided
- Bonus calculation
    """,
    'category': 'Services/Beauty',
    'author': 'Movliaiko Vitalii',
    'website': 'https://github.com/vetalo555/odoo',
    'license': 'OPL-1',
    'depends': [
        'base',
        'mail',
        'product',

    ],

    'external_dependencies': {
        'python': [],
    },
    'data': [
        # Security
        # 'security/beauty_salon_security.xml',
        'security/ir.model.access.csv',
        #
        # # Data
        # 'data/beauty_salon_data.xml',
        #
        # # Views
        'views/beauty_salon_menu.xml',
        'views/beauty_salon_master.xml',
        'views/beauty_salon_client.xml',
        'views/beauty_salon_service.xml',
        'views/beauty_salon_appointment.xml',
        'views/beauty_salon_appointment_line.xml',
        'views/beauty_salon_reminder.xml',
        'wizard/beauty_salon_set_master.xml'

        #
        # # Wizards
        # 'wizards/appointment_wizard_views.xml',
        #
        # # Reports
        # 'report/master_workload_report_template.xml',
    ],
    'demo': [
        'data/demo_master_client_service.xml',
        'data/demo_appoitment.xml',
        'data/demo_reminder.xml',
    ],
    'images': [
        # 'static/description/banner.png',
    ],
    'installable': True,
    # 'application': True,
    'auto_install': False,
}
