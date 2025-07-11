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
    # 'assets': {
    #     'web.assets_backend': [
    #         # Path ke file JavaScript kustom Anda
    #         'inspection/static/src/js/field_binary_camera_image.js',
    #         # Path ke file XML template QWeb kustom Anda
    #         'inspection/static/src/xml/field_binary_camera_image.xml',
    #         # Jika Anda punya CSS kustom, tambahkan di sini juga
    #         # 'my_inspection_module/static/src/css/custom_styles.scss', 
    #     ],
    # },
    'application': True,
    'author': "A.M. Fathan",
    'license': 'AGPL-3',
}