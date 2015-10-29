import generate_pricelist_csv as csv_generate 

def sheet_5_price(file, product_values, worksheet, region_values,pricelist_name):
    data_lst = []
    for k_profile,v_profile in product_values.iteritems():
        res = {k_profile:{}}
        for main_k,main_v in v_profile.iteritems():
            res_base = {
               'Baserate': {'Standing Charge pence per day':False,'Primary Unit Rate kwh': False},
               'Nightsaver': {'Standing Charge pence per day':False,'Primary Unit Rate kwh': False,'Night Unit Rate kwh': False},
               }
            res[k_profile].update({main_k:res_base})
            for k,v in main_v.iteritems():
                for sub_k,sub_v in v.iteritems():
                    rowValues = worksheet.row_values(sub_v)
                    dictionary = dict(zip(region_values, rowValues))
                    res[k_profile][main_k][k].update({sub_k:dictionary})
        data_lst.append(res)
    csv_lst = csv_generate.generate_csv_5678(data_lst,pricelist_name)
    return csv_lst

