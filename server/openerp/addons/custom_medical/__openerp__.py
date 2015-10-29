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

{
    'name' : 'Medical',
    'version' : '1.1',
    'author' : 'INOOSEV',
    'category' : 'Medical Management',
    'description' : """
        Drive Patients, Doctors, Consultations, Prescriptions, Stocks for a Hospital 
    """,
    'website': '',
    'images' : [],
    'depends' : ['base','account','hr'],
    
    
    'data': [
            'security/security_view.xml',
            'security/ir.model.access.csv',
             "res/res_partner_view.xml",
             'hr/hr_view.xml',
             'res/res_medical_config_view.xml',
             'res/product_view.xml',
             'medical/patient_consultation_view.xml',
             'medical/patient_prescription_view.xml',
#              'stock/stock_view.xml',
            'demo/demo_data_view.xml',
             "menu/menu_view.xml",
             'report/report_menu.xml'
             ],
    
    'demo': [],
    'test': [],
    
    'installable': True,
    'auto_install': False,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: