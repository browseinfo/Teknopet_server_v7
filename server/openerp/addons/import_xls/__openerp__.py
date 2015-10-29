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


{
    "name": "Utility Renewals Module For Import Pricelist",
    "version": "1.0",
    "depends": ['base','utility_renewals'],
    "author": "Tech-Receptives Solutions Pvt. Ltd.",
    "category": "Custom Made",
    "description": """
    This module provide :
    Customization for Utility Renewals
    """,
    "init_xml": [],
    'update_xml': [
                   'wizard/import_xls_wizard_view.xml',
                   'wizard/import_cng_prices_view.xml',
                   'wizard/import_total_gas_power_price_view.xml',
                   'wizard/import_easy_utility_prices_view.xml',
                   'wizard/import_bg_prices_view.xml',
                   'wizard/import_opus_prices_view.xml',
                   'wizard/import_sse_prices_view.xml',
                   'wizard/import_ovo_price_view.xml',
					
                   'postgres_config_view.xml',
                   ],
    'demo_xml': [
                 ],
    'js':[
          ],
    'qweb':[
            ],
    'installable': True,
    'application': True,
    "sequence": 2,
    'active': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
