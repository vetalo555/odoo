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
             'views/hr_hospital_menu.xml',
             'wizard/hr_hospital_disease_report_wizard.xml',
             'views/hr_hospital_doctor.xml',
             'views/hr_hospital_patient.xml',
             'views/hr_hospital_visits.xml',
             'views/hr_hospital_disease.xml',
             'views/hr_hospital_diagnosis.xml',
             'wizard/hr_hospital_personal_doctor_wizard_view.xml',
             'report/hr_hospital_report.xml',

             ],
    'demo': ['demo/hr_hospital_demo.xml'],
    'installable': True,
    'auto_install': False,
    'images': [
        'static/description/icon.png'
    ],

}
