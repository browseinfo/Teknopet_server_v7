# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2013 Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
#    Copyright (C) 2013 Open for Small Business Ltd. (<http://www.o4sb.com>)
#    Copyright (C) 2013 Ursa Information Systems Ltd. (<http://www.ursainfosys.com>)
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

import time
from openerp.osv import fields, orm, osv
from datetime import datetime

class base_synchro_server(orm.Model):
    '''Class to store the information regarding server'''

    def name_get(self, cr, uid, ids, context=None):
        result= []
        if not all(ids):
            return result
        for pl in self.browse(cr, uid, ids, context=context):
            rank = pl.name +  '('+pl.server_db + ')'
            result.append((pl.id,rank))
        return result

    _name = "base.synchro.server"
    _description = "Synchronized server"

    _columns = {
        'name': fields.char('Server name', size=64, required=True),
        'server_url': fields.char('Server URL', size=64, required=True),
        'server_port': fields.integer('Server Port', required=True),
        'server_db': fields.char('Server Database', size=64, required=True),
        'login': fields.char('User Name', size=50, required=True),
        'password': fields.char('Password', size=64, required=True),
        'obj_ids': fields.one2many('base.synchro.obj', 'server_id',
                                    'Models', ondelete='cascade'),
    }
    _defaults = {
        'server_port': 8069
    }


class base_synchro_obj(orm.Model):
    '''OpenERP objects to be synchronised'''
    _name = "base.synchro.obj"
    _description = "Register Class"

    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'domain': fields.char('Domain', size=256, required=True),
        'server_id': fields.many2one('base.synchro.server', 'Server',
                                    ondelete='cascade', required=True),
        'model_id': fields.many2one('ir.model', 'Object to synchronize',
                                    required=True),
        'action': fields.selection([('d', 'Download'),
                                   ('u', 'Upload'),
                                   ('b', 'Both')],
                                  'Synchronisation direction', required=True),
        'sequence': fields.integer('Sequence'),
        'active': fields.boolean('Active'),
        'synchronize_date': fields.datetime('Latest Synchronization',
                                            readonly=True),
        'line_id': fields.one2many('base.synchro.obj.line', 'obj_id',
                                   'Ids Affected', ondelete='cascade'),
        'avoid_ids': fields.one2many('base.synchro.obj.avoid', 'obj_id',
                                     'Fields Not Sync.'),
        'branch_ids' :fields.many2many('res.branch', 'base_synchro_obj_res_branch__rel', 'res_branch_id','brach_id', 'Branch'),

    }
    _defaults = {
        'active': True,
        'action': 'd',
        'domain': '[]'
    }
    _order = 'sequence'
    #
    # Return a list of changes: [ (date, id) ]
    #

    def read(self, cr, uid, ids, fields=None, context=None, load="_classic_read"):
        res = super(base_synchro_obj, self).read(cr, uid, ids, [], context=context)
        self.br_id = []
        print "\n resssssssssssssssssss", res
        if res:
            self.br_id = res[0]['branch_ids']
        print "\n br_idddddddddddddddddddd", self.br_id
        return res

    def get_ids(self, cr, uid, object_, dt, domain=None, context=None):
        return self._get_ids(cr, uid, object_, dt, domain, context=context)

    def _get_ids(self, cr, uid, object_, dt, domain=None, context=None):
#         if not domain:
#             domain = ['|', ('branch_id','in', self.br_id), ('branch_id', '=', False)]
#         else:
#             domain = domain + ['|', ('branch_id','in', self.br_id), ('branch_id', '=', False)]

        result = []
        if dt:
            #dt = dt.split()
            domain2 = domain + [('write_date', '>=', dt)]
            domain3 = domain + [('create_date', '>=', dt)]
        else:
            domain2 = domain3 = domain
        print '_____________________object__________________',object_
        print "\n domainnnnnnnnnnnnnnnnnnnnnnnnnnn", domain
        print "\n domain2222222222222222222222222", domain2
        print "\n domain3333333333333333333333333", domain3
        
        ids = self.pool.get(object_).search(cr, uid, domain2, context=context)
        ids += self.pool.get(object_).search(cr, uid, domain3, context=context)
        for r in self.pool.get(object_).perm_read(cr, uid, ids, context=context,
                                                  details=False):
            result.append((r['write_date'] or r['create_date'], r['id'],
                           context.get('action', 'd')))
        print "\n resultttttttttttttttttttttttttttttttt", result
        return result


class base_synchro_obj_avoid(orm.Model):
    """Fields to not synchronize"""
    _name = "base.synchro.obj.avoid"
    _description = __doc__
    _columns = {
        'name': fields.char('Field Name', size=64, required=True),
        'obj_id': fields.many2one('base.synchro.obj', 'Object', required=True,
                                 ondelete='cascade'),
        }


class base_synchro_obj_line(orm.Model):
    '''
    Stores object ids and their corresponding ids
    on the remote server
    '''
    _name = "base.synchro.obj.line"
    _description = "Synchronized instances"
    _columns = {
        'name': fields.datetime('Date', required=True),
        'obj_id': fields.many2one('base.synchro.obj', 'Object',
                                  ondelete='cascade'),
        'local_id': fields.integer('Local Id', readonly=True),
        'remote_id': fields.integer('Remote Id', readonly=True),
    }
    _defaults = {
        'name': fields.datetime.now
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
