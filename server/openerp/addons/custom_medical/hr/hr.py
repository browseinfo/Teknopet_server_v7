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
#    MERCHANTABILITY or 9FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv

class hr_employee(osv.osv):
    
    _inherit = 'hr.employee'
    
    _columns = {
                'is_prescriber': fields.boolean('Is Prescriber ?')
                }
    
    _defaults = {
                 'is_prescriber': False,
                 }




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: