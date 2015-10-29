import generate_pricelist_csv as csv_generate 

def sheet_3_price(file,product_values, worksheet, region_values,pricelist_name):
    data_lst = []
    for main_k,main_v in product_values.iteritems():
        res_base = {
               'RHT': {'Standing Charge pence per day':False,'Primary Unit Rate kwh': False},
               }
        res = {main_k:res_base}
        for k,v in main_v.iteritems():
            for sub_k,sub_v in v.iteritems():
                rowValues = worksheet.row_values(sub_v)
                dictionary = dict(zip(region_values, rowValues))
                res[main_k][k].update({sub_k:dictionary})
        data_lst.append(res)
    csv_lst = csv_generate.generate_csv_rht(file,data_lst,pricelist_name)
    return csv_lst

