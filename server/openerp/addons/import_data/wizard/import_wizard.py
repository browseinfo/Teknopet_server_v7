# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) Browse Info Pvt Ltd (<http://www.browseinfo.in>).
#    $autor:
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


from openerp.osv import osv, fields
import time
from openerp.tools.translate import _
from datetime import datetime
import csv
import base64
import cStringIO

class import_data(osv.osv_memory):
    _name = 'import.data'
    _columns={
              'file': fields.binary('Upload file'),
              }

    def import_file(self, cr, uid, ids, context=None):
        if context is None:
                context = {}
        language = context.get('lang')
        context.update({'lang': language})
        
        picking_obj = self.pool.get('stock.picking')
        location_obj = self.pool.get('stock.location')
        move_obj = self.pool.get('stock.move')
        self_browse = self.browse(cr, uid, ids)
        for obj in self_browse:
            if not obj.file:
                raise osv.except_osv(_('Import Error!'), _('Please Select Valid File.'))
            else:
                file_data = base64.decodestring(obj.file)
                input = cStringIO.StringIO(file_data)
                reader = csv.reader(input,delimiter='\t')
                for row in reader:
                    picking_search = picking_obj.search(cr, uid, [('branch_id.name','=',row[0]),('origin','=',row[1])])
                    source_location_search = location_obj.search(cr, uid, [('branch_id.name','=',row[0]),('name','=',row[2])])
                    destination_location_search = location_obj.search(cr, uid, [('branch_id.name','=',row[0]),('name','=',row[3])])
#                     if source_location_search and destination_location_search:
                    picking_obj.write(cr, uid, picking_search, {'src_location_id': source_location_search[0],
                                                                'location_id': destination_location_search[0]})
                    picking_browse = picking_obj.browse(cr, uid, picking_search)
                    res_branch_search = self.pool.get('res.branch').search(cr, uid, [('name','=',row[0])])
                    print '____________________res_branch_search__________',res_branch_search
                    for picking in picking_browse:
                        for line in picking.move_lines:
                            move_obj.write(cr, uid, [line.id], {'location_id': source_location_search[0],
                                                                'location_dest_id': destination_location_search[0],
                                                                'branch_id': res_branch_search[0]
                                                                })
                    
                    
        return True
    
