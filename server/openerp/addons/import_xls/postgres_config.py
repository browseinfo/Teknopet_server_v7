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

class postgres_config(osv.osv):
    
    _name = 'postgres.config'
    
    _columns = {
                'db_user': fields.char('Postgres User', size=256, required=True),
                'host_name': fields.char('Host Name', size=256, required=True),
                'db_user_pass': fields.char('Postgres User Password', size=256, required=True),
                }
    
    _defaults = {
                 'db_user': 'postgres',
                 'host_name': 'localhost',
                 'db_user_pass': 'postgres',
                 }
    
postgres_config()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
