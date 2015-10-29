# -*- coding: utf-8 -*-
##############################################################################
#
#    Product Images on sale order line and Delivery Order line.
#    Copyright (C) 2012-Today Browse Info Pvt Ltd (<http://www.browseinfo.in>).
#    $autor:
##############################################################################


{
    "name" : "Sale Focus Product Design",
    "category": 'Sale',
    "version" : "1.0",
    'description': """
        This module add the product images on sale order line
    """,
    "depends" : ["sale","report_aeroo","report_aeroo_ooo"],
    "author" : "Browse Info",
    "website" : "http://browseinfo.in",
    "category" : "Generic Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : ['sale_focus.xml','sale_focus_design_report.xml'],
    "active": False,
    "installable": True
}
