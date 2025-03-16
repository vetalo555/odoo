{
    'name': 'Автоматизація лікарні2',
    'version': '17.0.1.0.0',
    'author': 'Movliaiko Vitalii',
    'website': 'https://github.com/vetalo555/odoo',
    'category': 'Customizations',
    'license': 'OPL-1',
    'depends': ['base'],
    'external_dependencies': {
        'python': [],
    },
    'data': ['security/ir.model.access.csv',
            'views/hr_hospital_doctor.xml',
             'views/hr_hospital_menu.xml'


             ],
   # 'demo': ['demo/demo_data.xml'],
    'installable': True,
    'auto_install': False,
    'images': [
        'static/description/logo.png'
    ],



}