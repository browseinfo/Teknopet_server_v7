import csv
import tempfile
import addons
import time
import re

def generate_csv_1234(file,data,pricelist_name):
    csv_lst =[]
    for list in data:
        for l_k,l_v in list.iteritems():
            f1 = open (file,"r") # open input file for reading
            filename = ("/tmp/PRICELIST_%s.csv")%(l_k)
            print "_________filename____________",filename
            csv_lst.append(filename)
            with open(filename, 'w') as f: # output csv file
                writer = csv.writer(f, delimiter=',')
                with open(file,'r') as csvfile: # input csv file
                    reader = csv.reader(csvfile, delimiter=',')
                    for row in reader:
                        if row[1] != 'product_id' and row[3] != 'region_id':
                            row[5] = l_v[row[1]] and l_v[row[1]].get('Standing Charge pence per day', False) and l_v[row[1]]['Standing Charge pence per day'][float(row[3])] or 0.0
                            row[6] = l_v[row[1]] and l_v[row[1]].get('Primary Unit Rate kwh', False) and l_v[row[1]]['Primary Unit Rate kwh'][float(row[3])] or 0.0
                            row[7] = l_v[row[1]] and l_v[row[1]].get('Night Unit Rate kwh', False) and l_v[row[1]]['Night Unit Rate kwh'][float(row[3])] or 0.0
                            row[8] = l_v[row[1]] and l_v[row[1]].get('Evening and Weekend Unit Rate kwh', False) and l_v[row[1]]['Evening and Weekend Unit Rate kwh'][float(row[3])] or 0.0
                            row[9] = pricelist_name[l_k]
                            writer.writerow(row)
                        else:
                            writer.writerow(row)
                          
        f1.close()
    return csv_lst

def generate_csv_gas(file,data,pricelist_name):
    csv_lst =[]
    for list in data:
        for l_k,l_v in list.iteritems():
            f1 = open (file,"r") # open input file for reading
            filename = ("/tmp/PRICELIST_%s.csv")%(l_k)
            print "_________filename____________",filename
            csv_lst.append(filename)
            with open(filename, 'w') as f: # output csv file
                writer = csv.writer(f, delimiter=',')
                with open(file,'r') as csvfile: # input csv file
                    reader = csv.reader(csvfile, delimiter=',')
                    for row in reader:
                        if row[1] != 'product_id' and row[0] != 'region_id':
                            row[2] = l_v.get('Standing Charge pence per day', False) and l_v['Standing Charge pence per day'][float(row[0])] or 0.0
                            row[3] = l_v.get('Primary Unit Rate kwh', False) and l_v['Primary Unit Rate kwh'][float(row[0])] or 0.0
                            row[4] = pricelist_name[l_k]
                            writer.writerow(row)
                        else:
                            writer.writerow(row)
                          
        f1.close()
    return csv_lst

def generate_csv_5678(data,pricelist_name):
    csv_lst = []
    for list in data:
        for k_profile,v_profile in list.iteritems():
            if k_profile == '5':
                file = addons.get_module_resource('import_xls/csv_data', 'master_csv_5.csv')
            elif k_profile == '6':
                file = addons.get_module_resource('import_xls/csv_data', 'master_csv_6.csv')
            elif k_profile == '7':
                file = addons.get_module_resource('import_xls/csv_data', 'master_csv_7.csv')
            elif k_profile == '8':
                file = addons.get_module_resource('import_xls/csv_data', 'master_csv_8.csv')
            for l_k,l_v in v_profile.iteritems():
                f1 = open (file,"r") # open input file for reading
                filename = ("/tmp/PRICELIST_%s_%s.csv")%(l_k,k_profile)
                print "_________filename____________",filename
                csv_lst.append(filename)
                with open(filename, 'w') as f: # output csv file
                    writer = csv.writer(f, delimiter=',')
                    with open(file,'r') as csvfile: # input csv file
                        reader = csv.reader(csvfile, delimiter=',')
                        for row in reader:
                            if row[1] != 'product_id' and row[3] != 'region_id':
                                row[5] = l_v[row[1]] and l_v[row[1]].get('Standing Charge pence per day', False) and l_v[row[1]]['Standing Charge pence per day'][float(row[3])] or 0.0
                                row[6] = l_v[row[1]] and l_v[row[1]].get('Primary Unit Rate kwh', False) and l_v[row[1]]['Primary Unit Rate kwh'][float(row[3])] or 0.0
                                row[7] = l_v[row[1]] and l_v[row[1]].get('Night Unit Rate kwh', False) and l_v[row[1]]['Night Unit Rate kwh'][float(row[3])] or 0.0
                                row[8] = l_v[row[1]] and l_v[row[1]].get('Evening and Weekend Unit Rate kwh', False) and l_v[row[1]]['Evening and Weekend Unit Rate kwh'][float(row[3])] or 0.0
                                row[9] = pricelist_name[l_k]
                                writer.writerow(row)
                            else:
                                writer.writerow(row)
                             
            f1.close()
    return csv_lst

def generate_csv_rht(file,data,pricelist_name):
    csv_lst =[]
    for list in data:
        for l_k,l_v in list.iteritems():
            f1 = open (file,"r") # open input file for reading
            filename = ("/tmp/PRICELIST_RHT_%s.csv")%(l_k)
            print "_________filename____________",filename
            csv_lst.append(filename)
            with open(filename, 'w') as f: # output csv file
                writer = csv.writer(f, delimiter=',')
                with open(file,'r') as csvfile: # input csv file
                    reader = csv.reader(csvfile, delimiter=',')
                    for row in reader:
                        if row[1] != 'product_id' and row[3] != 'region_id':
                            row[5] = l_v[row[1]] and l_v[row[1]].get('Standing Charge pence per day', False) and l_v[row[1]]['Standing Charge pence per day'][float(row[3])] or 0.0
                            row[6] = l_v[row[1]] and l_v[row[1]].get('Primary Unit Rate kwh', False) and l_v[row[1]]['Primary Unit Rate kwh'][float(row[3])] or 0.0
                            row[9] = pricelist_name[l_k]
                            writer.writerow(row)
                        else:
                            writer.writerow(row)
                          
        f1.close()
    return csv_lst


def generate_csv_cng_gas(file,data,pricelist_name):
    csv_lst =[]
    my_dict = {
                       'region_id': '',
                       'product_id': '',
                       'amount': 0.00,
                       'primary_rate': 0.0,
                       'pricelist_id' : '',
                       'region_code' : 0.0,
                       'min_usage' : 0.0,
                       'max_usage' : 0.0
                       }
    f1 = open (file,"r") # open input file for reading
    filename = ("/tmp/%s.csv")%(pricelist_name)
    print "_________filename____________",filename
    csv_lst.append(filename)
    with open(filename, 'wb') as f: # output csv file
        w = csv.DictWriter(f, my_dict.keys())
        w.writeheader()
        for list in data:
            row = {
                   'region_id': '',
                   'product_id': list.get('Product',False) and list['Product'] or '',
                   'amount': 0.00,
                   'primary_rate': list.get('Day/All/STOD OtherDayUnits',False) and (list['Day/All/STOD OtherDayUnits']) * 100 or 0.0,
                   'pricelist_id' : pricelist_name,
                   'region_code' : list.get('Region',False) and list['Region'] or 0.0,
                   'min_usage' : list.get('MinAQ',False) and list['MinAQ'] or 0.0,
                   'max_usage' : list.get('MaxAQ',False) and list['MaxAQ'] or 0.0
                   }
            w.writerow(row)
    f1.close()
    return csv_lst


def generate_csv_total_gas(file,data,pricelist_name):
    csv_lst =[]
    my_dict = {
                       'region_id': '',
                       'product_id': '',
                       'amount': 0.00,
                       'primary_rate': 0.0,
                       'pricelist_id' : '',
                       'region_code' : 0.0,
                       'min_usage' : 0.0,
                       'max_usage' : 0.0,
                       'valid_from': False,
                       'valid_to': False,
                       'sub_region_id': '',
                       'month': False
                       }
    for line in data:
#         print "_________line___________",line
        for k,v in line.iteritems():
            print "___________k________________",k
            filename = ("/tmp/pricelist_total_%s.csv")%(k)
            print "_________filename____________",filename
            csv_lst.append(filename)
            with open(filename, 'wb') as f: # output csv file
                w = csv.DictWriter(f, my_dict.keys())
                w.writeheader()
                for list in v:
                    valid_from = time.strftime('%Y-%m-%d', list.get('Valid from',False) and time.strptime(list['Valid from'], '%d/%m/%Y') or False)
                    valid_to = time.strftime('%Y-%m-%d', list.get('Valid to',False) and time.strptime(list['Valid to'], '%d/%m/%Y') or False)
                    pro_name_lst = re.split(r'[, ]+',list.get('Product Name',False) and list['Product Name'] or '')
                    pro_month = [x for x in pro_name_lst if x in ['1','2','3','4','5','6','7','8','9','10','11','12']]
                    if pro_month:
                        if len(pro_month[0]) == 1:
                            pro_month[0] = '0'+pro_month[0]
                    row = {
                           'region_id': '',
                           'product_id': list.get('Product Name',False) and list['Product Name'] or '',
                           'amount': list.get('Standing Charge (pence/day)',False) and list['Standing Charge (pence/day)'] or 0.0,
                           'primary_rate': list.get('p/kWh',False) and list['p/kWh'] or 0.0,
                           'pricelist_id' : pricelist_name.get(k, False) and pricelist_name[k],
                           'region_code' : list.get('Region',False) and list['Region'][:-1] or 0.0,
                           'min_usage' : list.get('AQ Min (kWh)',False) and list['AQ Min (kWh)'] or 0.0,
                           'max_usage' : list.get('AQ Max (kWh)',False) and list['AQ Max (kWh)'] or 0.0,
                           'valid_from' : valid_from,
                           'valid_to' : valid_to,
                           'sub_region_id': list.get('Region',False) and list['Region'] or '',
                           'month': pro_month and pro_month[0] or False,
                           }
                    w.writerow(row)
            f.close()
    return csv_lst

def generate_csv_total_ele(file,data,pricelist_name):
    csv_lst = []
    my_dict = {
               'mtc_code': False,
               'product_id': False,
               'llf_code': False,
               'region_id': False,
               'profile_id': False,
               'amount': False,
               'primary_rate': 0.00,
               'secondary_rate':0.00,
               'tertiary_rate':0.00,
               'other_price_1': 0.00,
               'pricelist_id': False

               }
    for list in data:
        for k_profile,v_profile in list.iteritems():
#             print "__________k_profile__________",k_profile
            filename = ("/tmp/TOTAL_ELE_PRICELIST_%s.csv")%(k_profile)
            print "_________filename____________",filename
            csv_lst.append(filename)
            with open(filename, 'w') as f: # output csv file
                w = csv.DictWriter(f, my_dict.keys())
                w.writeheader()
                for l_k,l_v in v_profile.iteritems():
                    if l_v:
#                         print "__________l_k,l_v__________",l_k
                        for line in l_v:
#                             print "___________line_____________",line
                            row = {
                                   'mtc_code': line.get('MTC', False) and int(float(line['MTC'])) or False,
                                   'product_id': line.get('Product Name', False) and line['Product Name'] or False,
                                   'llf_code': '',
                                   'region_id': line.get('Region', False) and int(line['Region']) or False,
                                   'profile_id': line.get('Profiles', False) and int(line['Profiles']) or False,
                                   'amount': line.get('Fixed Charge p / day', False) and line['Fixed Charge p / day'] or False,
                                   'primary_rate': line.get('Units (p/kWh)', False) and line['Units (p/kWh)'] != '' and line['Units (p/kWh)'] or line.get('Day Units (p/kWh)', False) and line['Day Units (p/kWh)'] != '' and line['Day Units (p/kWh)'] or 0.00,
                                   'secondary_rate':line.get('Night Units (p/kWh)', False) and line['Night Units (p/kWh)'] or 0.00,
                                   'tertiary_rate': line.get('Eve/We Units (p/kWh)', False) and line['Eve/We Units (p/kWh)'] or 0.00,
                                   'other_price_1': line.get('Weekday Units (p/kWh)', False) and line['Weekday Units (p/kWh)'] or 0.00,
                                   'pricelist_id': pricelist_name.get(l_k, False) and pricelist_name[l_k] or False
                                   }
                            w.writerow(row)
    return csv_lst


def generate_csv_easy_price(file,data,pricelist_name,sheet):
    csv_lst = []
    my_dict = {
               'mtc_code': False,
               'product_id': False,
               'llf_code': False,
               'region_id': False,
               'profile_id': False,
               'amount': False,
               'primary_rate': 0.00,
               'secondary_rate':0.00,
               'tertiary_rate':0.00,
               'other_price_1': 0.00,
               'other_price_2': 0.00,
               'fit_rate': 0.00,
               'pricelist_id': False

               }
    for list in data:
        for k_profile,v_profile in list.iteritems():
            print "_________asdsadsa________________",file
#             print "__________k_profile__________",k_profile,v_profile
            f1 = open (file,"r") # open input file for reading
            filename = ("/tmp/%s_EASY_PRICELIST_%s.csv")%(sheet,k_profile)
            print "_________filename____________",filename
#             print "________pricelist_name___________",pricelist_name
            csv_lst.append(filename)
            temp_header = True
            with open(filename, 'w') as f: # output csv file
                writer = csv.writer(f, delimiter=',')
                with open(file,'r') as csvfile: # input csv file
                    reader = csv.reader(csvfile, delimiter=',')
                    for l_k,l_v in v_profile.iteritems():
#                         reader = csv.reader(csvfile, delimiter=',')
#                         print "__________l_k,l_v__________",l_k,l_v
                        for sub_k,sub_v in l_v.iteritems():
                            temp_mtc_lst = []
                            temp_llf_lst =[]
#                             print "___________sub_k,sub_v_____________",sub_k,sub_v
                            mtc = sub_v.get('MTC Guide', False) and isinstance(sub_v.get('MTC Guide', False), (str,unicode)) and [sub_v.get('MTC Guide', False)] or type(sub_v.get('MTC Guide', False)) ==  float and ("%d"%sub_v['MTC Guide']).split('.') or False
                            llf = sub_v.get('LLF Guide', False) and isinstance(sub_v.get('LLF Guide', False), (str,unicode)) and [sub_v.get('LLF Guide', False)] or type(sub_v.get('LLF Guide', False)) ==  float and ("%d"%sub_v['LLF Guide']).split('.') or False
                            if mtc:
                                mtc_lst = re.split(r'[,]+',mtc[0])
                                if len(mtc[0])%3 ==0:
                                    temp_mtc_lst = map(''.join, zip(*[iter(mtc[0])]*3))
                                else:
                                    temp_mtc_lst = mtc_lst
                            if llf:
                                llf_lst = re.split(r'[,]+',llf[0])
                                if len(llf[0])%3 ==0:
                                    temp_llf_lst = map(''.join, zip(*[iter(llf[0])]*3))
                                else:
                                    temp_llf_lst = llf_lst
#                             print "____________aa________",temp_mtc_lst
#                             print "____________temp_llf_lst________",temp_llf_lst
                            if temp_mtc_lst:
                                for temp_mtc in temp_mtc_lst:
#                                     print "______temp_mtc___________",temp_mtc
                                    if temp_llf_lst:
#                                         print "__________if_____________"
                                        for temp_llf in temp_llf_lst:
#                                             print "_________temp_llf_____________",temp_llf,reader
                                            csvfile.seek(0)
                                            for row in reader:
#                                                 print "________if__row_____________",row
#                                                 stop
                                                if row[1] != 'product_id' and row[3] != 'region_id':
#                                                     print "________row[2],temp_llf____________",row[2],temp_llf
                                                    if row[0] == temp_mtc and row[2] == temp_llf and row[4] == l_k:
#                                                         print "______l_v____________",l_v
#                                                         stop
                                                        row[5] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Standing Charge (p/Day)', False) and l_v[row[1]]['Standing Charge (p/Day)'] or 0.0
                                                        row[6] =  row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Unit Rate  (p/kWh)', False) and l_v[row[1]]['Unit Rate  (p/kWh)'] > 0.0 and l_v[row[1]]['Unit Rate  (p/kWh)'] or row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Day Rate (p/kWh)', False) and l_v[row[1]]['Day Rate (p/kWh)'] > 0.0 and l_v[row[1]]['Day Rate (p/kWh)'] or 0.0
                                                        row[7] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Night Rate (p/kWh)', False) and l_v[row[1]]['Night Rate (p/kWh)'] or 0.0
                                                        row[8] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Evening Weekend Rate (p/kWh)', False) and l_v[row[1]]['Evening Weekend Rate (p/kWh)'] or 0.0
                                                        row[9] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Weekday Rate (p/kWh)', False) and l_v[row[1]]['Weekday Rate (p/kWh)'] or 0.0
                                                        row[10] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Evening Weekend & Night Rate (p/kWh)', False) and l_v[row[1]]['Evening Weekend & Night Rate (p/kWh)'] or 0.0
                                                        row[11] = pricelist_name[k_profile]
                                                        writer.writerow(row)
                                                else:
#                                                     print "________temp_header________",temp_header
                                                    if temp_header:
                                                        writer.writerow(row)
                                                        temp_header = False
#                                             stop
                                    else:
#                                         print "__________else_____________"
                                        csvfile.seek(0)
                                        for row in reader:
#                                                 print "________else__row_____________",row
                                            if row[1] != 'product_id' and row[3] != 'region_id':
                                                if row[0] == temp_mtc and row[4] == l_k: 
                                                    row[5] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Standing Charge (p/Day)', False) and l_v[row[1]]['Standing Charge (p/Day)'] or 0.0
                                                    row[6] =  row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Unit Rate  (p/kWh)', False) and l_v[row[1]]['Unit Rate  (p/kWh)'] > 0.0 and l_v[row[1]]['Unit Rate  (p/kWh)'] or row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Day Rate (p/kWh)', False) and l_v[row[1]]['Day Rate (p/kWh)'] > 0.0 and l_v[row[1]]['Day Rate (p/kWh)'] or 0.0
                                                    row[7] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Night Rate (p/kWh)', False) and l_v[row[1]]['Night Rate (p/kWh)'] or 0.0
                                                    row[8] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Evening Weekend Rate (p/kWh)', False) and l_v[row[1]]['Evening Weekend Rate (p/kWh)'] or 0.0
                                                    row[9] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Weekday Rate (p/kWh)', False) and l_v[row[1]]['Weekday Rate (p/kWh)'] or 0.0
                                                    row[10] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Evening Weekend & Night Rate (p/kWh)', False) and l_v[row[1]]['Evening Weekend & Night Rate (p/kWh)'] or 0.0
                                                    row[11] = pricelist_name[k_profile]
                                                    writer.writerow(row)
                                            else:
#                                                 print "________temp_header________",temp_header
                                                if temp_header:
                                                    writer.writerow(row)
                                                    temp_header = False
                            elif temp_llf_lst:
                                for temp_llf in temp_llf_lst:
#                                     print "{________llf______________",temp_llf,reader
                                    csvfile.seek(0)
                                    for row in reader:
#                                         print "________if__row_____________",row
#                                         stop
                                        if row[1] != 'product_id' and row[3] != 'region_id':
#                                                 print "________row[2],temp_llf____________",row[2],temp_llf
                                            if row[2] == temp_llf and row[4] == l_k:
#                                                     print "______l_v____________",l_v
#                                                     stop 
                                                row[5] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Standing Charge (p/Day)', False) and l_v[row[1]]['Standing Charge (p/Day)'] or 0.0
                                                row[6] =  row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Unit Rate  (p/kWh)', False) and l_v[row[1]]['Unit Rate  (p/kWh)'] > 0.0 and l_v[row[1]]['Unit Rate  (p/kWh)'] or row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Day Rate (p/kWh)', False) and l_v[row[1]]['Day Rate (p/kWh)'] > 0.0 and l_v[row[1]]['Day Rate (p/kWh)'] or 0.0
                                                row[7] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Night Rate (p/kWh)', False) and l_v[row[1]]['Night Rate (p/kWh)'] or 0.0
                                                row[8] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Evening Weekend Rate (p/kWh)', False) and l_v[row[1]]['Evening Weekend Rate (p/kWh)'] or 0.0
                                                row[9] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Weekday Rate (p/kWh)', False) and l_v[row[1]]['Weekday Rate (p/kWh)'] or 0.0
                                                row[10] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Evening Weekend & Night Rate (p/kWh)', False) and l_v[row[1]]['Evening Weekend & Night Rate (p/kWh)'] or 0.0
                                                row[11] = pricelist_name[k_profile]
                                                writer.writerow(row)
                                        else:
#                                             print "________temp_header________",temp_header
                                            if temp_header:
#                                                 print "___________temp_header___________",temp_header
                                                writer.writerow(row)
                                                temp_header = False
                                            
                                                
                                    
            f1.close()
#     print "________csv_lst___________",csv_lst
#     stop
    return csv_lst



def generate_csv_bg_gas(file,data,pricelist_name):
    csv_lst =[]
    my_dict = {
                       'region_id': '',
                       'product_id': '',
                       'amount': 0.00,
                       'primary_rate': 0.0,
                       'pricelist_id' : '',
                       'min_usage' : 0.0,
                       'max_usage' : 0.0,
                       'payment_type_id': False,
                       }
    filename = ("/tmp/pricelist_total_BG_GAS.csv")
    print "_________filename____________",filename
    csv_lst.append(filename)
    with open(filename, 'wb') as f: # output csv file
        w = csv.DictWriter(f, my_dict.keys())
        w.writeheader()
        for line in data:
            pricelist = False
            payment_type = False
#             print "_________line___________",line
            if '-Y1-' in line.get('PRICE CODE',False) and line['PRICE CODE']:
                pricelist = pricelist_name.get('GAS 1 YEAR CONTRACT', False) and pricelist_name['GAS 1 YEAR CONTRACT']
            elif '-Y2-' in line.get('PRICE CODE',False) and line['PRICE CODE']:
                pricelist = pricelist_name.get('GAS 2 YEAR CONTRACT', False) and pricelist_name['GAS 2 YEAR CONTRACT']
            elif '-Y3-' in line.get('PRICE CODE',False) and line['PRICE CODE']:
                pricelist = pricelist_name.get('GAS 3 YEAR CONTRACT', False) and pricelist_name['GAS 3 YEAR CONTRACT']
            if 'DD' in line.get('PRICE CODE',False) and line['PRICE CODE']:
                payment_type = 'DD'
            elif 'CC' in line.get('PRICE CODE',False) and line['PRICE CODE']:
                payment_type = 'Cheque'
#             print "_______pricelist____________",pricelist
            usage = re.sub("[,>kWh ]", "", line.get('Consumption', False) and line['Consumption'] or '')
            usage = usage.split('-')
#             print "________usage____________",usage
            min_usage = 0.00
            max_usage = 0.00
            if usage:
                if float(usage[0]) >= 400000.00:
                    min_usage = float(usage[0])
                    max_usage = float(usage[0])
                else:
                    min_usage = float(usage[0])
                    max_usage = float(len(usage) > 1 and usage[1] or 0.00)
            
            row = {
                   'region_id': line.get('PES Region',False) and line['PES Region'] or '',
                   'product_id': line.get('PRICE CODE',False) and line['PRICE CODE'] or '',
                   'amount': line.get('STANDING CHARGE p/day',False) and line['STANDING CHARGE p/day'] or 0.0,
                   'primary_rate': line.get('Unit Rate p/kwh',False) and line['Unit Rate p/kwh'] or 0.0,
                   'pricelist_id' : pricelist,
                   'min_usage' : min_usage,
                   'max_usage' : max_usage,
                   'payment_type_id': payment_type
                   }
#             print "_________row____________",row
            w.writerow(row)
    f.close()
    return csv_lst



def generate_csv_bg_ele(file,data,pricelist_name,min,max):
    csv_lst =[]
    for main_k,main_v in data.iteritems():
        print "_________main_k,main_v_________",main_k,file
        filename = ("/tmp/pricelist_total_BG_ELE_%s.csv")%(main_k)
        print "_________filename____________",filename
        csv_lst.append(filename)
        with open(filename, 'w') as f: # output csv file
            writer = csv.writer(f, delimiter=',')
            with open(file,'r') as csvfile: # input csv file
                reader = csv.reader(csvfile, delimiter=',')
                for d1 in main_v:
                    for d2 in main_v:
                        if d1['Tariff'] == d2['Tariff'] and d1['PES'] == d2['PES'] and d1['Line Description'] != d2['Line Description'] and not d2.get('checked') and (not d1.get(d2['Line Description']) or not d2.get(d1['Line Description'])) and not d1.get('checked'):
                            d1.update({d2['Line Description'] : d2['Unit_Charge']})
                            d2.update({'checked': True})
                l1 = []
                for dic in main_v:
                    if not dic.get('checked'):
                        l1.append(dic)
#                 for line in l1:
# #                     print "_______line___________",line
#                     line.update({line['Line Description'] : line['Unit_Charge']})
#                     del line['Line Description']
#                     del line['Unit_Charge']
#                     print "_______line_____after______",line
#                     stop
                for row in reader:
                    for line in l1:
#                         print "_______line___________",line
                        line.update({line['Line Description'] : line['Unit_Charge']})
#                         del line['Line Description']
#                         del line['Unit_Charge']
                        if row[1] != 'product_id' and row[3] != 'region_id':
    #                             print "______!11_________",type(row[3]),row[3],type(str(line['PES'])),line['PES'],type(row[4]),row[4],type(line['Profile Class']),line['Profile Class']
    #                             stop
                            if float(row[3]) == (line.get('PES', False) and line['PES']) and (row[4] == (line.get('Profile Class',False) and line['Profile Class'])):
                                row[1] = line.get('Tariff', False) and line['Tariff'] or 0.0
                                row[5] = line.get('Standing Charge', False) and line['Standing Charge'] or 0.0
                                row[6] =  line.get('Day Unit Charge', False) and line['Day Unit Charge'] > 0.0 and line['Day Unit Charge'] or line.get('Night Unit Charge', False) and line['Night Unit Charge'] > 0.0 and line['Night Unit Charge'] or 0.0
                                row[7] = line.get('Night Rate (p/kWh)', False) and line['Night Rate (p/kWh)'] or 0.0
                                row[8] = line.get('Eve & Weekend Unit Charge', False) and line['Eve & Weekend Unit Charge'] or 0.0
                                row[9] = line.get('Weekday Rate (p/kWh)', False) and line['Weekday Rate (p/kWh)'] or 0.0
                                row[10] = line.get('Evening Weekend & Night Rate (p/kWh)', False) and line['Evening Weekend & Night Rate (p/kWh)'] or 0.0
                                row[11] = ''
                                row[12] = min
                                row[13] = max
                                row[14] = pricelist_name[main_k]
                                writer.writerow(row)
                        else:
                            writer.writerow(row)
        #             print "_________row____________",row
        f.close()
    return csv_lst


def generate_csv_opus_price(file,data,pricelist_name,sheet):
    csv_lst = []
    my_dict = {
               'mtc_code': False,
               'product_id': False,
               'llf_code': False,
               'region_id': False,
               'profile_id': False,
               'amount': False,
               'primary_rate': 0.00,
               'secondary_rate':0.00,
               'tertiary_rate':0.00,
               'other_price_1': 0.00,
               'other_price_2': 0.00,
               'fit_rate': 0.00,
               'pricelist_id': False

               }
    for list in data:
        for k_profile,v_profile in list.iteritems():
            print "_________asdsadsa________________",file
#             print "__________k_profile__________",k_profile,v_profile
            f1 = open (file,"r") # open input file for reading
            filename = ("/tmp/%s_opus_PRICELIST_%s.csv")%(sheet,k_profile)
            print "_________filename____________",filename
#             print "________pricelist_name___________",pricelist_name
            csv_lst.append(filename)
            temp_header = True
            with open(filename, 'w') as f: # output csv file
                writer = csv.writer(f, delimiter=',')
                with open(file,'r') as csvfile: # input csv file
                    reader = csv.reader(csvfile, delimiter=',')
                    for l_k,l_v in v_profile.iteritems():
#                         reader = csv.reader(csvfile, delimiter=',')
#                         print "__________l_k,l_v__________",l_k,l_v
#                         stop
                        for sub_k,sub_v in l_v.iteritems():
                            temp_mtc_lst = []
                            temp_llf_lst =[]
#                             if l_k in ('5','6','7','8') and sub_k == 'extra':
#                                 sub_k = 'Baserate'
                            if sub_k == 'extra' and sub_v.get('ns', False):
                                sub_k = 'Nightsaver'
                            if sub_k == 'extra' and sub_v.get('bs', False):
                                sub_k = 'Baserate'
#                             print "___________sub_k,sub_v_____________",sub_k,sub_v 
                            mtc = sub_v.get('MTC Guide', False) and isinstance(sub_v.get('MTC Guide', False), (str,unicode)) and [sub_v.get('MTC Guide', False)] or type(sub_v.get('MTC Guide', False)) ==  float and ("%d"%sub_v['MTC Guide']).split('.') or False
                            llf = sub_v.get('LLF Guide', False) and isinstance(sub_v.get('LLF Guide', False), (str,unicode)) and [sub_v.get('LLF Guide', False)] or type(sub_v.get('LLF Guide', False)) ==  float and ("%d"%sub_v['LLF Guide']).split('.') or False
                            if mtc:
                                mtc_lst = re.split(r'[,]+',mtc[0])
                                if len(mtc[0])%3 ==0:
                                    temp_mtc_lst = map(''.join, zip(*[iter(mtc[0])]*3))
                                else:
                                    temp_mtc_lst = mtc_lst
                            elif llf:
                                llf_lst = re.split(r'[,]+',llf[0])
                                if len(llf[0])%3 ==0:
                                    temp_llf_lst = map(''.join, zip(*[iter(llf[0])]*3))
                                else:
                                    temp_llf_lst = llf_lst
#                             print "____________aa________",temp_mtc_lst
#                             print "____________temp_llf_lst________",temp_llf_lst
#                             if temp_mtc_lst:
#                                 for temp_mtc in temp_mtc_lst:
#                                     if temp_llf_lst:
#                                         for temp_llf in temp_llf_lst:
#                                             csvfile.seek(0)
#                                             for row in reader:
#                                                 if row[1] != 'product_id' and row[3] != 'region_id':
#                                                     if row[0] == temp_mtc and row[2] == temp_llf and row[4] == l_k:
#                                                         row[5] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Standing Charge (p/Day)', False) and l_v[row[1]]['Standing Charge (p/Day)'] or 0.0
#                                                         row[6] =  row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Unit Rate  (p/kWh)', False) and l_v[row[1]]['Unit Rate  (p/kWh)'] > 0.0 and l_v[row[1]]['Unit Rate  (p/kWh)'] or row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Day Rate (p/kWh)', False) and l_v[row[1]]['Day Rate (p/kWh)'] > 0.0 and l_v[row[1]]['Day Rate (p/kWh)'] or 0.0
#                                                         row[7] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Night Rate (p/kWh)', False) and l_v[row[1]]['Night Rate (p/kWh)'] or 0.0
#                                                         row[8] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Evening Weekend Rate (p/kWh)', False) and l_v[row[1]]['Evening Weekend Rate (p/kWh)'] or 0.0
#                                                         row[9] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Weekday Rate (p/kWh)', False) and l_v[row[1]]['Weekday Rate (p/kWh)'] or 0.0
#                                                         row[10] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Evening Weekend & Night Rate (p/kWh)', False) and l_v[row[1]]['Evening Weekend & Night Rate (p/kWh)'] or 0.0
#                                                         row[11] = pricelist_name[k_profile]
#                                                         writer.writerow(row)
#                                                     elif row[2] == temp_llf and row[4] == l_k:
#                                                         row[5] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Standing Charge (p/Day)', False) and l_v[row[1]]['Standing Charge (p/Day)'] or 0.0
#                                                         row[6] =  row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Unit Rate  (p/kWh)', False) and l_v[row[1]]['Unit Rate  (p/kWh)'] > 0.0 and l_v[row[1]]['Unit Rate  (p/kWh)'] or row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Day Rate (p/kWh)', False) and l_v[row[1]]['Day Rate (p/kWh)'] > 0.0 and l_v[row[1]]['Day Rate (p/kWh)'] or 0.0
#                                                         row[7] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Night Rate (p/kWh)', False) and l_v[row[1]]['Night Rate (p/kWh)'] or 0.0
#                                                         row[8] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Evening Weekend Rate (p/kWh)', False) and l_v[row[1]]['Evening Weekend Rate (p/kWh)'] or 0.0
#                                                         row[9] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Weekday Rate (p/kWh)', False) and l_v[row[1]]['Weekday Rate (p/kWh)'] or 0.0
#                                                         row[10] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Evening Weekend & Night Rate (p/kWh)', False) and l_v[row[1]]['Evening Weekend & Night Rate (p/kWh)'] or 0.0
#                                                         row[11] = pricelist_name[k_profile]
#                                                         writer.writerow(row)
#                                                 else:
#                                                     if temp_header:
#                                                         writer.writerow(row)
#                                                         temp_header = False
#                                     else:
#                                         csvfile.seek(0)
#                                         for row in reader:
#                                             if row[1] != 'product_id' and row[3] != 'region_id':
#                                                 if row[0] == temp_mtc and row[4] == l_k: 
#                                                     row[5] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Standing Charge (p/Day)', False) and l_v[row[1]]['Standing Charge (p/Day)'] or 0.0
#                                                     row[6] =  row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Unit Rate  (p/kWh)', False) and l_v[row[1]]['Unit Rate  (p/kWh)'] > 0.0 and l_v[row[1]]['Unit Rate  (p/kWh)'] or row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Day Rate (p/kWh)', False) and l_v[row[1]]['Day Rate (p/kWh)'] > 0.0 and l_v[row[1]]['Day Rate (p/kWh)'] or 0.0
#                                                     row[7] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Night Rate (p/kWh)', False) and l_v[row[1]]['Night Rate (p/kWh)'] or 0.0
#                                                     row[8] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Evening Weekend Rate (p/kWh)', False) and l_v[row[1]]['Evening Weekend Rate (p/kWh)'] or 0.0
#                                                     row[9] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Weekday Rate (p/kWh)', False) and l_v[row[1]]['Weekday Rate (p/kWh)'] or 0.0
#                                                     row[10] = row[1] in l_v and l_v[row[1]] and l_v[row[1]].get('Evening Weekend & Night Rate (p/kWh)', False) and l_v[row[1]]['Evening Weekend & Night Rate (p/kWh)'] or 0.0
#                                                     row[11] = pricelist_name[k_profile]
#                                                     writer.writerow(row)
#                                             else:
#                                                 if temp_header:
#                                                     writer.writerow(row)
#                                                     temp_header = False
                            if temp_llf_lst:
                                for temp_llf in temp_llf_lst:
                                    csvfile.seek(0)
                                    for row in reader:
                                        if row[1] != 'product_id' and row[3] != 'region_id':
                                            if row[2] == temp_llf and row[4] == l_k:
                                                row[5] = sub_v.get('Standing Charge (p/Day)', False) and sub_v['Standing Charge (p/Day)'] or 0.0
                                                row[6] =  sub_v.get('Unit Rate  (p/kWh)', False) and sub_v['Unit Rate  (p/kWh)'] > 0.0 and sub_v['Unit Rate  (p/kWh)'] or sub_v.get('Day Rate (p/kWh)', False) and sub_v['Day Rate (p/kWh)'] > 0.0 and sub_v['Day Rate (p/kWh)'] or 0.0
                                                row[7] = sub_v.get('Night Rate (p/kWh)', False) and sub_v['Night Rate (p/kWh)'] or 0.0
                                                row[8] = sub_v.get('Evening Weekend Rate (p/kWh)', False) and sub_v['Evening Weekend Rate (p/kWh)'] or 0.0
                                                row[9] = sub_v.get('Weekday Rate (p/kWh)', False) and sub_v['Weekday Rate (p/kWh)'] or 0.0
                                                row[10] = sub_v.get('Evening Weekend & Night Rate (p/kWh)', False) and sub_v['Evening Weekend & Night Rate (p/kWh)'] or 0.0
                                                row[11] = pricelist_name[k_profile]
#                                                 if temp_llf in ('15','49'):
#                                                     print "__________row_______________",row
# #                                                     stop
                                                writer.writerow(row)
                                        else:
                                            if temp_header:
                                                writer.writerow(row)
                                                temp_header = False
                                                
                            else:
                                csvfile.seek(0)
#                                 for temp_mtc in temp_mtc_lst:
                                for row in reader:
                                    if row[1] != 'product_id' and row[3] != 'region_id':
                                        if row[1] == sub_k and row[4] == l_k:
#                                             if row[0] == temp_mtc and row[4] == l_k:
                                            row[5] = sub_v.get('Standing Charge (p/Day)', False) and sub_v['Standing Charge (p/Day)'] or 0.0
                                            row[6] =  sub_v.get('Unit Rate  (p/kWh)', False) and sub_v['Unit Rate  (p/kWh)'] > 0.0 and sub_v['Unit Rate  (p/kWh)'] or sub_v.get('Day Rate (p/kWh)', False) and sub_v['Day Rate (p/kWh)'] > 0.0 and sub_v['Day Rate (p/kWh)'] or 0.0
                                            row[7] = sub_v.get('Night Rate (p/kWh)', False) and sub_v['Night Rate (p/kWh)'] or 0.0
                                            row[8] = sub_v.get('Evening Weekend Rate (p/kWh)', False) and sub_v['Evening Weekend Rate (p/kWh)'] or 0.0
                                            row[9] = sub_v.get('Weekday Rate (p/kWh)', False) and sub_v['Weekday Rate (p/kWh)'] or 0.0
                                            row[10] = sub_v.get('Evening Weekend & Night Rate (p/kWh)', False) and sub_v['Evening Weekend & Night Rate (p/kWh)'] or 0.0
                                            row[11] = pricelist_name[k_profile]
                                            writer.writerow(row)
                                    else:
                                        if temp_header:
                                            writer.writerow(row)
                                            temp_header = False
                                            
                                                
                                    
            f1.close()
#     print "________csv_lst___________",csv_lst
#     stop
    return csv_lst


def generate_csv_opus_gas(file,data,pricelist_name,sheet):
    csv_lst =[]
    final_lst = []
    
    my_dict = {
                       'region_id': '',
                       'product_id': '',
                       'amount': 0.00,
                       'primary_rate': 0.0,
                       'pricelist_id' : '',
                       'min_usage' : 0.0,
                       'max_usage' : 0.0,
                       'region_code': '',
                       'check_sc': False
                       }
    for main_k,main_v in data.iteritems():
        print "_________main_k,main_v_________",main_k
        for temp_dic in main_v:
            final_lst.append(temp_dic)
    filename = ("/tmp/pricelist_opus_gas_%s.csv")%(sheet)
    print "_________filename____________",filename
    csv_lst.append(filename)
    with open(filename, 'wb') as f: # output csv file
        w = csv.DictWriter(f, my_dict.keys())
        w.writeheader()
        for line in final_lst:
            check_sc = False
            if sheet == 0:
                check_sc = True
            row = {
               'region_id': '',
               'region_code': line.get('LDZ',False) and line['LDZ'] or '', 
               'product_id': line.get('Tariff Code',False) and line['Tariff Code'] or '',
               'amount': line.get('SC p/day',False) and line['SC p/day'] or 0.0,
               'primary_rate': line.get('Unit p/kWh',False) and line['Unit p/kWh'] or 0.0,
               'pricelist_id' : pricelist_name.get('GAS CONTRACT', False) and pricelist_name['GAS CONTRACT'] or '',
               'min_usage' : line.get('min',False) and line['min'] or 0.0,
               'max_usage' : line.get('max',False) and line['max'] or 0.0,
               'check_sc': check_sc,
               }
            w.writerow(row)
    f.close()
    return csv_lst



def generate_csv_sse_gas(file,data,pricelist_name,utility_type):
    csv_lst =[]
    my_dict = {
                       'region_id': '',
                       'product_id': '',
                       'amount': 0.00,
                       'primary_rate': 0.0,
                       'pricelist_id' : '',
                       'region_code' : 0.0,
                       'min_usage' : 0.0,
                       'max_usage' : 0.0,
                       'valid_from': False,
                       'valid_to': False,
                       }
    
#         print "_________line___________",line
#         stop
#         for k,v in line.iteritems():
#             print "___________k________________",k
    filename = ("/tmp/pricelist_sse_gas.csv")
    print "_________filename____________",filename
    csv_lst.append(filename)
    with open(filename, 'wb') as f: # output csv file
        w = csv.DictWriter(f, my_dict.keys())
        w.writeheader()
        for line in data:
            cons_lst = []
            if 'Consumption Band' in line:
                cons_lst = re.split(r'[- ]+',line['Consumption Band'])
            row = {
                   'region_id': '',
#                    'product_id': line.get('MatrixID',False) and str(line['MatrixID']) or '',
                    'product_id': '12841',
                   'amount': line.get('StandingChargeLive',False) and line['StandingChargeLive'] or 0.0,
                   'primary_rate': line.get('UnitRateLive',False) and line['UnitRateLive'] or 0.0,
                   'pricelist_id' : pricelist_name.get('GAS CONTRACT', False) and pricelist_name['GAS CONTRACT'] or False,
                   'region_code' : line.get('LDZ',False) and line['LDZ'] or '',
                   'min_usage' : cons_lst and cons_lst[0] or 0.0,
                   'max_usage' : cons_lst and len(cons_lst) > 1 and cons_lst[1] or 0.0,
                   'valid_from' : line.get('ProposedStartDate', False) and line['ProposedStartDate'] or False,
                   'valid_to' : line.get('ProposedEndDate', False) and line['ProposedEndDate'] or False,
                   }
            w.writerow(row)
    f.close()
#     stop
    return csv_lst


def generate_csv_ovo_baserate(file,data,pricelist_name,sheet):
    csv_lst = []
    
    for k,v in data.iteritems():
        for sub_k,sub_v in v.iteritems():
            temp_header = True
            f1 = open (file,"r") # open input file for reading
            filename = ("/tmp/ovo_%s_%s.csv")%(sub_k,sheet)
            csv_lst.append(filename)
            with open(filename, 'w') as f: # output csv file
                writer = csv.writer(f, delimiter=',')
                with open(file,'r') as csvfile: # input csv file
                    reader = csv.reader(csvfile, delimiter=',')
                    for col in reader:
                        for line_v in sub_v:
                            if col[1] != 'product_id' and col[3] != 'region_id':
                                if col[1] == k and float(col[3]) == line_v['Region']:
                                    col[5] = line_v.get('P3 Better Energy standing charge', False) and (line_v['P3 Better Energy standing charge'] * 100) or 0.00  
                                    col[6] = line_v.get('P3 Better Energy unit rate', False) and (line_v['P3 Better Energy unit rate'] * 100) or 0.00
                                    col[10] = line_v.get('P4 Better Energy standing charge', False) and (line_v['P4 Better Energy standing charge']* 100) or 0.00
                                    col[11] = line_v.get('P4 Better Energy Day unit rate', False) and (line_v['P4 Better Energy Day unit rate']* 100) or 0.00
                                    col[12] = line_v.get('P4 Better Energy Night unit rate', False) and (line_v['P4 Better Energy Night unit rate']* 100) or 0.00
                                    col[9] = pricelist_name.get(sub_k, False) and pricelist_name[sub_k] or False
                                    writer.writerow(col)
                            else:
                                if temp_header:
                                    writer.writerow(col)
                                    temp_header = False
            f.close()
    return csv_lst

