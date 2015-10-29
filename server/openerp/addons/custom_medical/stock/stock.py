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

from openerp.osv import fields, osv

class stock_picking(osv.osv):
    
    _inherit = 'stock.picking'
    _description = 'Prescription'
    
    _columns = {
                'is_prescription': fields.boolean('Prescription ?'),
                'prescription_doctor_id': fields.many2one('res.partner', 'Doctor'),
                'prescription_patient_id': fields.many2one('res.partner', 'Patient'),
                'prescription_consultation_id': fields.many2one('medical.patient.consultation', 'Prescription Consultation Id'),
                
        }
    
    _defaults = {
                 'is_prescription': False,
                 }
    


stock_picking()

class stock_picking_out(osv.osv):
    _inherit = ['stock.picking','stock.picking.out']
    _name = 'stock.picking.out'
    
    
    
stock_picking_out()