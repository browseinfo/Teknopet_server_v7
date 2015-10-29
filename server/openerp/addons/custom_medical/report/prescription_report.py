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

from openerp.osv import osv
from openerp.report import report_sxw
from datetime import datetime
from openerp import pooler
import time

class report_prescription(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context=None):
        
        super(report_prescription, self).__init__(cr, uid, name, context=context)
        
        self.localcontext.update({
                                  
                                })
        self.context = context
        
        
report_sxw.report_sxw('report.report.prescription','medical.patient.prescription', 
                      'addons/custom_medical/report/prescription_report.rml', 
                      parser=report_prescription,
                      header='internal')

