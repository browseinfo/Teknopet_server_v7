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

class medical_patient_consultation(osv.osv):
    
    _name = 'medical.patient.consultation'
    _description = 'Medical Patient Consultation'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True, readonly=True),
                'state': fields.selection([('draft','Draft'),('open','Open'),('close','Close'),('cancel','Cancel')], 'State'),
                'patient_id': fields.many2one('res.partner', 'Patient'),
                'doctor_id': fields.many2one('hr.employee', 'Doctor'),
                'date_start': fields.date('Date'),
#                 'date_end': fields.date('To'),
                'center_id': fields.many2one('medical.center', 'Medical Center'),
                'sizee': fields.char('Size', size=128),
                'weight': fields.char('Weight', size=128),
                'activity_id': fields.many2one('medical.activity', 'Medical Activity'),
                'speciality_id': fields.many2one('medical.specialty', 'Medical Specialty'),
                'work_accident': fields.boolean('Work Accident'),
                'sentinel_desease_id': fields.many2one('medical.disease', 'Sentinel Desease'),
                'destination_id': fields.many2one('medical.destination', 'Destination'),
                'destination_from_date': fields.date('From Date'),
                'destination_to_date': fields.date('To Date'),
                'destination_from': fields.char('Destination From', size=128),
                'destination_to': fields.char('Destination To', size=128),
                'destination_period_from': fields.many2one('account.period', 'Destination From Period'),
                'destination_period_to': fields.many2one('account.period', 'Destination To Period'),
                'om_ecg': fields.selection([('ok','OK'),('nok','NOK'),('not_done','Not Done')], 'OM ECG'),
                'om_rxt': fields.selection([('ok','OK'),('nok','NOK'),('not_done','Not Done')], 'OM RXT'),
                'om_audio': fields.selection([('ok','OK'),('nok','NOK'),('not_done','Not Done')], 'OM Audio'),
                'om_visio': fields.selection([('ok','OK'),('nok','NOK'),('not_done','Not Done')], 'OM Visio'),
                'om_oh': fields.selection([('ok','OK'),('nok','NOK'),('not_done','Not Done')], 'OM OH'),
                'om_drug': fields.selection([('ok','OK'),('nok','NOK'),('not_done','Not Done')], 'OM Drug'),
                'om_decision': fields.many2one('medical.om.decision', 'OM Decision'),
                'parent_id': fields.many2one('medical.patient.consultation', 'Medical Patient Consultation'),
                'med_pat_con_line': fields.one2many('medical.patient.consultation', 'parent_id', 'Medical Patient Consultation')
                
                
        }
    
    _defaults = {
                 'work_accident': False,
                 'date_start': time.strftime('%Y-%m-%d'),
                 'destination_from_date': time.strftime('%Y-%m-%d'),
                 'state': 'draft',
                 'name': '/',
                 }
    
    def action_open(self, cr, uid, ids, context={}):
        self.write(cr, uid, ids, {'state': 'open'}, context=context)
        return True
    
    def action_close(self, cr, uid, ids, context={}):
        self.write(cr, uid, ids, {'state': 'close'}, context=context)
        return True
    
    def action_cancel(self, cr, uid, ids, context={}):
        self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
        return True
    
    def create(self, cr, uid, vals, context={}):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'medical.patient.consultation') or '/'
        return super(medical_patient_consultation, self).create(cr, uid, vals, context=context)

medical_patient_consultation()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: