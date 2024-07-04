{
    'name': 'Hospital',
    'author': 'Ardaza',
    'version': "1.0.1",
    'website': 'www.Ardaza.com',
    'summary': 'Odoo testing module',
    'depends': ['mail'], 

    'data':[
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/menu.xml',
        'views/patient.xml',
        'views/doctor.xml',
    ]
}