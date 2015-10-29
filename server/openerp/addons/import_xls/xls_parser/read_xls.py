import xlrd
import csv
import shutil
import os
import read_xls_1 as first_sheet
import read_xls_3 as third_sheet
import read_xls_5 as fifth_sheet
import import_pricelist as pricelist
from macpath import defpath
import addons

def parse_xls_file(xls_file,db,user,host,password,pricelist_name, wizard_obj):
    rb = xlrd.open_workbook(xls_file,formatting_info=False)
    final_lst = []
    for sheet in [1,3,5]:
        worksheet = rb.sheet_by_index(sheet)
        region_values = worksheet.row_values(4)
        data_lst = []
        if sheet == 1:
            file = addons.get_module_resource('import_xls/csv_data', 'master_sheet_1234.csv')
            file_gas = addons.get_module_resource('import_xls/csv_data', 'master_csv_gas.csv')
            product_values = {'ELECTRICITY 1 YEAR CONTRACT':{'Baserate': {'Standing Charge pence per day':7,'Primary Unit Rate kwh':8},
                                                              'Nightsaver': {'Standing Charge pence per day':10,'Primary Unit Rate kwh':11,'Night Unit Rate kwh':12},
                                                              'Flexirate 2':{'Standing Charge pence per day':14,'Primary Unit Rate kwh':15,'Evening and Weekend Unit Rate kwh':16},
                                                              'Flexirate 3':{'Standing Charge pence per day':18,'Primary Unit Rate kwh':19,'Night Unit Rate kwh': 20,'Evening and Weekend Unit Rate kwh':21},
                                                              },
                            'ELECTRICITY 2 YEAR CONTRACT': {'Baserate': {'Standing Charge pence per day':24,'Primary Unit Rate kwh':25},
                                                            'Nightsaver': {'Standing Charge pence per day':27,'Primary Unit Rate kwh':28,'Night Unit Rate kwh':29},
                                                            'Flexirate 2':{'Standing Charge pence per day':31,'Primary Unit Rate kwh':32,'Evening and Weekend Unit Rate kwh':33},
                                                            'Flexirate 3':{'Standing Charge pence per day':35,'Primary Unit Rate kwh':36,'Night Unit Rate kwh': 37,'Evening and Weekend Unit Rate kwh':38},
                                                            },
                            'ELECTRICITY 3 YEAR CONTRACT': {'Baserate': {'Standing Charge pence per day':41,'Primary Unit Rate kwh':42},
                                                            'Nightsaver': {'Standing Charge pence per day':44,'Primary Unit Rate kwh':45,'Night Unit Rate kwh':46},
                                                            'Flexirate 2':{'Standing Charge pence per day':48,'Primary Unit Rate kwh':49,'Evening and Weekend Unit Rate kwh':50},
                                                            'Flexirate 3':{'Standing Charge pence per day':52,'Primary Unit Rate kwh':53,'Night Unit Rate kwh': 54,'Evening and Weekend Unit Rate kwh':55},
                                                            }
                              
                              }
            product_values_gas = {
                                    'GAS 1 YEAR CONTRACT':{'Standing Charge pence per day':87,'Primary Unit Rate kwh':88},
                                    'GAS 2 YEAR CONTRACT': {'Standing Charge pence per day':91,'Primary Unit Rate kwh':92},
                                    'GAS 3 YEAR CONTRACT': {'Standing Charge pence per day':95,'Primary Unit Rate kwh':96},
                                }
            
            
            sheet_1_data = first_sheet.sheet_1_price(file,product_values, worksheet, region_values,pricelist_name)
            sheet_1_data_gas = first_sheet.sheet_1_gas_price(file_gas,product_values_gas, worksheet, region_values,pricelist_name)
            final_lst += sheet_1_data
        elif sheet == 5:
            file = addons.get_module_resource('import_xls/csv_data', 'master_sheet_5678.csv')
            if wizard_obj.check_format:
                product_values = {'5':{'ELECTRICITY 1 YEAR CONTRACT':{'Baserate': {'Standing Charge pence per day':7,'Primary Unit Rate kwh':8},
                                                                          'Nightsaver': {'Standing Charge pence per day':10,'Primary Unit Rate kwh':11,'Night Unit Rate kwh':12}
                                                                          },
                                        'ELECTRICITY 2 YEAR CONTRACT': {'Baserate': {'Standing Charge pence per day':15,'Primary Unit Rate kwh':16},
                                                                        'Nightsaver': {'Standing Charge pence per day':18,'Primary Unit Rate kwh':19,'Night Unit Rate kwh':20}
                                                                        }
                                          
                                          },
                                  '6': {'ELECTRICITY 1 YEAR CONTRACT':{'Baserate': {'Standing Charge pence per day':7,'Primary Unit Rate kwh':8},
                                                                          'Nightsaver': {'Standing Charge pence per day':10,'Primary Unit Rate kwh':11,'Night Unit Rate kwh':12}
                                                                          },
                                        'ELECTRICITY 2 YEAR CONTRACT': {'Baserate': {'Standing Charge pence per day':15,'Primary Unit Rate kwh':16},
                                                                        'Nightsaver': {'Standing Charge pence per day':18,'Primary Unit Rate kwh':19,'Night Unit Rate kwh':20}
                                                                        }
                                          
                                          },
                                  '7': {'ELECTRICITY 1 YEAR CONTRACT':{'Baserate': {'Standing Charge pence per day':7,'Primary Unit Rate kwh':8},
                                                                          'Nightsaver': {'Standing Charge pence per day':10,'Primary Unit Rate kwh':11,'Night Unit Rate kwh':12}
                                                                          },
                                        'ELECTRICITY 2 YEAR CONTRACT': {'Baserate': {'Standing Charge pence per day':15,'Primary Unit Rate kwh':16},
                                                                        'Nightsaver': {'Standing Charge pence per day':18,'Primary Unit Rate kwh':19,'Night Unit Rate kwh':20}
                                                                        }
                                          
                                          },
                                  '8': {'ELECTRICITY 1 YEAR CONTRACT':{'Baserate': {'Standing Charge pence per day':7,'Primary Unit Rate kwh':8},
                                                                          'Nightsaver': {'Standing Charge pence per day':10,'Primary Unit Rate kwh':11,'Night Unit Rate kwh':12}
                                                                          },
                                        'ELECTRICITY 2 YEAR CONTRACT': {'Baserate': {'Standing Charge pence per day':15,'Primary Unit Rate kwh':16},
                                                                        'Nightsaver': {'Standing Charge pence per day':18,'Primary Unit Rate kwh':19,'Night Unit Rate kwh':20}
                                                                        }
                                          
                                          },
                                  }
            else:
                product_values = {'5':{'ELECTRICITY 1 YEAR CONTRACT':{'Baserate': {'Standing Charge pence per day':7,'Primary Unit Rate kwh':8},
                                                                          'Nightsaver': {'Standing Charge pence per day':10,'Primary Unit Rate kwh':11,'Night Unit Rate kwh':12}
                                                                          },
                                        'ELECTRICITY 2 YEAR CONTRACT': {'Baserate': {'Standing Charge pence per day':15,'Primary Unit Rate kwh':16},
                                                                        'Nightsaver': {'Standing Charge pence per day':18,'Primary Unit Rate kwh':19,'Night Unit Rate kwh':20}
                                                                        }
                                          
                                          },
                                  '6': {'ELECTRICITY 1 YEAR CONTRACT':{'Baserate': {'Standing Charge pence per day':24,'Primary Unit Rate kwh':25},
                                                                          'Nightsaver': {'Standing Charge pence per day':27,'Primary Unit Rate kwh':28,'Night Unit Rate kwh':29}
                                                                          },
                                        'ELECTRICITY 2 YEAR CONTRACT': {'Baserate': {'Standing Charge pence per day':32,'Primary Unit Rate kwh':33},
                                                                        'Nightsaver': {'Standing Charge pence per day':35,'Primary Unit Rate kwh':36,'Night Unit Rate kwh':37}
                                                                        }
                                          
                                          },
                                  '7': {'ELECTRICITY 1 YEAR CONTRACT':{'Baserate': {'Standing Charge pence per day':69,'Primary Unit Rate kwh':70},
                                                                          'Nightsaver': {'Standing Charge pence per day':72,'Primary Unit Rate kwh':73,'Night Unit Rate kwh':74}
                                                                          },
                                        'ELECTRICITY 2 YEAR CONTRACT': {'Baserate': {'Standing Charge pence per day':77,'Primary Unit Rate kwh':78},
                                                                        'Nightsaver': {'Standing Charge pence per day':80,'Primary Unit Rate kwh':81,'Night Unit Rate kwh':82}
                                                                        }
                                          
                                          },
                                  '8': {'ELECTRICITY 1 YEAR CONTRACT':{'Baserate': {'Standing Charge pence per day':86,'Primary Unit Rate kwh':87},
                                                                          'Nightsaver': {'Standing Charge pence per day':89,'Primary Unit Rate kwh':90,'Night Unit Rate kwh':91}
                                                                          },
                                        'ELECTRICITY 2 YEAR CONTRACT': {'Baserate': {'Standing Charge pence per day':94,'Primary Unit Rate kwh':95},
                                                                        'Nightsaver': {'Standing Charge pence per day':97,'Primary Unit Rate kwh':98,'Night Unit Rate kwh':99}
                                                                        }
                                          
                                          }
                                  }
            sheet_5_data = fifth_sheet.sheet_5_price(file,product_values, worksheet, region_values,pricelist_name)
            final_lst += sheet_5_data
        elif sheet == 3:
            file = addons.get_module_resource('import_xls/csv_data', 'master_sheet_rht.csv')
            product_values = {'ELECTRICITY 1 YEAR CONTRACT':{'RHT': {'Standing Charge pence per day':7,'Primary Unit Rate kwh':8}},
                            'ELECTRICITY 2 YEAR CONTRACT': {'RHT': {'Standing Charge pence per day':7,'Primary Unit Rate kwh':8}},
                            'ELECTRICITY 3 YEAR CONTRACT': {'RHT': {'Standing Charge pence per day':7,'Primary Unit Rate kwh':8}}
                              }
            sheet_3_data = third_sheet.sheet_3_price(file,product_values, worksheet, region_values,pricelist_name)
            final_lst += sheet_3_data
    pricelist.import_pricelist(db,user,host,password,final_lst)
    pricelist.import_pricelist_gas(db,user,host,password,sheet_1_data_gas)
    final_lst += sheet_1_data_gas
    return final_lst


def parse_cng_xls_file(xls_file,db,pricelist_name, wizard_obj):
    user = wizard_obj.postgres_config_id.db_user
    host = wizard_obj.postgres_config_id.host_name
    password = wizard_obj.postgres_config_id.db_user_pass
    rb = xlrd.open_workbook(xls_file,formatting_info=False)
    final_lst = []
    worksheet = rb.sheet_by_index(0)
    col_values = worksheet.row_values(0)
    data_lst = []
    file_gas = addons.get_module_resource('import_xls/csv_data', 'master_sheet_cng_gas.csv')
    sheet_1_data_gas = first_sheet.sheet_1_cng_gas_price(file_gas,col_values,worksheet,pricelist_name)
    pricelist.import_pricelist_cng_gas(db,user,host,password,sheet_1_data_gas)
    final_lst += sheet_1_data_gas
    return final_lst


def parse_total_xls_file(xls_file,db,pricelist_name, wizard_obj):
    user = wizard_obj.postgres_config_id.db_user
    host = wizard_obj.postgres_config_id.host_name
    password = wizard_obj.postgres_config_id.db_user_pass
    utility_type = wizard_obj.categ_id and wizard_obj.categ_id.name or False 
    reader = csv.DictReader(open(xls_file, 'r'), delimiter=",")
    final_lst = []
    data_lst = []
    file_gas = addons.get_module_resource('import_xls/csv_data', 'master_sheet_cng_gas.csv')
    if utility_type == 'Gas':
        product_lst,sheet_1_data_gas = first_sheet.sheet_1_total_gas_price(file_gas,reader,pricelist_name,utility_type)
        product_import = pricelist.import_pricelist_total_product(db,user,host,password,product_lst,utility_type)
        pricelist.import_pricelist_total_gas(db,user,host,password,sheet_1_data_gas,utility_type)
    elif utility_type == 'Electricity':
        product_lst,sheet_1_data_gas = first_sheet.sheet_1_total_gas_price(file_gas,reader,pricelist_name,utility_type)
        product_import = pricelist.import_pricelist_total_product(db,user,host,password,product_lst,utility_type)
        pricelist.import_total_pricelist_ele(db,user,host,password,sheet_1_data_gas,utility_type)
    final_lst += sheet_1_data_gas
    return final_lst


def parse_easy_utility_xls_file(xls_file,db,pricelist_name, wizard_obj):
    user = wizard_obj.postgres_config_id.db_user
    host = wizard_obj.postgres_config_id.host_name
    password = wizard_obj.postgres_config_id.db_user_pass
    utility_type = wizard_obj.categ_id and wizard_obj.categ_id.name or False 
    rb = xlrd.open_workbook(xls_file,formatting_info=False,on_demand=False, ragged_rows=False)
    final_lst = []
    data_lst = []
    file_dic = {
                '10': '10_easy_master.csv',
                '11': '11_easy_master.csv',
                '12': '12_easy_master.csv',
                '13': '13_easy_master.csv',
                '14': '14_easy_master.csv',
                '15': '15_easy_master.csv',
                '16': '16_easy_master.csv',
                '17': '17_easy_master.csv',
                '18': '18_easy_master.csv',
                '19': '19_easy_master.csv',
                '20': '20_easy_master.csv',
                '21': '21_easy_master.csv',
                '22': '22_easy_master.csv',
                '23': '23_easy_master.csv'
                }
    for sheet in ['10','11','12','13','14','15','16','17','18','19','20','21','22','23']:
#     for sheet in ['20']:
        print "________sheet__________",sheet
#         worksheet = rb.sheet_by_index(sheet)
        worksheet = rb.sheet_by_name(sheet)
#         print "________adsadsa_________",rb.sheet_by_name('10')
#         stop
        col_values = worksheet.row_values(0)
#         region_values = worksheet.row_values(1)
        file_gas = addons.get_module_resource('import_xls/csv_data', file_dic[sheet])
        product_values = {
                          'ELECTRICITY 2 YEAR CONTRACT':{
                                                           '3':{'Baserate': 35,
                                                                'Flexirate 2':36
                                                                },
                                                            '4':{'Nightsaver': 37,
                                                                'Flexirate 3':38,
                                                                'RHT':39,
                                                                  },
                                                            '5':{'Baserate': 42,
                                                                'Nightsaver': 43,
                                                                'Flexirate 3':44,
                                                                  },
                                                            '6':{'Baserate': 42,
                                                                'Nightsaver': 43,
                                                                'Flexirate 3':44,
                                                                  },
                                                            '7':{'Baserate': 42,
                                                                'Nightsaver': 43,
                                                                'Flexirate 3':44,
                                                                  },
                                                            '8':{'Baserate': 42,
                                                                'Nightsaver': 43,
                                                                'Flexirate 3':44,
                                                                  }
                                                         },
                            'ELECTRICITY 3 YEAR CONTRACT': {
                                                            '3':{'Baserate': 17,
                                                                'Flexirate 2':18,
                                                                    },
                                                            '4':{
                                                                'Nightsaver': 19,
                                                                'Flexirate 3':20,
                                                                'RHT':21,
                                                                    },
                                                            '5':{'Baserate': 24,
                                                                'Nightsaver': 25,
                                                                'Flexirate 3':26,
                                                                    },
                                                            '6':{'Baserate': 24,
                                                                'Nightsaver': 25,
                                                                'Flexirate 3':26,
                                                                    },
                                                            '7':{'Baserate': 24,
                                                                'Nightsaver': 25,
                                                                'Flexirate 3':26,
                                                                    },
                                                            '8':{'Baserate': 24,
                                                                'Nightsaver': 25,
                                                                'Flexirate 3':26,
                                                                    },
                                                            }
                        }
                          
        
        
        
        sheet_1_data_gas = first_sheet.sheet_1_easy_utility_price(file_gas,worksheet,product_values,pricelist_name,utility_type,sheet)
        final_lst += sheet_1_data_gas
    print "__________final_lst___________",final_lst
#     stop
#     product_import = pricelist.import_pricelist_total_product(db,user,host,password,product_lst,utility_type)
    pricelist.import_easy_pricelist_ele(db,user,host,password,final_lst)
#     final_lst += sheet_1_data_gas
    return final_lst


def parse_bg_gas_xls_file(xls_file,db,pricelist_name, wizard_obj):
    user = wizard_obj.postgres_config_id.db_user
    host = wizard_obj.postgres_config_id.host_name
    password = wizard_obj.postgres_config_id.db_user_pass
    utility_type = wizard_obj.categ_id and wizard_obj.categ_id.name or False 
    rb = xlrd.open_workbook(xls_file,formatting_info=False)
    final_lst = []
    worksheet = rb.sheet_by_name('Sheet1')
    col_values = worksheet.row_values(1,start_colx=0, end_colx=6)
#     print "________col_values______________",col_values
    data_lst = []
    file_gas = addons.get_module_resource('import_xls/csv_data', 'master_sheet_cng_gas.csv')
    sheet_1_data_gas,product_lst = first_sheet.sheet_1_bg_gas_price(file_gas,col_values,worksheet,pricelist_name)
    product_import = pricelist.import_pricelist_bg_gas_product(db,user,host,password,product_lst,utility_type)
    pricelist.import_pricelist_bg_gas(db,user,host,password,sheet_1_data_gas,utility_type)
    final_lst += sheet_1_data_gas
    return final_lst


def parse_bg_ele_xls_file(xls_file,db,pricelist_name, wizard_obj):
    user = wizard_obj.postgres_config_id.db_user
    host = wizard_obj.postgres_config_id.host_name
    password = wizard_obj.postgres_config_id.db_user_pass
    utility_type = wizard_obj.categ_id and wizard_obj.categ_id.name or False 
    rb = xlrd.open_workbook(xls_file,formatting_info=False)
    final_lst = []
    for sheet in ['Range 1','Range 2','Range 3']:
        product_values = {
                        'ELECTRICITY 1 YEAR CONTRACT': {'start_col': 0,'end_col':7},
                        'ELECTRICITY 2 YEAR CONTRACT': {'start_col': 8,'end_col':15},
                          'ELECTRICITY 3 YEAR CONTRACT': {'start_col': 16,'end_col':23}
                          }
        if sheet == 'Range 1':
            min = 0.0
            max = 11999.00
        elif sheet == 'Range 2':
            min = 12000.00
            max = 50999.00
        elif sheet == 'Range 3':
            min = 51000.00
            max = 51000.00
        worksheet = rb.sheet_by_name(sheet)
        col_values = worksheet.row_values(1,start_colx=0, end_colx=7)
    #     print "________col_values______________",col_values
        data_lst = []
        file_gas = addons.get_module_resource('import_xls/csv_data', 'master_bg_ele.csv')
        sheet_1_data_gas,product_lst = first_sheet.sheet_1_bg_ele_price(file_gas,col_values,worksheet,pricelist_name,product_values,min,max)
#     product_import = pricelist.import_pricelist_bg_gas_product(db,user,host,password,product_lst,utility_type)
    pricelist.import_pricelist_bg_gas(db,user,host,password,sheet_1_data_gas,utility_type)
    final_lst += sheet_1_data_gas
    return final_lst



def parse_opus_xls_file(xls_file,db,pricelist_name, wizard_obj):
    user = wizard_obj.postgres_config_id.db_user
    host = wizard_obj.postgres_config_id.host_name
    password = wizard_obj.postgres_config_id.db_user_pass
    utility_type = wizard_obj.categ_id and wizard_obj.categ_id.name or False 
    rb = xlrd.open_workbook(xls_file,formatting_info=False,on_demand=False, ragged_rows=False)
    final_lst = []
    product_final_lst = []
    if utility_type == 'Electricity':
        file_dic = {
                    '10': '10_opus_master.csv',
                    '11': '11_opus_master.csv',
                    '12': '12_opus_master.csv',
                    '13': '13_opus_master.csv',
                    '14': '14_opus_master.csv',
                    '15': '15_opus_master.csv',
                    '16': '16_opus_master.csv',
                    '17': '17_opus_master.csv',
                    '18': '18_opus_master.csv',
                    '19': '19_opus_master.csv',
                    '20': '20_opus_master.csv',
                    '21': '21_opus_master.csv',
                    '22': '22_opus_master.csv',
                    '23': '23_opus_master.csv'
                    }
        for sheet in ['10','11','12','13','14','15','16','17','18','19','20','21','22','23']:
#         for sheet in ['10']:
            print "________sheet__________",sheet
    #         worksheet = rb.sheet_by_index(sheet)
            worksheet = rb.sheet_by_name(sheet)
    #         print "________adsadsa_________",rb.sheet_by_name('10')
    #         stop
    #         col_values = worksheet.row_values(0)
    #         region_values = worksheet.row_values(1)
            file_gas = addons.get_module_resource('import_xls/csv_data', file_dic[sheet])
            product_values = {'ELECTRICITY CONTRACT': 
                                  {
                                  '1':{'Baserate': 14,
                                        },
                                  '2':{'Nightsaver': 15,
                                        'RHT':16,
                                          },
                                  '3':{'Baserate': 18,
                                        'Flexirate 2':19
                                        },
                                  '4':{'Nightsaver': 20,
                                        'Flexirate 3':21,
                                        'RHT':22,
                                        'extra': 23,
                                          },
                                  '5':{'Baserate': 25,
                                        'Nightsaver': 26,
#                                         'Flexirate 3':27,
                                          },
                                  '6':{'Baserate': 25,
                                        'Nightsaver': 26,
#                                         'Flexirate 3':27,
                                          },
                                  '7':{'Baserate': 25,
                                        'Nightsaver': 26,
#                                         'Flexirate 3':27,
                                          },
                                  '8':{'Baserate': 25,
                                        'Nightsaver': 26,
#                                         'Flexirate 3':27,
                                          }
                                  }
                              }
                              
                              
            
            
            
            sheet_1_data_gas = first_sheet.sheet_1_opus_price(file_gas,worksheet,product_values,pricelist_name,utility_type,sheet)
            final_lst += sheet_1_data_gas
        pricelist.import_opus_pricelist_ele(db,user,host,password,final_lst)
    elif utility_type == 'Gas':
#         for sheet in ['1 Yr EB w SC','1 Yr EB no SC']:
        for sheet in [0,1]:
            product_values = {
                            'GAS 1 CONTRACT': {'start_col': 1,'end_col':5,'min': 0.0, 'max': 73200.0},
                            'GAS 2 CONTRACT': {'start_col': 6,'end_col':10,'min': 73200.0, 'max': 293000.0},
                            'GAS 3 CONTRACT': {'start_col': 11,'end_col':15,'min': 293000.0, 'max': 73200.0}
                              }
#             worksheet = rb.sheet_by_name(sheet)
            worksheet = rb.sheet_by_index(sheet)
            col_values = worksheet.row_values(5,start_colx=1, end_colx=5)
            file_gas = addons.get_module_resource('import_xls/csv_data', 'master_bg_ele.csv')
            sheet_1_data_gas,product_lst = first_sheet.sheet_1_opus_gas_price(file_gas,col_values,worksheet,pricelist_name,product_values,sheet)
            final_lst += sheet_1_data_gas
            product_final_lst += product_lst
        product_import = pricelist.import_pricelist_total_product(db,user,host,password,product_final_lst,utility_type)
        pricelist.import_pricelist_opus_gas(db,user,host,password,final_lst,utility_type)
    print "__________final_lst___________",final_lst
    return final_lst


def parse_sse_xls_file(xls_file,db,pricelist_name, wizard_obj):
    user = wizard_obj.postgres_config_id.db_user
    host = wizard_obj.postgres_config_id.host_name
    password = wizard_obj.postgres_config_id.db_user_pass
    utility_type = wizard_obj.categ_id and wizard_obj.categ_id.name or False 
    rb = xlrd.open_workbook(xls_file,formatting_info=False,on_demand=False, ragged_rows=False)
    final_lst = []
    data_lst = []
    worksheet = rb.sheet_by_index(0)
    col_values = worksheet.row_values(0)
#     worksheet = rb.sheet_by_name(sheet)
    final_lst = []
    data_lst = []
    file_gas = addons.get_module_resource('import_xls/csv_data', 'master_sheet_cng_gas.csv')
    if utility_type == 'Gas':
        sheet_1_data_gas = first_sheet.sheet_1_sse_gas_price(file_gas,col_values,worksheet,pricelist_name,utility_type,rb)
        pricelist.import_pricelist_sse_gas(db,user,host,password,sheet_1_data_gas,utility_type)
    elif utility_type == 'Electricity':
        stop
        product_lst,sheet_1_data_gas = first_sheet.sheet_1_total_gas_price(file_gas,reader,pricelist_name,utility_type)
        product_import = pricelist.import_pricelist_total_product(db,user,host,password,product_lst,utility_type)
        pricelist.import_total_pricelist_ele(db,user,host,password,sheet_1_data_gas,utility_type)
    final_lst += sheet_1_data_gas
    return final_lst



def parse_ovo_xls_file(xls_file,db,user,host,password,pricelist_name, wizard_obj):
    rb = xlrd.open_workbook(xls_file,formatting_info=False,encoding_override='utf-8-sig')
    final_lst = []
    
    for sheet in [0,1]:
        file = addons.get_module_resource('import_xls/csv_data', 'ovo_master.csv')
        worksheet = rb.sheet_by_index(sheet)
        region_values = [u'Region', u'P3 Better Energy standing charge', u'P3 Better Energy unit rate', u'P3 Greener Energy standing charge', u'P3 Greener Energy unit rate', u'P4 Better Energy standing charge', u'P4 Better Energy Day unit rate', u'P4 Better Energy Night unit rate', u'P4 Greener Energy standing charge', u'P4 Greener Energy Day unit rate', u'P4 Greener Energy Night unit rate', '', '', '', '']
        data_lst = []
        if sheet == 0:
            product_values = {
                              'Baserate':{
                                          '1 year Electricity' : [2,3,4,5,6,7,8,9,10,11,12,13,14,15
                                                                  ],
                                          '2 year Electricity' : [20,21,22,23,24,25,26,27,28,29,30,31,32,33
                                                                  ]
                                        },
                            }
            sheet_1_data = first_sheet.sheet_1_ovo_price(file,product_values, worksheet,region_values,pricelist_name,sheet)
            final_lst +=sheet_1_data

        elif sheet == 1:
            product_values = {
                              'Nightsaver':{
                                          '1 year Electricity' : [2,3,4,5,6,7,8,9,10,11,12,13,14,15
                                                                  ],
                                          '2 year Electricity' : [20,21,22,23,24,25,26,27,28,29,30,31,32,33
                                                                  ]
                                        },
                            }
            sheet_2_data = first_sheet.sheet_1_ovo_price(file,product_values, worksheet,region_values,pricelist_name,sheet)
            final_lst +=sheet_2_data
    pricelist.import_pricelist_ovo(db,user,host,password,final_lst)
    return final_lst





