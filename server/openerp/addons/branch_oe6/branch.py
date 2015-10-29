# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from datetime import datetime, date
import time
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc



class res_branch(osv.Model):
    _name = 'res.branch'

    _columns = {
        'name': fields.char('Name', required=True),
        'address': fields.text('Address', size=252),
        'telephone_no':fields.char("Telephone No"),
        'company_id': fields.many2one('res.company', 'Company', required=True),
    }


class res_users(osv.Model):
    _inherit = 'res.users'

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
        'branch_ids': fields.many2many('res.branch', id1='user_id', id2='branch_id',string='Branch'),
    }

class sale_order(osv.Model):
    _inherit = 'sale.order'

    def _get_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }


    _defaults = {
        'branch_id': _get_default_branch,
    }

       
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        journal_obj = self.pool.get('account.journal')
        inv_vals = super(sale_order, self)._prepare_invoice(cr, uid, order, lines, context=context)
        journal_ids = journal_obj.search(cr, uid,[('type', '=', 'sale'), ('company_id', '=', order.company_id.id),('branch_id', '=', order.branch_id.id)],limit=1)
        if not journal_ids:
            raise osv.except_osv(_('Error!'),
                _('Please define sales journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
        inv_vals.update({'branch_id' : order.branch_id.id, 'journal_id': journal_ids[0]})
        return inv_vals

    def _prepare_order_picking(self, cr, uid, order, context=None):
        result = super(sale_order, self)._prepare_order_picking(cr, uid, order, context=context)
        result.update({'branch_id': order.branch_id.id})
        return result



class purchase_order(osv.Model):
    _inherit = 'purchase.order'

    def _get_purchase_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id


    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_purchase_default_branch,
    }

    def action_invoice_create(self, cr, uid, ids, context=None):
        res = False
        journal_obj = self.pool.get('account.journal')
        inv_obj = self.pool.get('account.invoice')
        inv_line_obj = self.pool.get('account.invoice.line')
        for order in self.browse(cr, uid, ids, context=context):
            pay_acc_id = order.partner_id.property_account_payable.id
            journal_ids = journal_obj.search(cr, uid, [('type', '=','purchase'),('company_id', '=', order.company_id.id), ('branch_id', '=', order.branch_id.id)], limit=1)
            if not journal_ids:
                raise osv.except_osv(_('Error!'),
                    _('Define purchase journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
            inv_lines = []
            for po_line in order.order_line:
                acc_id = self._choose_account_from_po_line(cr, uid, po_line, context=context)
                inv_line_data = self._prepare_inv_line(cr, uid, acc_id, po_line, context=context)
                inv_line_id = inv_line_obj.create(cr, uid, inv_line_data, context=context)
                inv_lines.append(inv_line_id)
                po_line.write({'invoiced':True, 'invoice_lines': [(4, inv_line_id)]}, context=context)
            inv_data = {
                'name': order.partner_ref or order.name,
                'reference': order.partner_ref or order.name,
                'account_id': pay_acc_id,
                'type': 'in_invoice',
                'partner_id': order.partner_id.id,
                'currency_id': order.pricelist_id.currency_id.id,
                'journal_id': len(journal_ids) and journal_ids[0] or False,
                'invoice_line': [(6, 0, inv_lines)],
                'origin': order.name,
                'fiscal_position': order.fiscal_position.id or False,
                'payment_term': order.payment_term_id.id or False,
                'company_id': order.company_id.id,
                'branch_id': order.branch_id.id
            }
            inv_id = inv_obj.create(cr, uid, inv_data, context=context)
            inv_obj.button_compute(cr, uid, [inv_id], context=context, set_total=True)
            order.write({'invoice_ids': [(4, inv_id)]}, context=context)
            res = inv_id
        return res

    def _prepare_order_picking(self, cr, uid, order, context=None):
        result = super(purchase_order, self)._prepare_order_picking(cr, uid, order, context=context)
        result.update({'branch_id': order.branch_id.id})
        return result


class account_invoice(osv.Model):
    _inherit = 'account.invoice'

    def _get_invoice_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_invoice_default_branch,
    }

    def invoice_pay_customer(self, cr, uid, ids, context=None):
        result = super(account_invoice, self).invoice_pay_customer(cr, uid, ids, context=context)
        inv = self.pool.get('account.invoice').browse(cr, uid, ids[0], context=context)
        result.get('context').update({'default_branch_id': inv.branch_id.id})
        return result


class account_voucher(osv.Model):
    _inherit = 'account.voucher'

    def _get_voucher_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_voucher_default_branch,
    }


class account_invoice_refund(osv.Model):
    _inherit = 'account.invoice.refund'

    def _get_invoice_refund_default_branch(self, cr, uid, context=None):
        if context.get('active_id'):
            ids = context.get('active_id')
            user_pool = self.pool.get('account.invoice')
            branch_id = user_pool.browse(cr, uid, ids, context=context).branch_id and user_pool.browse(cr, uid, ids, context=context).branch_id.id or False
            return branch_id

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_invoice_refund_default_branch,
    }


class account_asset_asset(osv.Model):
    _inherit = 'account.asset.asset'

    def _get_asset_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_asset_default_branch,
    }

class account_bank_statement(osv.Model):
    _inherit = 'account.bank.statement'

    def _get_bankstatement_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_bankstatement_default_branch,
    }

class sale_shop(osv.Model):
    _inherit = 'sale.shop'

    def _get_shop_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_shop_default_branch,
    }

class account_journal(osv.Model):
    _inherit = 'account.journal'

    def _get_journal_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id


    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
        'stock_journal': fields.boolean('Stock Journal'),
        
    }
    _defaults = {
        'branch_id': _get_journal_default_branch,
    }


    def name_get(self, cr, user, ids, context=None):
        if not ids:
            return []
        if isinstance(ids, (int, long)):
            ids = [ids]
        result = self.browse(cr, user, ids, context=context)
        res = []
        for rs in result:
            if rs.currency:
                currency = rs.currency
            else:
                currency = rs.company_id.currency_id
            name = "%s %s (%s)" % (rs.name, rs.branch_id.name, currency.name)
            res += [(rs.id, name)]
        return res


class crossovered_budget(osv.Model):
    _inherit = 'crossovered.budget'

    def _get_budget_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_budget_default_branch,
    }

class stock_picking(osv.Model):
    _inherit = 'stock.picking'

    def _get_stock_picking_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id


    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_stock_picking_default_branch,
    }


class stock_picking_in(osv.Model):
    _inherit = 'stock.picking.in'

    def _get_incoming_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id

    
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_incoming_default_branch,
    }
    
class stock_picking_out(osv.Model):
    _inherit = 'stock.picking.out'

    def _get_delivery_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id
    
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_delivery_default_branch,
    }

class stock_warehouse(osv.Model):
    _inherit = 'stock.warehouse'

    def _get_warehouse_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id
    
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_warehouse_default_branch,
    }

class stock_location(osv.Model):
    _inherit = 'stock.location'

    def _get_location_default_branch(self, cr, uid, context=None):
        user_pool = self.pool.get('res.users')
        branch_id = user_pool.browse(cr, uid, uid, context=context).branch_id and user_pool.browse(cr, uid, uid, context=context).branch_id.id or False
        return branch_id
    
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

    _defaults = {
        'branch_id': _get_location_default_branch,
    }


class product_product(osv.osv):
    _inherit = "product.product"
    
    def get_product_accounts(self, cr, uid, product_id, context=None):
        """ To get the stock input account, stock output account and stock journal related to product.
        @param product_id: product id
        @return: dictionary which contains information regarding stock input account, stock output account and stock journal
        """
        if context is None:
            context = {}
        product_obj = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
        user_obj=self.pool.get('res.users')
        account_journal_obj=self.pool.get('account.journal')
        branch_id = user_obj.browse(cr, uid, [uid], context)[0].branch_id
        journal_id= account_journal_obj.search(cr, uid, [('branch_id', '=', branch_id.id), ('stock_journal', '=', True), ('type', '=', 'general')])

        stock_input_acc = product_obj.property_stock_account_input and product_obj.property_stock_account_input.id or False
        if not stock_input_acc:
            stock_input_acc = product_obj.categ_id.property_stock_account_input_categ and product_obj.categ_id.property_stock_account_input_categ.id or False

        stock_output_acc = product_obj.property_stock_account_output and product_obj.property_stock_account_output.id or False
        if not stock_output_acc:
            stock_output_acc = product_obj.categ_id.property_stock_account_output_categ and product_obj.categ_id.property_stock_account_output_categ.id or False
        
        #journal_id = product_obj.categ_id.property_stock_journal and product_obj.categ_id.property_stock_journal.id or False
        account_valuation = product_obj.categ_id.property_stock_valuation_account_id and product_obj.categ_id.property_stock_valuation_account_id.id or False
        return {
            'stock_account_input': stock_input_acc,
            'stock_account_output': stock_output_acc,
            'stock_journal': journal_id and journal_id[0] ,
            'property_stock_valuation_account_id': account_valuation
        }
        
        
product_product()


    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
