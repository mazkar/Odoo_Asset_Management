def pre_init_hook(cr):
    cr.execute("DELETE FROM stock_warehouse WHERE code = 'WH' AND company_id = 1;")
