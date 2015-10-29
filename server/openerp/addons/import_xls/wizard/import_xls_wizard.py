# -*- coding: utf-8 -*-
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.tech-receptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
import xlrd
import tempfile
from tempfile import TemporaryFile
import cStringIO
import os
import base64
from import_xls import xls_parser as parser
import sys
import psycopg2
import psycopg2.extras
import xmlrpclib
import traceback
import time
import datetime
import calendar

class import_xls_wizard(osv.osv_memory):
    _name = 'import.xls.wizard'
    _description = 'Import xls wizard'
    
    def _get_postgres_config(self, cr, uid, context={}):
        postgres_config_id = self.pool.get('postgres.config').search(cr, uid, [], context=context)
        return postgres_config_id and postgres_config_id[0] or False 
    
    
    _columns = {
                'file': fields.binary('Upload file'),
                'partner_id': fields.many2one('res.partner', 'Supplier', required=True),
                'name': fields.char('Pricelist Name', size=256, required=True),
                'contract_type_id': fields.many2one('contract.type', 'Contract Type', required=True),
                'check_format': fields.boolean('Merged (05,06,07,08) profiles ?'),
                'start_date': fields.date('Start Date', required=True),
                'end_date': fields.date('End Date', required=True),
                'postgres_config_id': fields.many2one('postgres.config', 'Postgres Configuration')
                }
    
    _defaults = {
                 'check_format': True,
                 'postgres_config_id': _get_postgres_config
                 }
    
#     def get_month_day_range(self,date):
#         """
#         For a date 'date' returns the start and end date for the month of 'date'.
#     
#         Month with 31 days:
#         >>> date = datetime.date(2011, 7, 27)
#         >>> get_month_day_range(date)
#         (datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))
#     
#         Month with 28 days:
#         >>> date = datetime.date(2011, 2, 15)
#         >>> get_month_day_range(date)
#         (datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))
#         """
#         first_day = date.replace(day = 1)
#         last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])
#         return first_day, last_day
    
    
    def save_as_temp_file(self, data):
        with tempfile.NamedTemporaryFile(delete=False,
                suffix=".xls") as f:
            f.write(base64.decodestring(data))
            return f.name
    
    def create_pricelist(self, cr, uid, partner, name, contract_type_id,start_date,end_date,context={}):
#         date = datetime.date.today()
#         final_date = self.get_month_day_range(date)
#         first_date = final_date[0].strftime('%Y-%m-%d')
#         last_date = final_date[1].strftime('%Y-%m-%d')
        res = {
               'ELECTRICITY 1 YEAR CONTRACT': False,
               'ELECTRICITY 2 YEAR CONTRACT': False,
               'ELECTRICITY 3 YEAR CONTRACT': False,
               'GAS 1 YEAR CONTRACT': False,
               'GAS 2 YEAR CONTRACT': False,
               'GAS 3 YEAR CONTRACT': False,
               }
        pricelist_pool = self.pool.get('product.pricelist')
        for pricelist in [1,2,3]:
            default_fields = pricelist_pool.fields_get(cr, uid, context=context)
            default_data = pricelist_pool.default_get(cr, uid, default_fields, context=context)
            default_data.update({
                                 'name': name+' Electricity - '+str(pricelist)+' Year',
                                 'start_date': start_date,
                                 'end_date': end_date,
                                 'utility_type': 'ele',
                                 'duration': str(pricelist),
                                 'contract_type_id': contract_type_id,
                                 'partner_id': partner.id,
                                 })
            if pricelist == 1:
                res['ELECTRICITY 1 YEAR CONTRACT'] = default_data['name']
            elif pricelist == 2:
                res['ELECTRICITY 2 YEAR CONTRACT'] = default_data['name']
            elif pricelist == 3:
                res['ELECTRICITY 3 YEAR CONTRACT'] = default_data['name']
            pricelist_pool.create(cr, uid, default_data, context=context)
            cr.commit()
        for pricelist_gas in [1,2,3]:
            default_fields_gas = pricelist_pool.fields_get(cr, uid, context=context)
            default_data_gas = pricelist_pool.default_get(cr, uid, default_fields_gas, context=context)
            default_data_gas.update({
                                 'name': name+' Gas - '+str(pricelist_gas)+' Year',
                                 'start_date': start_date,
                                 'end_date': end_date,
                                 'utility_type': 'gas',
                                 'duration': str(pricelist_gas),
                                 'contract_type_id': contract_type_id,
                                 'partner_id': partner.id,
                                 })
            if pricelist_gas == 1:
                res['GAS 1 YEAR CONTRACT'] = default_data_gas['name']
            elif pricelist_gas == 2:
                res['GAS 2 YEAR CONTRACT'] = default_data_gas['name']
            elif pricelist_gas == 3:
                res['GAS 3 YEAR CONTRACT'] = default_data_gas['name']
            pricelist_pool.create(cr, uid, default_data_gas, context=context)
            cr.commit()
        return res
        
    def import_file(self, cr, uid, ids, context={}):
        for self_obj in self.browse(cr, uid, ids, context=context):
            if not self_obj.postgres_config_id:
                raise osv.except_osv(('Invalid Data!'),("Please Defined Postgres Configuration!"))
            try:
                conn = psycopg2.connect(("dbname=%s user=%s host=%s password=%s")%(cr.dbname,self_obj.postgres_config_id.db_user,str(self_obj.postgres_config_id.host_name),self_obj.postgres_config_id.db_user_pass))
            except Exception,e:
                raise osv.except_osv(('Invalid Data!'),("%s.")%(e))
            pricelist_name = self.create_pricelist(cr, uid, self_obj.partner_id, self_obj.name, self_obj.contract_type_id.id,self_obj.start_date,self_obj.end_date,context=context)
            file_name = self.save_as_temp_file(self_obj.file)
             
            file_lst = parser.read_xls.parse_xls_file(file_name, cr.dbname, self_obj.postgres_config_id.db_user,str(self_obj.postgres_config_id.host_name), self_obj.postgres_config_id.db_user_pass,pricelist_name, self_obj)
            file_lst.append(file_name)
        for file in file_lst:
            os.remove(file)
        return True
    
import_xls_wizard()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: