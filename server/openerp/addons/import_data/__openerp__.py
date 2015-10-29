# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) Browse Info Pvt Ltd (<http://www.browseinfo.in>).
#    $autor:
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
    'name': 'Custom Resa xlsx upload',
    'version': '1.0',
    'category': '',
    'description': """
        This module is for to upload data from xlsx file:
    """,
    'author': 'browseinfo',
    'website': 'http://www.browseinfo.in',
    'depends': ['stock'],
    'init_xml': [],
    'update_xml': [
                   'wizard/import_wizard_view.xml',
                   ],
    'demo_xml': [
    ],
    'test':[
    ],
    'installable': True,
    'certificate': '',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: