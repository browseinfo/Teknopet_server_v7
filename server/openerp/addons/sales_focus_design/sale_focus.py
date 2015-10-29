# -*- coding: utf-8 -*-
##############################################################################
#
#    Product Images on sale order line and Delivery Order line.
#    Copyright (C) 2012-Today Browse Info Pvt Ltd (<http://www.browseinfo.in>).
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

from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class sale_order_line(osv.Model):
	_name = 'sale.order.line'
	_inherit = 'sale.order.line'
	_columns = {
		'prod_image' : fields.binary('Product Image'),
		'note' : fields.text('Note'),
		'disable': fields.boolean('Disable'),
		
		}

	_defaults = {
		'disable': False,		
				}
		
	def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
	uom=False, qty_uos=0, uos=False, name='', partner_id=False,
	lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False,prod_image=False, context=None):
		context = context or {}
		product_uom_obj = self.pool.get('product.uom')
		partner_obj = self.pool.get('res.partner')
		product_obj = self.pool.get('product.product')
		warning = {}
		res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
		uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
		lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
		if not product:
			res['value'].update({'product_packaging': False})
			return res

		#update of result obtained in super function
		res_packing = self.product_packaging_change(cr, uid, ids, pricelist, product, qty, uom, partner_id, packaging, context=context)
		res['value'].update(res_packing.get('value', {}))
		warning_msgs = res_packing.get('warning') and res_packing['warning']['message'] or ''
		product_obj = product_obj.browse(cr, uid, product, context=context)
		res['value']['delay'] = (product_obj.sale_delay or 0.0)
		res['value']['type'] = product_obj.procure_method

		#check if product is available, and if not: raise an error
		uom2 = False
		if uom:
			uom2 = product_uom_obj.browse(cr, uid, uom)
		if product_obj.uom_id.category_id.id != uom2.category_id.id:
			uom = False
		if not uom2:
			uom2 = product_obj.uom_id
		compare_qty = float_compare(product_obj.virtual_available * uom2.factor, qty * product_obj.uom_id.factor, precision_rounding=product_obj.uom_id.rounding)
		if (product_obj.type=='product') and int(compare_qty) == -1 \
		and (product_obj.procure_method=='make_to_stock'):
			warn_msg = _('You plan to sell %.2f %s but you only have %.2f %s available !\nThe real stock is %.2f %s. (without reservations)') % \
			(qty, uom2 and uom2.name or product_obj.uom_id.name,
			max(0,product_obj.virtual_available), product_obj.uom_id.name,
			max(0,product_obj.qty_available), product_obj.uom_id.name)
			warning_msgs += _("Not enough stock ! : ") + warn_msg + "\n\n"

		#update of warning messages
		if warning_msgs:
			warning = {
			'title': _('Configuration Error!'),
			'message' : warning_msgs
			}
		res.update({'warning': warning})
		res['value']['prod_image'] =  product_obj.image_small or False
		return res


sale_order_line()

class sale_order(osv.Model):
	_name = 'sale.order'
	_inherit = 'sale.order'

	def _prepare_order_line_move(self, cr, uid, order, line, picking_id, date_planned, context=None):
		location_id = order.shop_id.warehouse_id.lot_stock_id.id
		output_id = order.shop_id.warehouse_id.lot_output_id.id
		return {
			'name': line.name,
			'picking_id': picking_id,
			'product_id': line.product_id.id,
			'prod_image':line.prod_image,
			'date': date_planned,
			'date_expected': date_planned,
			'product_qty': line.product_uom_qty,
			'product_uom': line.product_uom.id,
			'product_uos_qty': (line.product_uos and line.product_uos_qty) or line.product_uom_qty,
			'product_uos': (line.product_uos and line.product_uos.id)\
				or line.product_uom.id,
			'product_packaging': line.product_packaging.id,
			'partner_id': line.address_allotment_id.id or order.partner_shipping_id.id,
			'location_id': location_id,
			'location_dest_id': output_id,
			'sale_line_id': line.id,
			'tracking_id': False,
			'state': 'draft',
			#'state': 'waiting',
			'company_id': order.company_id.id,
			'price_unit': line.product_id.standard_price or 0.0
		}
sale_order()
	

