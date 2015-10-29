# -*- coding: utf-8 -*-
import csv
import sys
import psycopg2
import psycopg2.extras
import xmlrpclib
import traceback
import os
import glob

def import_pricelist(db,user,host,password,file_lst):
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
#         print "XXXXXXXXXXXXXXXXXXXXXXX_________________",product_dict
        cur.execute("select name,id from product_pricelist;")
        
        product_pricelist = cur.fetchall()
        product_pricelist_dict = dict(zip(([res_pro['name'] for res_pro in product_pricelist]),[int(res_pro['id']) for res_pro in product_pricelist]))
#         print "_______res_profile_region_dict_______",product_pricelist_dict
        cur.execute("select name,id from res_profile")
        profile_data = cur.fetchall()
        profile_dict = dict(zip([profile['name'] for profile in profile_data],[int(profile['id']) for profile in profile_data]))
#         print "yyyyyyyyyyyyyyyyyyyyyyy_________________",profile_dict
        cur.execute("select code,id from res_region")
        region_data = cur.fetchall()
        region_dict = dict(zip([region['code'] for region in region_data],[int(region['id']) for region in region_data]))
#         print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzZZ____________",region_dict
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    
     
    for file in file_lst:
        print "_______file______import_____",file
        reader = csv.DictReader(open(file, 'r'), delimiter=",")
        for row in reader:
            try:
                col_data = []
                val_data = []
                if row['product_id']:
                    row['product_id'] = product_dict[row['product_id']]
                if row['pricelist_id']:
                    row['pricelist_id'] = product_pricelist_dict[row['pricelist_id']]
                if row['region_id']:
                    row['region_id'] = region_dict[row['region_id']]
                if row['llf_code']:
                    if len(row['llf_code']) == 1:
                        row['llf_code'] = '00'+row['llf_code']
                    elif len(row['llf_code']) == 2:
                        row['llf_code'] = '0'+row['llf_code']
                if row['mtc_code']:
                    if len(row['mtc_code']) == 1:
                        row['mtc_code'] = '00'+row['mtc_code']
                    elif len(row['mtc_code']) == 2:
                        row['mtc_code'] = '0'+row['mtc_code']
                if row['profile_id']:
                    if len(row['profile_id']) == 1:
                        row['profile_id'] = profile_dict["0"+row['profile_id']]
                    else:
                        row['profile_id'] = profile_dict[row['profile_id']]
                 
                for addr in row:
                    if row[addr]:
                        col_data.append('"'+addr+'"')
                        if isinstance(row[addr],str):
                            val_data.append("'"+unicode(row[addr].replace("'","''"),"ISO-8859-1")+"'")                    
                        else:
                            val_data.append("'"+str(row[addr])+"'")
                query = """INSERT INTO res_profile_region ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
                cur.execute(query)
            except Exception, e:
                print row
    #             print query
                print "error",Exception
                print "zzzzzzzzzz",e.message
                print "Unexpected error:", traceback.print_exc(file=sys.stdout)
        conn.commit()
    cur.close()
    conn.close()
    
def import_pricelist_gas(db,user,host,password,file_lst):
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
        print "XXXXXXXXXXXXXXXXXXXXXXX_________________",product_dict
        cur.execute("select name,id from product_pricelist;")
        
        product_pricelist = cur.fetchall()
        product_pricelist_dict = dict(zip(([res_pro['name'] for res_pro in product_pricelist]),[int(res_pro['id']) for res_pro in product_pricelist]))
        print "_______res_profile_region_dict_______",product_pricelist_dict
        cur.execute("select name,id from res_profile")
        profile_data = cur.fetchall()
        profile_dict = dict(zip([profile['name'] for profile in profile_data],[int(profile['id']) for profile in profile_data]))
        print "yyyyyyyyyyyyyyyyyyyyyyy_________________",profile_dict
        cur.execute("select code,id from res_region")
        region_data = cur.fetchall()
        region_dict = dict(zip([region['code'] for region in region_data],[int(region['id']) for region in region_data]))
        print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzZZ____________",region_dict
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    
    # filelist= glob.glob("/home/erp/Downloads/json Strings/*.txt")
    for file in file_lst:
        print "_______file___________",file
        reader = csv.DictReader(open(file, 'r'), delimiter=",")
        for row in reader:
            if row['region_id']:
                try:
                    col_data = []
                    val_data = []
                     
                    if row['product_id']:
                        row['product_id'] = product_dict[row['product_id']]
                    if row['pricelist_id']:
                        row['pricelist_id'] = product_pricelist_dict[row['pricelist_id']]
                    if row['region_id']:
                        row['region_id'] = region_dict[row['region_id']]
                    for addr in row:
                        if row[addr]:
                            col_data.append('"'+addr+'"')
                            if isinstance(row[addr],str):
                                val_data.append("'"+unicode(row[addr].replace("'","''"),"ISO-8859-1")+"'")                    
                            else:
                                val_data.append("'"+str(row[addr])+"'")
                    query = """INSERT INTO res_profile_region_gas ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
                    cur.execute(query)
                except Exception, e:
                    print row
        #             print query
                    print "error",Exception
                    print "zzzzzzzzzz",e.message
                    print "Unexpected error:", traceback.print_exc(file=sys.stdout)
        conn.commit()
    cur.close()
    conn.close()
    
    
def import_pricelist_cng_gas(db,user,host,password,file_lst):
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
        print "XXXXXXXXXXXXXXXXXXXXXXX_________________",product_dict
        cur.execute("select name,id from product_pricelist;")
        
        product_pricelist = cur.fetchall()
        product_pricelist_dict = dict(zip(([res_pro['name'] for res_pro in product_pricelist]),[int(res_pro['id']) for res_pro in product_pricelist]))
        print "_______res_profile_region_dict_______",product_pricelist_dict
        cur.execute("select name,id from res_profile")
        profile_data = cur.fetchall()
        profile_dict = dict(zip([profile['name'] for profile in profile_data],[int(profile['id']) for profile in profile_data]))
        print "yyyyyyyyyyyyyyyyyyyyyyy_________________",profile_dict
        cur.execute("select short_name,id from res_region")
        region_data = cur.fetchall()
        region_dict = dict(zip([region['short_name'] for region in region_data],[int(region['id']) for region in region_data]))
        print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzZZ____________",region_dict
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    
    # filelist= glob.glob("/home/erp/Downloads/json Strings/*.txt")
    
    for file in file_lst:
        print "_______file___________",file
        reader = csv.DictReader(open(file, 'r'), delimiter=",")
        for row in reader:
            if row['region_code']:
                try:
                    col_data = []
                    val_data = []
                     
                    if row['product_id']:
                        row['product_id'] = product_dict[row['product_id']]
                    if row['pricelist_id']:
                        row['pricelist_id'] = product_pricelist_dict[row['pricelist_id']]
                    if row['region_code']:
                        row['region_id'] = region_dict[row['region_code']]
                    del row['region_code']
                    for addr in row:
                        if row[addr]:
                            col_data.append('"'+addr+'"')
                            if isinstance(row[addr],str):
                                val_data.append("'"+unicode(row[addr].replace("'","''"),"ISO-8859-1")+"'")                    
                            else:
                                val_data.append("'"+str(row[addr])+"'")
                    query = """INSERT INTO res_profile_region_gas ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
                    cur.execute(query)
                except Exception, e:
                    print row
        #             print query
                    print "error",Exception
                    print "zzzzzzzzzz",e.message
                    print "Unexpected error:", traceback.print_exc(file=sys.stdout)
        conn.commit()
    cur.close()
    conn.close()
    

def import_pricelist_total_product(db,user,host,password,product_lst,utility_type):
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
#         print "___________product_________________",product_dict
        
        cur.execute("select name,id from product_category;")
        
        product_categ_data = cur.fetchall()
        product_categ_dict = dict(zip(([product_categ['name'] for product_categ in product_categ_data]),[int(product_categ['id']) for product_categ in product_categ_data]))
        print "__________category_________________",product_categ_dict
        
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    
    for p_name in product_lst:
        try:
            col_data = []
            val_data = []
            if not product_dict.has_key(p_name):
#                 print "_______if_______import___product_____"
                res = {
                       'name': p_name,
                       'type': 'consu',
                       'uom_id': 1,
                       'cost_method': 'standard',
                       'uom_po_id': 1,
                       'sale_ok': 1,
                       'categ_id': utility_type == 'Gas' and product_categ_dict.has_key('Gas') and product_categ_dict['Gas'] or utility_type == 'Electricity' and product_categ_dict.has_key('Electricity') and product_categ_dict['Electricity'] or False   
                       }
                for k,addr in res.iteritems():
                    col_data.append('"'+k+'"')
                    if isinstance(addr,str):
                        val_data.append("'"+unicode(addr.replace("'","''"),"ISO-8859-1")+"'")                    
                    else:
                        val_data.append("'"+str(addr)+"'")
#                 print "_________col_data_________",col_data
#                 print "__________val_data________",val_data
                query_template = """INSERT INTO product_template ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
                cur.execute(query_template)
                query_temp_select = """select id from product_template where name='%s'"""%(p_name)
#                 print "___________query_temp_select__________",query_temp_select
                cur.execute(query_temp_select)
                temp_id = cur.fetchall()
                query_insert_product = """insert into product_product ("product_tmpl_id","active") values ('%s','1')"""%(temp_id and temp_id[0].get('id', False) and temp_id[0]['id'])
                cur.execute(query_insert_product)
        except Exception, e:
#             print row
#             print query
            print "error",Exception
            print "zzzzzzzzzz",e.message
            print "Unexpected error:", traceback.print_exc(file=sys.stdout)
        conn.commit()
    cur.close()
    conn.close()



    
def import_pricelist_total_gas(db,user,host,password,file_lst,utility_type):
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
#         print "XXXXXXXXXXXXXXXXXXXXXXX_________________",product_dict
        cur.execute("select name,id from product_pricelist;")
        
        product_pricelist = cur.fetchall()
        product_pricelist_dict = dict(zip(([res_pro['name'] for res_pro in product_pricelist]),[int(res_pro['id']) for res_pro in product_pricelist]))
        print "_______res_profile_region_dict_______",product_pricelist_dict
        cur.execute("select name,id from res_profile")
        profile_data = cur.fetchall()
        profile_dict = dict(zip([profile['name'] for profile in profile_data],[int(profile['id']) for profile in profile_data]))
        print "yyyyyyyyyyyyyyyyyyyyyyy_________________",profile_dict
        cur.execute("select short_name,id from res_region")
        region_data = cur.fetchall()
        region_dict = dict(zip([region['short_name'] for region in region_data],[int(region['id']) for region in region_data]))
        print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzZZ____________",region_dict
        cur.execute("select name,id from res_sub_region")
        sub_region_data = cur.fetchall()
        sub_region_dict = dict(zip([sub_region['name'] for sub_region in sub_region_data],[int(sub_region['id']) for sub_region in sub_region_data]))
        print "_____________sub___region____________",sub_region_dict
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    
    # filelist= glob.glob("/home/erp/Downloads/json Strings/*.txt")
    
    for file in file_lst:
        print "_______file___________",file
        reader = csv.DictReader(open(file, 'r'), delimiter=",")
        for row in reader:
            if row['region_code']:
                try:
                    col_data = []
                    val_data = []
                    if row['product_id']:
                        row['product_id'] = product_dict[row['product_id']]
                    if row['pricelist_id']:
                        row['pricelist_id'] = product_pricelist_dict[row['pricelist_id']]
                    if row['region_code'] and region_dict.has_key(row['region_code']):
                        row['region_id'] = region_dict[row['region_code']]
                    if row['sub_region_id'] and sub_region_dict.has_key(row['sub_region_id']):
                        row['sub_region_id'] = sub_region_dict[row['sub_region_id']]
                    del row['region_code']
                    for addr in row:
                        if row[addr]:
                            col_data.append('"'+addr+'"')
                            if isinstance(row[addr],str):
                                val_data.append("'"+unicode(row[addr].replace("'","''"),"ISO-8859-1")+"'")                    
                            else:
                                val_data.append("'"+str(row[addr])+"'")
                    query = """INSERT INTO res_profile_region_gas ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
#                     print "____________query_____________",query
                    cur.execute(query)
                except Exception, e:
                    print row
        #             print query
                    print "error",Exception
                    print "zzzzzzzzzz",e.message
                    print "Unexpected error:", traceback.print_exc(file=sys.stdout)
        conn.commit()
    cur.close()
    conn.close()


def import_total_pricelist_ele(db,user,host,password,file_lst,utility_type):
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
#         print "XXXXXXXXXXXXXXXXXXXXXXX_________________",product_dict
        cur.execute("select name,id from product_pricelist;")
        
        product_pricelist = cur.fetchall()
        product_pricelist_dict = dict(zip(([res_pro['name'] for res_pro in product_pricelist]),[int(res_pro['id']) for res_pro in product_pricelist]))
#         print "_______res_profile_region_dict_______",product_pricelist_dict
        cur.execute("select name,id from res_profile")
        profile_data = cur.fetchall()
        profile_dict = dict(zip([profile['name'] for profile in profile_data],[int(profile['id']) for profile in profile_data]))
#         print "yyyyyyyyyyyyyyyyyyyyyyy_________________",profile_dict
        cur.execute("select code,id from res_region")
        region_data = cur.fetchall()
        region_dict = dict(zip([region['code'] for region in region_data],[int(region['id']) for region in region_data]))
        print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzZZ____________",region_dict
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    
     
    for file in file_lst:
        print "_______file______import_____",file
        reader = csv.DictReader(open(file, 'r'), delimiter=",")
        for row in reader:
            try:
                col_data = []
                val_data = []
                if row['product_id']:
                    row['product_id'] = product_dict[row['product_id']]
                if row['pricelist_id']:
                    row['pricelist_id'] = product_pricelist_dict[row['pricelist_id']]
                if row['region_id']:
                    row['region_id'] = region_dict[row['region_id']]
                if row['llf_code']:
                    if len(row['llf_code']) == 1:
                        row['llf_code'] = '00'+row['llf_code']
                    elif len(row['llf_code']) == 2:
                        row['llf_code'] = '0'+row['llf_code']
                if row['mtc_code']:
                    if len(row['mtc_code']) == 1:
                        row['mtc_code'] = '00'+str(int(row['mtc_code']))
                    elif len(row['mtc_code']) == 2:
                        row['mtc_code'] = '0'+str(int(row['mtc_code']))
                if row['profile_id']:
                    if len(row['profile_id']) == 1:
                        row['profile_id'] = profile_dict["0"+row['profile_id']]
                    else:
                        row['profile_id'] = profile_dict[row['profile_id']]
                 
                for addr in row:
                    if row[addr]:
                        col_data.append('"'+addr+'"')
                        if isinstance(row[addr],str):
                            val_data.append("'"+unicode(row[addr].replace("'","''"),"ISO-8859-1")+"'")                    
                        else:
                            val_data.append("'"+str(row[addr])+"'")
                query = """INSERT INTO res_profile_region ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
                cur.execute(query)
            except Exception, e:
                print row
    #             print query
                print "error",Exception
                print "zzzzzzzzzz",e.message
                print "Unexpected error:", traceback.print_exc(file=sys.stdout)
        conn.commit()
    cur.close()
    conn.close()
    
    
def import_easy_pricelist_ele(db,user,host,password,file_lst):
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
#         print "XXXXXXXXXXXXXXXXXXXXXXX_________________",product_dict
        cur.execute("select name,id from product_pricelist;")
        
        product_pricelist = cur.fetchall()
        product_pricelist_dict = dict(zip(([res_pro['name'] for res_pro in product_pricelist]),[int(res_pro['id']) for res_pro in product_pricelist]))
#         print "_______res_profile_region_dict_______",product_pricelist_dict
        cur.execute("select name,id from res_profile")
        profile_data = cur.fetchall()
        profile_dict = dict(zip([profile['name'] for profile in profile_data],[int(profile['id']) for profile in profile_data]))
#         print "yyyyyyyyyyyyyyyyyyyyyyy_________________",profile_dict
        cur.execute("select code,id from res_region")
        region_data = cur.fetchall()
        region_dict = dict(zip([region['code'] for region in region_data],[int(region['id']) for region in region_data]))
#         print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzZZ____________",region_dict
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    
#     print "______import__file_lst______________",file_lst
#     stop 
    for file in file_lst:
        print "_______file______import_____",file
        reader = csv.DictReader(open(file, 'r'), delimiter=",")
        for row in reader:
            try:
                col_data = []
                val_data = []
                if row['product_id']:
                    row['product_id'] = product_dict[row['product_id']]
                if row['pricelist_id']:
                    row['pricelist_id'] = product_pricelist_dict[row['pricelist_id']]
                if row['region_id']:
                    row['region_id'] = region_dict[row['region_id']]
                if row['llf_code']:
                    if len(row['llf_code']) == 1:
                        row['llf_code'] = '00'+row['llf_code']
                    elif len(row['llf_code']) == 2:
                        row['llf_code'] = '0'+row['llf_code']
                if row['mtc_code']:
                    if len(row['mtc_code']) == 1:
                        row['mtc_code'] = '00'+row['mtc_code']
                    elif len(row['mtc_code']) == 2:
                        row['mtc_code'] = '0'+row['mtc_code']
                if row['profile_id']:
                    if len(row['profile_id']) == 1:
                        row['profile_id'] = profile_dict["0"+row['profile_id']]
                    else:
                        row['profile_id'] = profile_dict[row['profile_id']]
                 
                for addr in row:
                    if row[addr]:
                        col_data.append('"'+addr+'"')
                        if isinstance(row[addr],str):
                            val_data.append("'"+unicode(row[addr].replace("'","''"),"ISO-8859-1")+"'")                    
                        else:
                            val_data.append("'"+str(row[addr])+"'")
                query = """INSERT INTO res_profile_region ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
                cur.execute(query)
            except Exception, e:
                print row
    #             print query
                print "error",Exception
                print "zzzzzzzzzz",e.message
                print "Unexpected error:", traceback.print_exc(file=sys.stdout)
#                 stop
        conn.commit()
    cur.close()
    conn.close()
    
    

def import_pricelist_bg_gas_product(db,user,host,password,product_lst,utility_type):
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
#         print "___________product_________________",product_dict
        
        cur.execute("select name,id from product_category;")
        
        product_categ_data = cur.fetchall()
        product_categ_dict = dict(zip(([product_categ['name'] for product_categ in product_categ_data]),[int(product_categ['id']) for product_categ in product_categ_data]))
        print "__________category_________________",product_categ_dict
        
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    
    for p_name in product_lst:
        try:
            col_data = []
            val_data = []
            if not product_dict.has_key(p_name):
#                 print "_______if_______import___product_____"
                res = {
                       'name': p_name,
                       'type': 'consu',
                       'uom_id': 1,
                       'cost_method': 'standard',
                       'uom_po_id': 1,
                       'sale_ok': 1,
                       'categ_id': utility_type == 'Gas' and product_categ_dict.has_key('Gas') and product_categ_dict['Gas'] or utility_type == 'Electricity' and product_categ_dict.has_key('Electricity') and product_categ_dict['Electricity'] or False   
                       }
                for k,addr in res.iteritems():
                    col_data.append('"'+k+'"')
                    if isinstance(addr,str):
                        val_data.append("'"+unicode(addr.replace("'","''"),"ISO-8859-1")+"'")                    
                    else:
                        val_data.append("'"+str(addr)+"'")
#                 print "_________col_data_________",col_data
#                 print "__________val_data________",val_data
                query_template = """INSERT INTO product_template ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
                cur.execute(query_template)
                query_temp_select = """select id from product_template where name='%s'"""%(p_name)
#                 print "___________query_temp_select__________",query_temp_select
                cur.execute(query_temp_select)
                temp_id = cur.fetchall()
                query_insert_product = """insert into product_product ("product_tmpl_id","active") values ('%s','1')"""%(temp_id and temp_id[0].get('id', False) and temp_id[0]['id'])
                cur.execute(query_insert_product)
        except Exception, e:
#             print row
#             print query
            print "error",Exception
            print "zzzzzzzzzz",e.message
            print "Unexpected error:", traceback.print_exc(file=sys.stdout)
        conn.commit()
    cur.close()
    conn.close()
    
    

def import_pricelist_bg_gas(db,user,host,password,file_lst,utility_type):
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
#         print "XXXXXXXXXXXXXXXXXXXXXXX_________________",product_dict
        cur.execute("select name,id from product_pricelist;")
        
        product_pricelist = cur.fetchall()
        product_pricelist_dict = dict(zip(([res_pro['name'] for res_pro in product_pricelist]),[int(res_pro['id']) for res_pro in product_pricelist]))
#         print "_______res_profile_region_dict_______",product_pricelist_dict
        cur.execute("select name,id from res_profile")
        profile_data = cur.fetchall()
        profile_dict = dict(zip([profile['name'] for profile in profile_data],[int(profile['id']) for profile in profile_data]))
#         print "yyyyyyyyyyyyyyyyyyyyyyy_________________",profile_dict
        cur.execute("select name,id from res_region")
        region_data = cur.fetchall()
        region_dict = dict(zip([region['name'] for region in region_data],[int(region['id']) for region in region_data]))
        
        cur.execute("select name,id from payment_type")
        payment_data = cur.fetchall()
        payment_dict = dict(zip([pt['name'] for pt in payment_data],[int(pt['id']) for pt in payment_data]))
        print "payment_dict____________",payment_dict
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    
    # filelist= glob.glob("/home/erp/Downloads/json Strings/*.txt")
    
    for file in file_lst:
        print "_______file___________",file
        reader = csv.DictReader(open(file, 'r'), delimiter=",")
        for row in reader:
            if row['region_id']:
                try:
                    col_data = []
                    val_data = []
                    if row['product_id']:
                        row['product_id'] = product_dict[row['product_id']]
                    if row['pricelist_id']:
                        row['pricelist_id'] = product_pricelist_dict[row['pricelist_id']]
                    if row['region_id']:
                        row['region_id'] = region_dict[row['region_id']]
                    if row['payment_type_id']:
                        row['payment_type_id'] = payment_dict[row['payment_type_id']]
                    for addr in row:
                        if row[addr]:
                            col_data.append('"'+addr+'"')
                            if isinstance(row[addr],str):
                                val_data.append("'"+unicode(row[addr].replace("'","''"),"ISO-8859-1")+"'")                    
                            else:
                                val_data.append("'"+str(row[addr])+"'")
                    query = """INSERT INTO res_profile_region_gas ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
                    cur.execute(query)
                except Exception, e:
                    print row
        #             print query
                    print "error",Exception
                    print "zzzzzzzzzz",e.message
                    print "Unexpected error:", traceback.print_exc(file=sys.stdout)
        conn.commit()
    cur.close()
    conn.close()
    
    
def import_opus_pricelist_ele(db,user,host,password,file_lst):
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
#         print "XXXXXXXXXXXXXXXXXXXXXXX_________________",product_dict
        cur.execute("select name,id from product_pricelist;")
        
        product_pricelist = cur.fetchall()
        product_pricelist_dict = dict(zip(([res_pro['name'] for res_pro in product_pricelist]),[int(res_pro['id']) for res_pro in product_pricelist]))
#         print "_______res_profile_region_dict_______",product_pricelist_dict
        cur.execute("select name,id from res_profile")
        profile_data = cur.fetchall()
        profile_dict = dict(zip([profile['name'] for profile in profile_data],[int(profile['id']) for profile in profile_data]))
#         print "yyyyyyyyyyyyyyyyyyyyyyy_________________",profile_dict
        cur.execute("select code,id from res_region")
        region_data = cur.fetchall()
        region_dict = dict(zip([region['code'] for region in region_data],[int(region['id']) for region in region_data]))
#         print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzZZ____________",region_dict
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    
#     print "______import__file_lst______________",file_lst
#     stop 
    for file in file_lst:
        print "_______file______import_____",file
        reader = csv.DictReader(open(file, 'r'), delimiter=",")
        for row in reader:
            try:
                col_data = []
                val_data = []
                if row['product_id']:
                    row['product_id'] = product_dict[row['product_id']]
                if row['pricelist_id']:
                    row['pricelist_id'] = product_pricelist_dict[row['pricelist_id']]
                if row['region_id']:
                    row['region_id'] = region_dict[row['region_id']]
                if row['llf_code']:
                    if len(row['llf_code']) == 1:
                        row['llf_code'] = '00'+row['llf_code']
                    elif len(row['llf_code']) == 2:
                        row['llf_code'] = '0'+row['llf_code']
                if row['mtc_code']:
                    if len(row['mtc_code']) == 1:
                        row['mtc_code'] = '00'+row['mtc_code']
                    elif len(row['mtc_code']) == 2:
                        row['mtc_code'] = '0'+row['mtc_code']
                if row['profile_id']:
                    if len(row['profile_id']) == 1:
                        row['profile_id'] = profile_dict["0"+row['profile_id']]
                    else:
                        row['profile_id'] = profile_dict[row['profile_id']]
                 
                for addr in row:
                    if row[addr]:
                        col_data.append('"'+addr+'"')
                        if isinstance(row[addr],str):
                            val_data.append("'"+unicode(row[addr].replace("'","''"),"ISO-8859-1")+"'")                    
                        else:
                            val_data.append("'"+str(row[addr])+"'")
                query = """INSERT INTO res_profile_region ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
                cur.execute(query)
            except Exception, e:
                print row
    #             print query
                print "error",Exception
                print "zzzzzzzzzz",e.message
                print "Unexpected error:", traceback.print_exc(file=sys.stdout)
#                 stop
        conn.commit()
    cur.close()
    conn.close()


def import_pricelist_sse_gas(db,user,host,password,file_lst,utility_type):
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
#         print "XXXXXXXXXXXXXXXXXXXXXXX_________________",product_dict
        cur.execute("select name,id from product_pricelist;")
        
        product_pricelist = cur.fetchall()
        product_pricelist_dict = dict(zip(([res_pro['name'] for res_pro in product_pricelist]),[int(res_pro['id']) for res_pro in product_pricelist]))
        print "_______res_profile_region_dict_______",product_pricelist_dict
        cur.execute("select name,id from res_profile")
        profile_data = cur.fetchall()
        profile_dict = dict(zip([profile['name'] for profile in profile_data],[int(profile['id']) for profile in profile_data]))
        print "yyyyyyyyyyyyyyyyyyyyyyy_________________",profile_dict
        cur.execute("select short_name,id from res_region")
        region_data = cur.fetchall()
        region_dict = dict(zip([region['short_name'] for region in region_data],[int(region['id']) for region in region_data]))
        print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzZZ____________",region_dict
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    
    # filelist= glob.glob("/home/erp/Downloads/json Strings/*.txt")
    
    for file in file_lst:
        print "_______file___________",file
        reader = csv.DictReader(open(file, 'r'), delimiter=",")
        for row in reader:
            if row['region_code']:
                try:
                    col_data = []
                    val_data = []
                    if row['product_id']:
                        row['product_id'] = product_dict[row['product_id']]
                    if row['pricelist_id']:
                        row['pricelist_id'] = product_pricelist_dict[row['pricelist_id']]
                    if row['region_code'] and region_dict.has_key(row['region_code']):
                        row['region_id'] = region_dict[row['region_code']]
                    del row['region_code']
                    for addr in row:
                        if row[addr]:
                            col_data.append('"'+addr+'"')
                            if isinstance(row[addr],str):
                                val_data.append("'"+unicode(row[addr].replace("'","''"),"ISO-8859-1")+"'")                    
                            else:
                                val_data.append("'"+str(row[addr])+"'")
                    query = """INSERT INTO res_profile_region_gas ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
                    cur.execute(query)
                except Exception, e:
                    print row
                    print "error",Exception
                    print "zzzzzzzzzz",e.message
                    print "Unexpected error:", traceback.print_exc(file=sys.stdout)
        conn.commit()
    cur.close()
    conn.close()


def import_pricelist_opus_gas(db,user,host,password,file_lst,utility_type):
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
#         print "XXXXXXXXXXXXXXXXXXXXXXX_________________",product_dict
        cur.execute("select name,id from product_pricelist;")
        
        product_pricelist = cur.fetchall()
        product_pricelist_dict = dict(zip(([res_pro['name'] for res_pro in product_pricelist]),[int(res_pro['id']) for res_pro in product_pricelist]))
        print "_______res_profile_region_dict_______",product_pricelist_dict
        cur.execute("select name,id from res_profile")
        profile_data = cur.fetchall()
        profile_dict = dict(zip([profile['name'] for profile in profile_data],[int(profile['id']) for profile in profile_data]))
        print "yyyyyyyyyyyyyyyyyyyyyyy_________________",profile_dict
        cur.execute("select short_name,id from res_region")
        region_data = cur.fetchall()
        region_dict = dict(zip([region['short_name'] for region in region_data],[int(region['id']) for region in region_data]))
        print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzZZ____________",region_dict
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    # filelist= glob.glob("/home/erp/Downloads/json Strings/*.txt")
    
    for file in file_lst:
        print "_______file___________",file
        reader = csv.DictReader(open(file, 'r'), delimiter=",")
        for row in reader:
            if row['region_code']:
                try:
                    col_data = []
                    val_data = []
                    if row['product_id']:
                        row['product_id'] = product_dict[row['product_id']]
                    if row['pricelist_id']:
                        row['pricelist_id'] = product_pricelist_dict[row['pricelist_id']]
                    if row['region_code'] and region_dict.has_key(row['region_code']):
                        row['region_id'] = region_dict[row['region_code']]
                    del row['region_code']
                    for addr in row:
                        if row[addr]:
                            col_data.append('"'+addr+'"')
                            if isinstance(row[addr],str):
                                val_data.append("'"+unicode(row[addr].replace("'","''"),"ISO-8859-1")+"'")                    
                            else:
                                val_data.append("'"+str(row[addr])+"'")
                    query = """INSERT INTO res_profile_region_gas ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
                    cur.execute(query)
                except Exception, e:
                    print row
                    print "error",Exception
                    print "zzzzzzzzzz",e.message
                    print "Unexpected error:", traceback.print_exc(file=sys.stdout)
        conn.commit()
    cur.close()
    conn.close()



def import_pricelist_ovo(db,user,host,password,file_lst):
    
    try:
        conn = psycopg2.connect(("dbname='%s' user='%s' host='%s' password='%s'")%(db,user,host,password))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("select name,id from product_template;")
        
        product_data = cur.fetchall()
        product_dict = dict(zip(([product['name'] for product in product_data]),[int(product['id']) for product in product_data]))
#         print "XXXXXXXXXXXXXXXXXXXXXXX_________________",product_dict
        cur.execute("select name,id from product_pricelist;")
        
        product_pricelist = cur.fetchall()
        product_pricelist_dict = dict(zip(([res_pro['name'] for res_pro in product_pricelist]),[int(res_pro['id']) for res_pro in product_pricelist]))
#         print "_______res_profile_region_dict_______",product_pricelist_dict
        cur.execute("select name,id from res_profile")
        profile_data = cur.fetchall()
        profile_dict = dict(zip([profile['name'] for profile in profile_data],[int(profile['id']) for profile in profile_data]))
#         print "yyyyyyyyyyyyyyyyyyyyyyy_________________",profile_dict
        cur.execute("select code,id from res_region")
        region_data = cur.fetchall()
        region_dict = dict(zip([region['code'] for region in region_data],[int(region['id']) for region in region_data]))
#         print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzZZ____________",region_dict
    except Exception, e:
        print "error",Exception
        print "zzzzzzzzzz",e.message
        print "I am unable to connect to the database"
    
    for file in file_lst:
        print "_______file______import_____",file
        reader = csv.DictReader(open(file, 'r'), delimiter=",")
        for row in reader:
            try:
                col_data = []
                val_data = []
                if row['product_id']:
                    row['product_id'] = product_dict[row['product_id']]
                if row['pricelist_id']:
                    row['pricelist_id'] = product_pricelist_dict[row['pricelist_id']]
                if row['region_id']:
                    row['region_id'] = region_dict[row['region_id']]
                if row['llf_code']:
                    if len(row['llf_code']) == 1:
                        row['llf_code'] = '00'+row['llf_code']
                    elif len(row['llf_code']) == 2:
                        row['llf_code'] = '0'+row['llf_code']
                if row['mtc_code']:
                    if len(row['mtc_code']) == 1:
                        row['mtc_code'] = '00'+row['mtc_code']
                    elif len(row['mtc_code']) == 2:
                        row['mtc_code'] = '0'+row['mtc_code']
                if row['profile_id']:
                    if len(row['profile_id']) == 1:
                        row['profile_id'] = profile_dict["0"+row['profile_id']]
                    else:
                        row['profile_id'] = profile_dict[row['profile_id']]
                 
                for addr in row:
                    if row[addr]:
                        col_data.append('"'+addr+'"')
                        if isinstance(row[addr],str):
                            val_data.append("'"+unicode(row[addr].replace("'","''"),"ISO-8859-1")+"'")                    
                        else:
                            val_data.append("'"+str(row[addr])+"'")
                query = """INSERT INTO res_profile_region ("""+(',').join(col_data)+") "+"""values ("""+(',').join(val_data)+")"
                cur.execute(query)
            except Exception, e:
                print row
                print "error",Exception
                print "xxxxxxx",e.message
                print "Unexpected error:", traceback.print_exc(file=sys.stdout)
        conn.commit()
    cur.close()
    conn.close()


