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
import time

class medicament_line(osv.osv):
    
    _name="medicament.line"
    
    _columns = {
                'medicament_id': fields.many2one('product.product', 'Medicament'),
                'medicament_qty': fields.float('Medicament Quantity'),
                'med_pat_pres_id': fields.many2one('medical.patient.prescription', 'Medical Patient Prescription'),
                }
    
medicament_line()

class examination_line(osv.osv):
    
    _name="examination.line"
    
    _columns = {
                'examination_id': fields.many2one('medical.examination', 'Examination'),
                'examination_note': fields.text('Examination Description'),
                'med_pat_pres_id': fields.many2one('medical.patient.prescription', 'Medical Patient Prescription'),
                }
    
medicament_line()

class medical_patient_prescription(osv.osv):
    
    _name = 'medical.patient.prescription'
    _description = 'Medical Patient Prescription'
    
    _columns = {
                'consultation_id': fields.many2one('medical.patient.consultation', 'Consultation Id'),
                'medicament_line': fields.one2many('medicament.line', 'med_pat_pres_id', 'Medicament Line'),
                'examination_line': fields.one2many('examination.line', 'med_pat_pres_id', 'Examination Line'),
                }


medical_patient_prescription()    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: