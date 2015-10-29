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
import datetime
import dateutil

class res_partner(osv.osv):
    
    _inherit = 'res.partner'
    
    def _get_patient_age(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for self_obj in self.browse(cr, uid, ids, context=context):
            res[self_obj.id] = False
            if self_obj.patient_birthdate:
                birthdate = datetime.datetime.strptime(self_obj.patient_birthdate, "%Y-%m-%d")
                now = datetime.datetime.utcnow()
                now = now.date()
                age = dateutil.relativedelta.relativedelta(now, birthdate)
                res[self_obj.id] = age.years
        return res
    
    _columns = {
                'is_patient': fields.boolean('Patient'),
#                 'is_doctor': fields.boolean('Doctor'),
                'patient_birthdate': fields.date('Birthdate'),
                'patient_age': fields.function(_get_patient_age, type="char", size=32, string='Age', method=True),
                'patient_staff_number': fields.char('Staff Number', size=128),
                'patient_sex': fields.selection([('male','Male'),('female','Female')], 'Sex'),
                'patient_status_id': fields.many2one('medical.patient.status', 'Patient Status'),
                'patient_dependant_relationship': fields.selection([('spouse','Spouse'),('child','Children')], 'Dependant Relationship'),
#                 'doctor_specialty_ids': fields.many2many('medical.specialty', 'doctor_spe_rel', 'partner_id', 'specialty_id', 'Doctor Specialty'),
                'is_dependant': fields.boolean('Dependant'),
                'patent_dependant_employee_id': fields.many2one('res.partner', 'Patient Dependant Employee'),
#                 'patient_consultation_line': fields.one2many('medical.patient.consultation', 'patient_id', 'Patient Consultation Line'),
#                 'doctor_consultation_line': fields.one2many('medical.patient.consultation', 'doctor_id', 'Doctor Consultation Line'),
        }
    
    _defaults = {
                 'is_patient': False,
                 'is_dependant': False
                 }
    
    def onchange_patient_status(self, cr, uid, ids, status_id, context={}):
        res = {'value': {'is_dependant': False}, 'domain': {}}
        if status_id:
            if self.pool.get('medical.patient.status').browse(cr, uid, status_id, context=context).name == 'Dependant':
                res['value']['is_dependant'] = True
        return res


res_partner()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: