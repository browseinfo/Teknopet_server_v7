# -*- coding: utf-8 -*-
##############################################################################
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

# from openerp.report import report_sxw
# from openerp.osv import osv
# from openerp.tools.translate import _
# import random
# from datetime import datetime,date, timedelta as td



import addons
import xmlrpclib
import psycopg2
from openerp import netsvc
import base64
import urllib
import binascii
import time
import operator
import itertools
from datetime import datetime
from dateutil import relativedelta
from report import report_sxw
from openerp.tools.amount_to_text_en import amount_to_text
from openerp.report import report_sxw
import os
from openerp.modules import get_module_resource, get_module_path


class Parser(report_sxw.rml_parse):
        
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.totals = 0.0
        self.subtotals = 0.0
        self.subtotal_price = 0.0
        self.labor_cost = 0.0
        self.nonlabor_cost = 0.0
        self.total_cost = 0.0
        self.localcontext.update({
            'time': time,
            'get_data': self._get_data,
            'get_totals': self.get_totals,
            'get_subtotals': self.get_subtotals,
            'get_subtotal_price': self.get_subtotal_price,
            'get_labor_cost': self.get_labor_cost,
            'get_nonlabor_cost': self.get_nonlabor_cost,
            'get_total_cost': self.get_total_cost,
            'get_static_data': self._get_static_data,
        })
    
    
    def get_totals(self):
        self.totals += (self.subtotals * 0.2)
        return self.totals

    def get_labor_cost(self):
        self.labor_cost += (self.totals * 200)
        return self.labor_cost

    def get_nonlabor_cost(self):
        self.nonlabor_cost += self.subtotal_price
        return self.nonlabor_cost

    def get_total_cost(self):
        self.total_cost = (self.labor_cost + self.nonlabor_cost)
        return self.total_cost

    def get_subtotals(self):
        return self.subtotals * 0.2

    def get_subtotal_price(self):
        return self.subtotal_price


    def _get_data(self, obj):
        sale_obj = self.pool.get('sale.order')
        line_obj = self.pool.get('sale.order.line')
        res = []
        line_name = []
        if obj:
            sale = sale_obj.browse(self.cr, self.uid, obj.id)
            for line in sale.order_line:
                if line.disable:
                    res.append({
                                'disable': line.disable,
                                'prod_image': line.prod_image,
                                'name': line.name or '',
                                'categ_id': line.product_id.categ_id.name,
                                'product_id': line.product_id.name,
                                'product_uom_qty':line.product_uom_qty or 0,
                                'price_unit': line.price_unit,
                                'description': line.name,
                                'note': line.note or '',
                                'totals': self.totals,
                            })
                    self.totals += (line.product_uom_qty)
                    self.subtotals += (line.product_uom_qty)
                    self.subtotal_price += (line.price_unit)
            newlist = sorted(res, key=lambda k: k['name'])
            groups = itertools.groupby(newlist, key=operator.itemgetter('categ_id'))
            result = [{'categ_id':k,'values':[x for x in v]} for k,v in groups]
            print '________result______',result
            return result

    def _get_static_data(self, obj):
        product_obj = self.pool.get('product.product')
        product_id = product_obj.search(self.cr, self.uid ,[('name','=','quote template image')])
        img_browse = product_obj.browse(self.cr, self.uid, product_id[0]).image
        return img_browse 
    
    
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: