{
    'name': "Inspeksi Kebersihan",
    'depends' :[
        'base','stock', 'mail','hr',
    ],
    'data':[
        'data/inspection_sequence.xml',
        'views/inspection_wizard_views.xml',
        'views/inspection_view.xml',
        'views/task_master_view.xml',
        'views/inspection_menus.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'author': "A.M. Fathan",
    'license': 'AGPL-3',
}