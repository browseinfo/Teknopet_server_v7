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

class import_opus_prices_wizard(osv.osv_memory):
    _name = 'import.opus.prices.wizard'
    _description = 'Import Opus Prices wizard'
    
    def _get_postgres_config(self, cr, uid, context={}):
        postgres_config_id = self.pool.get('postgres.config').search(cr, uid, [], context=context)
        return postgres_config_id and postgres_config_id[0] or False 
    
    
    _columns = {
                'file': fields.binary('Upload file'),
                'partner_id': fields.many2one('res.partner', 'Supplier', required=True),
                'name': fields.char('Pricelist Name', size=256, required=True),
                'contract_type_id': fields.many2one('contract.type', 'Contract Type', required=True),
                'start_date': fields.date('Start Date', required=True),
                'end_date': fields.date('End Date', required=True),
                'postgres_config_id': fields.many2one('postgres.config', 'Postgres Configuration'),
                'categ_id':fields.many2one('product.category', 'Category', required=True),
                'duration': fields.selection([('1','1'),('2','2'),('3','3')], 'Duration', required=True),
                }
    
    _defaults = {
                 'postgres_config_id': _get_postgres_config
                 }
    
    def save_as_temp_file(self, data):
        with tempfile.NamedTemporaryFile(delete=False,
                suffix=".xls") as f:
            f.write(base64.decodestring(data))
            name = f.name
        f.close()
        return name
    
    def create_pricelist(self, cr, uid, partner, name, contract_type_id,start_date,end_date,categ_name,duration,context={}):
        res = {
               'ELECTRICITY CONTRACT': False,
               'GAS CONTRACT': False
               }
        pricelist_pool = self.pool.get('product.pricelist')
        if categ_name == 'Electricity':
            default_fields = pricelist_pool.fields_get(cr, uid, context=context)
            default_data = pricelist_pool.default_get(cr, uid, default_fields, context=context)
            default_data.update({
                                 'name': name+' Electricity - '+str(duration)+' Year',
                                 'start_date': start_date,
                                 'end_date': end_date,
                                 'utility_type': 'ele',
                                 'duration': str(duration),
                                 'contract_type_id': contract_type_id,
                                 'partner_id': partner.id,
                                 })
            res['ELECTRICITY CONTRACT'] = default_data['name']
            pricelist_pool.create(cr, uid, default_data, context=context)
            cr.commit()
        elif categ_name == 'Gas':
            default_fields_gas = pricelist_pool.fields_get(cr, uid, context=context)
            default_data_gas = pricelist_pool.default_get(cr, uid, default_fields_gas, context=context)
            default_data_gas.update({
                                 'name': name+' Gas - '+str(duration)+' Year',
                                 'start_date': start_date,
                                 'end_date': end_date,
                                 'utility_type': 'gas',
                                 'duration': str(duration),
                                 'contract_type_id': contract_type_id,
                                 'partner_id': partner.id,
                                 })
            res['GAS CONTRACT'] = default_data_gas['name']
            pricelist_pool.create(cr, uid, default_data_gas, context=context)
            cr.commit()
        else:
            raise osv.except_osv(('Invalid Data!'),("You must select Electricity category in pop up interface."))
        return res
        
    def import_file(self, cr, uid, ids, context={}):
        for self_obj in self.browse(cr, uid, ids, context=context):
            if not self_obj.postgres_config_id:
                raise osv.except_osv(('Invalid Data!'),("You must defined postgres configuration in current Database."))
            try:
                conn = psycopg2.connect(("dbname=%s user=%s host=%s password=%s")%(cr.dbname,self_obj.postgres_config_id.db_user,str(self_obj.postgres_config_id.host_name),self_obj.postgres_config_id.db_user_pass))
            except Exception,e:
                raise osv.except_osv(('Invalid Data!'),("%s.")%(e))
            pricelist_name = self.create_pricelist(cr, uid, self_obj.partner_id, self_obj.name, self_obj.contract_type_id.id,self_obj.start_date,self_obj.end_date, self_obj.categ_id and self_obj.categ_id.name or False, self_obj.duration,context=context)
            print "______pricelist_name________",pricelist_name
            file_name = self.save_as_temp_file(self_obj.file)
            file_lst = parser.read_xls.parse_opus_xls_file(file_name, cr.dbname,pricelist_name, self_obj)
            file_lst.append(file_name)
        for file in file_lst:
            os.remove(file)
        return True
    
import_opus_prices_wizard()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: