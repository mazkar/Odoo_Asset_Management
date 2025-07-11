{
    'name': "Asset Management",
    'version': '1.0',
    'summary': 'Aset Bulanan dan Kondisi',
    'author': 'Your Name',
    'category': 'Assets',
    'depends': ['base','mail','stock'],
    'data': [
        'views/asset_item_import_wizard.xml',             # VIEW Wizard-nya
        'views/asset_item_views.xml',                     # Memakai action_import_asset_item
        'views/asset_condition_month_views.xml',
        'views/asset_condition_month_done_views.xml',
        'views/approval_route_line_menu.xml',
        'views/user_group_views.xml',
        'views/menu.xml',
        'data/approval_group_and_route.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'license': 'AGPL-3',
    'author': "Azka",
}