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

class medical_patient_status(osv.osv):
    
    _name = 'medical.patient.status'
    _description = 'Medical Patient Status'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                
        }
    


medical_patient_status()

class medical_specialty(osv.osv):
    
    _name = 'medical.specialty'
    _description = 'Medical Specialty'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                
        }
    


medical_specialty()


class medical_center(osv.osv):
    
    _name = 'medical.center'
    _description = 'Medical Center'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                
        }
    


medical_center()


class medical_activity(osv.osv):
    
    _name = 'medical.activity'
    _description = 'Medical Activity'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                
        }
    


medical_activity()


class medical_destination(osv.osv):
    
    _name = 'medical.destination'
    _description = 'Medical Destination'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                
        }
    


medical_destination()


class medical_disease_group(osv.osv):
    
    _name = 'medical.disease.group'
    _description = 'Medical disease Group'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                'code': fields.char('Code', size=128, required=True),
                
        }
    

medical_disease_group()


class medical_disease_category(osv.osv):
    
    _name = 'medical.disease.category'
    _description = 'Medical Disease Category'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                'code': fields.char('Code', size=128, required=True),
                'medical_disease_group_id': fields.many2one('medical.disease.group', 'Medical disease Group')
                
        }
    

medical_disease_group()


class medical_disease(osv.osv):
    
    _name = 'medical.disease'
    _description = 'Medical Disease'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                'code': fields.char('Code', size=128, required=True),
                'medical_disease_categ_id': fields.many2one('medical.disease.category', 'Medical disease category')
                
        }
    

medical_disease()

class medical_disease_sentinel(osv.osv):
    
    _name = 'medical.disease.sentinel'
    _description = 'Medical Sentinel Disease'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                
        }
    

medical_disease_sentinel()


class medical_om_decision(osv.osv):
    
    _name = 'medical.om.decision'
    _description = 'Occupational Medicine Decision'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                'code': fields.char('Code', size=128, required=True),
                
        }
    

medical_om_decision()

class medical_act_group(osv.osv):
    
    _name = 'medical.act.group'
    _description = 'Medical Act Group'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                'code': fields.char('Code', size=128, required=True),
                
        }
    

medical_act_group()


class medical_act_category(osv.osv):
    
    _name = 'medical.act.category'
    _description = 'Medical Act Category'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                'code': fields.char('Code', size=128, required=True),
                'med_act_group_id': fields.many2one('medical.act.group', 'Group Id'),
                
        }
    

medical_act_category()


class medical_act(osv.osv):
    
    _name = 'medical.act'
    _description = 'Medical Act'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                'code': fields.char('Code', size=128, required=True),
                'med_act_categ_id': fields.many2one('medical.act.category', 'Category Id'),
                
        }
    

medical_act()


class medical_om_type(osv.osv):
    
    _name = 'medical.om.type'
    _description = 'Medical OM Type'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                
        }
    

medical_om_type()


class medical_medicament_galenic(osv.osv):
    
    _name = 'medical.medicament.galenic'
    _description = 'Medical Medicament Galenic'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                
        }
    

medical_medicament_galenic()


class medical_medicament_speciality(osv.osv):
    
    _name = 'medical.medicament.speciality'
    _description = 'Medical Medicament Speciality'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                
        }
    

medical_medicament_speciality()


class medical_medicament_group(osv.osv):
    
    _name = 'medical.medicament.group'
    _description = 'Medical Medicament Group'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                
        }
    

medical_medicament_group()


class medical_examination(osv.osv):
    
    _name = 'medical.examination'
    _description = 'Medical Examination'
    
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                
        }
    

medical_examination()












# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: