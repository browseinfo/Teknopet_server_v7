import generate_pricelist_csv as csv_generate
import import_pricelist as pricelist
import re
import xlrd
import datetime 

def sheet_1_price(file,product_values, worksheet, region_values,pricelist_name):
    data_lst = []
    for main_k,main_v in product_values.iteritems():
        res_base = {
               'Baserate': {'Standing Charge pence per day':False,'Primary Unit Rate kwh': False},
               'Nightsaver': {'Standing Charge pence per day':False,'Primary Unit Rate kwh': False,'Night Unit Rate kwh': False},
               'Flexirate 2': {'Standing Charge pence per day':False,'Primary Unit Rate kwh': False,'Evening and Weekend Unit Rate kwh': False},
               'Flexirate 3': {'Standing Charge pence per day':False,'Primary Unit Rate kwh': False,'Night Unit Rate kwh': False,'Evening and Weekend Unit Rate kwh': False},
               }
        res = {main_k:res_base}
        for k,v in main_v.iteritems():
            for sub_k,sub_v in v.iteritems():
                rowValues = worksheet.row_values(sub_v)
                dictionary = dict(zip(region_values, rowValues))
                res[main_k][k].update({sub_k:dictionary})
        data_lst.append(res)
    csv_lst = csv_generate.generate_csv_1234(file,data_lst,pricelist_name)
    return csv_lst

def sheet_1_gas_price(file,product_values, worksheet, region_values,pricelist_name):
    data_lst = []
    for main_k,main_v in product_values.iteritems():
        res_base = {'Standing Charge pence per day':False,'Primary Unit Rate kwh': False}
        res = {main_k:res_base}
        for k,v in main_v.iteritems():
            rowValues = worksheet.row_values(v)
            dictionary = dict(zip(region_values, rowValues))
            res[main_k].update({k:dictionary})
        data_lst.append(res)
    csv_lst = csv_generate.generate_csv_gas(file,data_lst,pricelist_name)
    return csv_lst

def sheet_1_cng_gas_price(file, col_values,worksheet,pricelist_name):
    data_lst = []
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    curr_row = 0
    while curr_row < num_rows:
        curr_row += 1
        row = worksheet.row(curr_row)
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
            row_values = worksheet.row_values(curr_row)
            dictionary = dict(zip(col_values, row_values))
        data_lst.append(dictionary)
    print "________data_lst___________",len(data_lst)
    csv_lst = csv_generate.generate_csv_cng_gas(file,data_lst,pricelist_name)
    return csv_lst

def sheet_1_total_gas_price(file, worksheet,pricelist_name,utility_type):
    data_lst = []
    csv_lst =[]
    product_lst = []
    if utility_type == 'Electricity':
        res = { 1: {
                       'ELECTRICITY 1 YEAR CONTRACT': [],
                       'ELECTRICITY 2 YEAR CONTRACT': [],
                       'ELECTRICITY 3 YEAR CONTRACT': [],
                       'ELECTRICITY 4 YEAR CONTRACT': [],
                       'ELECTRICITY 5 YEAR CONTRACT': [],
                       },
               2: {
                       'ELECTRICITY 1 YEAR CONTRACT': [],
                       'ELECTRICITY 2 YEAR CONTRACT': [],
                       'ELECTRICITY 3 YEAR CONTRACT': [],
                       'ELECTRICITY 4 YEAR CONTRACT': [],
                       'ELECTRICITY 5 YEAR CONTRACT': [],
                       },
               3: {
                       'ELECTRICITY 1 YEAR CONTRACT': [],
                       'ELECTRICITY 2 YEAR CONTRACT': [],
                       'ELECTRICITY 3 YEAR CONTRACT': [],
                       'ELECTRICITY 4 YEAR CONTRACT': [],
                       'ELECTRICITY 5 YEAR CONTRACT': [],
                       },
               4: {
                       'ELECTRICITY 1 YEAR CONTRACT': [],
                       'ELECTRICITY 2 YEAR CONTRACT': [],
                       'ELECTRICITY 3 YEAR CONTRACT': [],
                       'ELECTRICITY 4 YEAR CONTRACT': [],
                       'ELECTRICITY 5 YEAR CONTRACT': [],
                       },
               5: {
                       'ELECTRICITY 1 YEAR CONTRACT': [],
                       'ELECTRICITY 2 YEAR CONTRACT': [],
                       'ELECTRICITY 3 YEAR CONTRACT': [],
                       'ELECTRICITY 4 YEAR CONTRACT': [],
                       'ELECTRICITY 5 YEAR CONTRACT': [],
                       },
               6: {
                       'ELECTRICITY 1 YEAR CONTRACT': [],
                       'ELECTRICITY 2 YEAR CONTRACT': [],
                       'ELECTRICITY 3 YEAR CONTRACT': [],
                       'ELECTRICITY 4 YEAR CONTRACT': [],
                       'ELECTRICITY 5 YEAR CONTRACT': [],
                       },
               7: {
                       'ELECTRICITY 1 YEAR CONTRACT': [],
                       'ELECTRICITY 2 YEAR CONTRACT': [],
                       'ELECTRICITY 3 YEAR CONTRACT': [],
                       'ELECTRICITY 4 YEAR CONTRACT': [],
                       'ELECTRICITY 5 YEAR CONTRACT': [],
                       },
               8: {
                       'ELECTRICITY 1 YEAR CONTRACT': [],
                       'ELECTRICITY 2 YEAR CONTRACT': [],
                       'ELECTRICITY 3 YEAR CONTRACT': [],
                       'ELECTRICITY 4 YEAR CONTRACT': [],
                       'ELECTRICITY 5 YEAR CONTRACT': [],
                       },
               
               }
#         num_rows = worksheet.nrows - 1
#         num_cells = worksheet.ncols - 1
#         curr_row = 0
#         while curr_row < num_rows:
#             dictionary ={}
#             curr_row += 1
#             row = worksheet.row(curr_row)
#             curr_cell = -1
#             row_values = worksheet.row_values(curr_row)
#     #         print "________row__________",row_values
#             dictionary = dict(zip(col_values, row_values))
        for dictionary in worksheet:
            product_lst.append(dictionary.get('Product Name', False) and dictionary['Product Name'])
            mtc_lst = dictionary.get('MTC', False) and str(dictionary['MTC']).split(' ') or False
            if dictionary.get('Contract Length', False) == '12':
#                 print "______main____dictionary_____________",dictionary
                if mtc_lst:
                    for code in mtc_lst:
                        temp_dic = dictionary.copy()
                        temp_dic.update({'MTC': code})
#                         print "_________dictionary___________",dictionary
                        res[dictionary.get('Profiles', False) and int(dictionary['Profiles']) or False]['ELECTRICITY 1 YEAR CONTRACT'].append(temp_dic)
#                         print "______asdsa____________",res[dictionary.get('Profiles', False) and int(dictionary['Profiles']) or False]['ELECTRICITY 1 YEAR CONTRACT']
            elif dictionary.get('Contract Length', False) == '24':
                if mtc_lst:
                    for code in mtc_lst:
                        temp_dic = dictionary.copy()
                        temp_dic.update({'MTC': code})
                        res[dictionary.get('Profiles', False) and int(dictionary['Profiles']) or False]['ELECTRICITY 2 YEAR CONTRACT'].append(temp_dic)
            elif dictionary.get('Contract Length', False) == '36':
                if mtc_lst:
                    for code in mtc_lst:
                        temp_dic = dictionary.copy()
                        temp_dic.update({'MTC': code})
                        res[dictionary.get('Profiles', False) and int(dictionary['Profiles']) or False]['ELECTRICITY 3 YEAR CONTRACT'].append(temp_dic)
            elif dictionary.get('Contract Length', False) == '48':
                if mtc_lst:
                    for code in mtc_lst:
                        temp_dic = dictionary.copy()
                        temp_dic.update({'MTC': code})
                        res[dictionary.get('Profiles', False) and int(dictionary['Profiles']) or False]['ELECTRICITY 4 YEAR CONTRACT'].append(temp_dic)
            elif dictionary.get('Contract Length', False) == '60':
                if mtc_lst:
                    for code in mtc_lst:
                        temp_dic = dictionary.copy()
                        temp_dic.update({'MTC': code})
                        res[dictionary.get('Profiles', False) and int(dictionary['Profiles']) or False]['ELECTRICITY 5 YEAR CONTRACT'].append(temp_dic)
#         print "_________res_________________",res[3]['ELECTRICITY 1 YEAR CONTRACT']
        data_lst.append(res)
        print "_______product_lst_______________",len(product_lst),len(set(product_lst))
        csv_lst = csv_generate.generate_csv_total_ele(file,data_lst,pricelist_name)
    elif utility_type == 'Gas':
        res = {
               'GAS 1 YEAR CONTRACT': [],
               'GAS 2 YEAR CONTRACT': [],
               'GAS 3 YEAR CONTRACT': [],
               'GAS 4 YEAR CONTRACT': [],
               'GAS 5 YEAR CONTRACT': [],
               }
#         num_rows = worksheet.nrows - 1
#         num_cells = worksheet.ncols - 1
#         curr_row = 0
#         while curr_row < num_rows:
#             curr_row += 1
#             row = worksheet.row(curr_row)
#             curr_cell = -1
#             row_values = worksheet.row_values(curr_row)
#             dictionary = dict(zip(col_values, row_values))
        for dictionary in worksheet:
#             print "_________dictionary____________",dictionary
            
            product_lst.append(dictionary.get('Product Name', False) and dictionary['Product Name'])
            if dictionary.get('Contract Length (months)', False) == '12':
                res['GAS 1 YEAR CONTRACT'].append(dictionary)
            elif dictionary.get('Contract Length (months)', False) == '24':
                res['GAS 2 YEAR CONTRACT'].append(dictionary)
            elif dictionary.get('Contract Length (months)', False) == '36':
                res['GAS 3 YEAR CONTRACT'].append(dictionary)
            elif dictionary.get('Contract Length (months)', False) == '48':
                res['GAS 4 YEAR CONTRACT'].append(dictionary)
            elif dictionary.get('Contract Length (months)', False) == '60':
                res['GAS 5 YEAR CONTRACT'].append(dictionary)
        data_lst.append(res)
        print "_______product_lst_______________",len(product_lst),len(set(product_lst))
        csv_lst = csv_generate.generate_csv_total_gas(file,data_lst,pricelist_name)
    return product_lst,csv_lst



def sheet_1_easy_utility_price(file, worksheet, product_values,pricelist_name, utility_type,sheet):
    region_values = ['', u'Profile Class', u'MTC Guide', u'LLF Guide', u'Tariff Description', u'Standing Charge (p/Day)', u'Unit Rate  (p/kWh)', u'Day Rate (p/kWh)', u'Night Rate (p/kWh)', u'Weekday Rate (p/kWh)', u'Evening Weekend Rate (p/kWh)', u'Evening Weekend & Night Rate (p/kWh)', '', '']
    data_lst = []
    for k_profile,v_profile in product_values.iteritems():
#         print "____________k_profile,v_profile__________",k_profile,v_profile
        res = {k_profile:{}}
        for main_k,main_v in v_profile.iteritems():
#             print "_________main_k,main_v____________",main_k,main_v
            res_base = {
               'Baserate': {'Standing Charge (p/Day)':False,'Unit Rate  (p/kWh)': False,'Day Rate (p/kWh)':False,'Night Rate (p/kWh)':False,'Weekday Rate (p/kWh)':False,'Evening Weekend Rate (p/kWh)':False,'Evening Weekend & Night Rate (p/kWh)':False},
               'Nightsaver': {'Standing Charge (p/Day)':False,'Unit Rate  (p/kWh)': False,'Day Rate (p/kWh)':False,'Night Rate (p/kWh)':False,'Weekday Rate (p/kWh)':False,'Evening Weekend Rate (p/kWh)':False,'Evening Weekend & Night Rate (p/kWh)':False},
               'Flexirate 2': {'Standing Charge (p/Day)':False,'Unit Rate  (p/kWh)': False,'Day Rate (p/kWh)':False,'Night Rate (p/kWh)':False,'Weekday Rate (p/kWh)':False,'Evening Weekend Rate (p/kWh)':False,'Evening Weekend & Night Rate (p/kWh)':False},
               'Flexirate 3': {'Standing Charge (p/Day)':False,'Unit Rate  (p/kWh)': False,'Day Rate (p/kWh)':False,'Night Rate (p/kWh)':False,'Weekday Rate (p/kWh)':False,'Evening Weekend Rate (p/kWh)':False,'Evening Weekend & Night Rate (p/kWh)':False},
               'RHT': {'Standing Charge (p/Day)':False,'Unit Rate  (p/kWh)': False,'Day Rate (p/kWh)':False,'Night Rate (p/kWh)':False,'Weekday Rate (p/kWh)':False,'Evening Weekend Rate (p/kWh)':False,'Evening Weekend & Night Rate (p/kWh)':False},
               }
            res[k_profile].update({main_k:{}})
            for k,v in main_v.iteritems():
#                 print "___________k,v_____________",k,v
#                 region_values = worksheet.row_values(0)
#                 print "________region_values__________",region_values
                rowValues = worksheet.row_values(v)
#                 print "________rowValues__________",rowValues
                for n,i in enumerate(rowValues):
                    if i in ['Single Rate (UE7)', 'Single Rate Maximum Demand (UE7)']:
                        rowValues[n] = 'Baserate'
                    elif i == 'Evening Weekend (EW)':
                        rowValues[n] = 'Flexirate 2'
                    elif i in ['Two Rate Economy 7 (UE7)', 'Two Rate Maximum Demand (UE7)']:
                        rowValues[n] = 'Nightsaver'
                    elif i in ('Three Rate Evening Weekend (3-Rate) ', 'Multi Rate Maximum Demand (3-Rate)'):
                        rowValues[n] = 'Flexirate 3'
                    elif i == 'Off Peak (EW)':
                        rowValues[n] = 'RHT'
                dictionary = dict(zip(region_values, rowValues))
#                 print "________dictionary_____________",dictionary
                res[k_profile][main_k].update({k:dictionary})
#                 print "__________res_______________",res
#                 stop
        data_lst.append(res)
#         print "_________data_lst___________",data_lst
#     stop
    csv_lst = csv_generate.generate_csv_easy_price(file,data_lst,pricelist_name,sheet)
    return csv_lst



def sheet_1_bg_gas_price(file, col_values,worksheet,pricelist_name):
    data_lst = []
    product_lst = []
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    curr_row = 1
    while curr_row < num_rows:
#         print "_______curr_row_________",curr_row
        curr_row += 1
        row = worksheet.row(curr_row)
        curr_cell = -1
        while curr_cell < num_cells:
#             print "________curr_cell____________",curr_cell
#             print "__________col_values________",col_values
            curr_cell += 1
            row_values = worksheet.row_values(curr_row,start_colx=0, end_colx=6)
#             print "_____________row_values________",row_values
            dictionary = dict(zip(col_values, row_values))
#             print "_________dictionary____________",dictionary
#             stop
        if dictionary.get('PRICE CODE', False) and dictionary['PRICE CODE'] not in product_lst:
              product_lst.append(dictionary['PRICE CODE'])
        data_lst.append(dictionary)
#     print "________data_lst___________",len(data_lst)
#     print "________product_lst___________",len(product_lst)
#     stop
    csv_lst = csv_generate.generate_csv_bg_gas(file,data_lst,pricelist_name)
    return csv_lst,product_lst



def sheet_1_bg_ele_price(file, col_values,worksheet,pricelist_name,product_values,min,max):
    data_lst = []
    product_lst = []
    res = {
                          'ELECTRICITY 1 YEAR CONTRACT': [],
                          'ELECTRICITY 2 YEAR CONTRACT': [],
                          'ELECTRICITY 3 YEAR CONTRACT': []
                          }
    for k,v in product_values.iteritems():
        print "_______kv_______________",k,v
        start_col = v.get('start_col', False) and v['start_col'] or 0
        end_col = v.get('end_col', False) and v['end_col'] or 0
        print "_______start_col,end_col__________",start_col,end_col
        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1
        curr_row = 1
        while curr_row < num_rows:
    #         print "_______curr_row_________",curr_row
            curr_row += 1
            row = worksheet.row(curr_row)
            curr_cell = -1
            while curr_cell < num_cells:
    #             print "________curr_cell____________",curr_cell
    #             print "__________col_values________",col_values
                curr_cell += 1
                row_values = worksheet.row_values(curr_row,start_colx=start_col, end_colx=end_col)
#                 print "_____________row_values________",row_values
                dictionary = dict(zip(col_values, row_values))
#                 print "_________dictionary____________",dictionary
#                 stop
            if dictionary.get('Tariff', False) and dictionary['Tariff'] not in product_lst:
                  product_lst.append(dictionary['Tariff'])
#             print "_________dictionary_____________",type(dictionary['Profile Class']),dictionary
            profile = re.sub(" ", "", dictionary.get('Profile Class', False) and str(dictionary['Profile Class']) or '')
#             print "________profile__________",profile
            if len(profile) > 1:
                profile_lst = profile.split('&')
                if profile_lst:
                    for pro in profile_lst:
                        new_dic = dictionary.copy()
                        new_dic.update({'Profile Class': pro})
                        res[k].append(new_dic)
            else:
                dictionary.update({'Profile Class': profile})
                res[k].append(dictionary)
    print "________product_lst___________",len(product_lst)
#     stop
    csv_lst = csv_generate.generate_csv_bg_ele(file,res,pricelist_name,min,max)
    return csv_lst,product_lst



def sheet_1_opus_price(file, worksheet, product_values,pricelist_name, utility_type,sheet):
    region_values = ['','', u'Profile Class', u'MTC Guide', u'LLF Guide', u'Tariff Code', 'Tariff Description', u'Standing Charge (p/Day)', u'Unit Rate  (p/kWh)', u'Day Rate (p/kWh)', u'Night Rate (p/kWh)', u'Weekday Rate (p/kWh)', u'Evening Weekend Rate (p/kWh)', u'Evening Weekend & Night Rate (p/kWh)', 'Winter Day Rate (p/kWH)', 'All Other Times Rate (p/kWH)']
    data_lst = []
    for k_profile,v_profile in product_values.iteritems():
#         print "____________k_profile,v_profile__________",k_profile,v_profile
        res = {k_profile:{}}
        for main_k,main_v in v_profile.iteritems():
#             print "_________main_k,main_v____________",main_k,main_v
            res_base = {
               'Baserate': {'Standing Charge (p/Day)':False,'Unit Rate  (p/kWh)': False,'Day Rate (p/kWh)':False,'Night Rate (p/kWh)':False,'Weekday Rate (p/kWh)':False,'Evening Weekend Rate (p/kWh)':False,'Evening Weekend & Night Rate (p/kWh)':False,'Winter Day Rate (p/kWH)': False, 'All Other Times Rate (p/kWH)': False},
               'extra': {'Standing Charge (p/Day)':False,'Unit Rate  (p/kWh)': False,'Day Rate (p/kWh)':False,'Night Rate (p/kWh)':False,'Weekday Rate (p/kWh)':False,'Evening Weekend Rate (p/kWh)':False,'Evening Weekend & Night Rate (p/kWh)':False,'Winter Day Rate (p/kWH)': False, 'All Other Times Rate (p/kWH)': False},
               'Nightsaver': {'Standing Charge (p/Day)':False,'Unit Rate  (p/kWh)': False,'Day Rate (p/kWh)':False,'Night Rate (p/kWh)':False,'Weekday Rate (p/kWh)':False,'Evening Weekend Rate (p/kWh)':False,'Evening Weekend & Night Rate (p/kWh)':False,'Winter Day Rate (p/kWH)': False, 'All Other Times Rate (p/kWH)': False},
               'Flexirate 2': {'Standing Charge (p/Day)':False,'Unit Rate  (p/kWh)': False,'Day Rate (p/kWh)':False,'Night Rate (p/kWh)':False,'Weekday Rate (p/kWh)':False,'Evening Weekend Rate (p/kWh)':False,'Evening Weekend & Night Rate (p/kWh)':False,'Winter Day Rate (p/kWH)': False, 'All Other Times Rate (p/kWH)': False},
               'Flexirate 3': {'Standing Charge (p/Day)':False,'Unit Rate  (p/kWh)': False,'Day Rate (p/kWh)':False,'Night Rate (p/kWh)':False,'Weekday Rate (p/kWh)':False,'Evening Weekend Rate (p/kWh)':False,'Evening Weekend & Night Rate (p/kWh)':False,'Winter Day Rate (p/kWH)': False, 'All Other Times Rate (p/kWH)': False},
               'RHT': {'Standing Charge (p/Day)':False,'Unit Rate  (p/kWh)': False,'Day Rate (p/kWh)':False,'Night Rate (p/kWh)':False,'Weekday Rate (p/kWh)':False,'Evening Weekend Rate (p/kWh)':False,'Evening Weekend & Night Rate (p/kWh)':False,'Winter Day Rate (p/kWH)': False, 'All Other Times Rate (p/kWH)': False},
               }
            res[k_profile].update({main_k:{}})
            for k,v in main_v.iteritems():
#                 print "___________k,v_____________",k,v
#                 region_values = worksheet.row_values(0)
#                 print "________region_values__________",region_values
                rowValues = worksheet.row_values(v)
                temp_rowvalues = worksheet.row_values(v)
                for n,i in enumerate(rowValues):
                    if i in ['Single Rate Domestic Unrestricted', 'Single Rate Non Domestic','Single Rate Maximum Demand','Catering Tariff']:
                        rowValues[n] = 'Baserate'
                    elif i == 'Evening Weekend Non Domestic':
                        rowValues[n] = 'Flexirate 2'
                    elif i in ['Two Rate Domestic Economy 7', 'Two Rate Economy 7 Non Domestic','Two Rate Maximum Demand','12 Hour Night and Day']:
                        rowValues[n] = 'Nightsaver'
                    elif i in ('Three Rate Evening Weekend Non Domestic', 'Multi Rate Maximum Demand'):
                        rowValues[n] = 'Flexirate 3'
                    elif i == ['Domestic Off Peak','Non Domestic Off Peak']:
                        rowValues[n] = 'RHT'
#                 print "________rowValues__________",rowValues
#                 print "________temp_rowvalues__________",temp_rowvalues
                dictionary = dict(zip(region_values, rowValues))
                if k == 'extra' and v == 23:
                    if u'12 Hour Night and Day' in temp_rowvalues:
                        dictionary.update({'ns': True})
                    if u'Catering Tariff' in temp_rowvalues:
                        dictionary.update({'bs': True})
#                 print "________dictionary_____________",dictionary
#                 stop
                res[k_profile][main_k].update({k:dictionary})
#                 print "__________res_______________",res
    data_lst.append(res)
#     print "_________data_lst___________",data_lst
#     stop
    csv_lst = csv_generate.generate_csv_opus_price(file,data_lst,pricelist_name,sheet)
    return csv_lst


def sheet_1_opus_gas_price(file, col_values,worksheet,pricelist_name,product_values,sheet):
    data_lst = []
    product_lst = []
    res = {
                          'GAS 1 CONTRACT': [],
                          'GAS 2 CONTRACT': [],
                          'GAS 3 CONTRACT': []
                          }
    for k,v in product_values.iteritems():
        print "_______kv_______________",k,v
        start_col = v.get('start_col', False) and v['start_col'] or 0
        end_col = v.get('end_col', False) and v['end_col'] or 0
        min = v.get('min', False) and v['min'] or 0.0
        max = v.get('max', False) and v['max'] or 0.0
        print "_______start_col,end_col__________",start_col,end_col
        num_rows = 18
        num_cells = worksheet.ncols - 1
        curr_row = 5
        while curr_row < num_rows:
    #         print "_______curr_row_________",curr_row
            curr_row += 1
            row = worksheet.row(curr_row)
            curr_cell = -1
            while curr_cell < num_cells:
    #             print "________curr_cell____________",curr_cell
    #             print "__________col_values________",col_values
                curr_cell += 1
                row_values = worksheet.row_values(curr_row,start_colx=start_col, end_colx=end_col)
#                 print "_____________row_values________",row_values
                dictionary = dict(zip(col_values, row_values))
#                 print "_________dictionary____________",dictionary
#                 stop
            if dictionary.get('Tariff Code', False) and dictionary['Tariff Code'] not in product_lst:
                  product_lst.append(dictionary['Tariff Code'])
            dictionary.update({'min': min,'max': max})
            res[k].append(dictionary)
    print "________product_lst___________",len(product_lst)
#     print "___________res________________",res
#     stop
    csv_lst = csv_generate.generate_csv_opus_gas(file,res,pricelist_name,sheet)
    return csv_lst,product_lst



def sheet_1_sse_gas_price(file, col_values,worksheet,pricelist_name,utility_type,rb):
    data_lst = []
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    curr_row = 0
    while curr_row < num_rows:
        curr_row += 1
        row = worksheet.row(curr_row)
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
            row_values = worksheet.row_values(curr_row)
            dictionary = dict(zip(col_values, row_values))
#         print "_____dictionary_________",dictionary
#         stop
        pro_start_date = (datetime.datetime(*xlrd.xldate_as_tuple(dictionary['ProposedStartDate'], rb.datemode))).strftime('%Y-%m-%d')
        pro_end_date = (datetime.datetime(*xlrd.xldate_as_tuple(dictionary['ProposedEndDate'], rb.datemode))).strftime('%Y-%m-%d')
        dictionary.update({'ProposedStartDate': pro_start_date, 'ProposedEndDate': pro_end_date, 'MatrixID': str(dictionary['MatrixID'])})
        data_lst.append(dictionary)
    print "________data_lst___________",len(data_lst)
    csv_lst = csv_generate.generate_csv_sse_gas(file,data_lst,pricelist_name,utility_type)
    return csv_lst




def sheet_1_ovo_price(file,product_values, worksheet,region_values,pricelist_name,sheet):
    data_lst = []
    res ={}
    if sheet == 0:
        res_base = {'Baserate':{
                                      '1 year Electricity' : [],
                                      '2 year Electricity' : [],
                                                              
                                    },}
        for main_k, main_v in product_values.iteritems():
            for sub_k,sub_v in main_v.iteritems():
                for list_line in sub_v:
                    rowValues = worksheet.row_values(list_line)
                    dictionary = dict(zip(region_values, rowValues))
                    res_base[main_k][sub_k].append(dictionary)
        csv_lst = csv_generate.generate_csv_ovo_baserate(file,res_base,pricelist_name,sheet)
    elif sheet == 1:
        res_night = {'Nightsaver':{
                                      '1 year Electricity' : [],
                                      '2 year Electricity' : [],
                                                              
                                    },}
        for main_k, main_v in product_values.iteritems():
            for sub_k,sub_v in main_v.iteritems():
                for list_line in sub_v:
                    rowValues = worksheet.row_values(list_line)
                    dictionary = dict(zip(region_values, rowValues))
                    res_night[main_k][sub_k].append(dictionary)
        csv_lst = csv_generate.generate_csv_ovo_baserate(file,res_night,pricelist_name,sheet)
    return csv_lst       
