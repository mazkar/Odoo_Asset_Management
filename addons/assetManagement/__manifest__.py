{
    'name': "Asset Management",
    'version': '1.0',
    'summary': 'Aset Bulanan dan Kondisi',
    'author': 'Your Name',
    'category': 'Assets',
    'depends': ['base','mail'],
    'data': [
        'views/user_group_views.xml',
        'security/asset_model_records.xml',  # Contains ir.model records
        'security/ir.model.access.csv',      # Access rights (if you have them)
        'views/asset_item_views.xml',        # Views for asset.item
        'views/asset_condition_month_views.xml', # Views for asset.condition.month
        'views/menu.xml',                    # Menu items
    ],
    'application': True,
}