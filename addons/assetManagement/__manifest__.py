{
    'name': "Asset Management",
    'version': '1.0',
    'summary': 'Aset Bulanan dan Kondisi',
    'author': 'Your Name',
    'category': 'Assets',
    'depends': ['base','mail','stock'],
    'data': [
        'views/asset_menu_views.xml',
        'views/asset_condition_month_line_views.xml',
        'views/menu.xml',    
        'views/user_group_views.xml',
        'data/module_category.xml',
        'data/approval_group_and_route.xml',
        'security/asset_model_records.xml',  # Contains ir.model records
        'security/ir.model.access.csv',      # Access rights (if you have them)
        'views/asset_item_views.xml',        # Views for asset.item
        'views/asset_condition_month_views.xml', # Views for asset.condition.month
                       # Menu items
    ],
    'application': True,
}