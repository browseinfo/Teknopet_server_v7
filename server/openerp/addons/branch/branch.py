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

class sale_order(osv.Model):
    _inherit = 'sale.order'

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
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

    def generate_prepurchase_order(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        wf_service = netsvc.LocalService("workflow")
        partner_obj=self.pool.get('res.partner')
        for sale in self.browse(cr, uid, ids, context):
            order = {
                          'name': sale.name,
                          'date_order': sale.date_order,
                          'company_id': sale.company_id and sale.company_id.id or False,
                          'pricelist_id': sale.partner_id.property_product_pricelist_purchase.id,
                          'branch_id': sale.branch_id.id,
                          }
            for line in sale.order_line:
                if not line.product_id.seller_ids:
                    raise osv.except_osv(
                             _('Supplier not found!'),
                            _('First add a supplier in sale order line  Product name:- %s.') % (line.product_id.name,))             
                cr.execute("select min(sequence) from product_supplierinfo where product_id=%s", [line.product_id.id])
                seq = cr.fetchone()[0]
                if seq == None:
                     raise osv.except_osv(_('No Supplier Found'), _('Please first add Supplier for Product.'))
                cr.execute("select name from product_supplierinfo where product_id=%s and sequence=%s", [line.product_id.id, seq])
                partner_id = cr.fetchone()[0]
                cr.execute("select id from prepurchase_order where partner_id=%s and sale_id=%s", [partner_id,sale.id])
                prepurchase_id = cr.fetchone()
                partner  = partner_obj.browse(cr, uid, partner_id, context=context)
                pricelist_id = partner.property_product_pricelist_purchase.id
                if prepurchase_id:
                    cr.execute("select product_id from prepurchase_order_line where sale_id=%s and product_id=%s", [sale.id, line.product_id.id])
                    product_id = cr.fetchone()
                    if product_id:
                        if product_id[0] == line.product_id.id:
                            cr.execute("select product_qty from prepurchase_order_line where sale_id=%s and product_id=%s", [sale.id,line.product_id.id ])
                            product_qty = cr.fetchone()
                            new_qty = product_qty[0] + line.product_uom_qty
                            cr.execute("update prepurchase_order_line set product_qty = %s where sale_id=%s and product_id=%s", [new_qty,sale.id, line.product_id.id])
                        else:
                            order_line = {
                              'name': line.name,
                              'product_id': line.product_id.id,
                              'product_qty': line.product_uom_qty,
                              'product_uom': line.product_uom.id,
                              'company_id': line.company_id.id,
                              'date_planned': sale.date_order,
                              'price_unit' : line.purchase_price,
                              }
                            cr.execute("INSERT INTO prepurchase_order_line(name, order_id, sale_id, sale_line_id, product_id, product_qty,product_uom,company_id, price_unit,date_planned, state) values (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s) returning id" 
                                       ,(order_line['name'],prepurchase_id, sale.id, line.id, order_line['product_id'], order_line['product_qty'], order_line['product_uom'], order_line['company_id'], order_line['price_unit'], order_line['date_planned'], 'draft'))
                    else:
                        order_line = {
                          'name': line.name,
                          'product_id': line.product_id.id,
                          'product_qty': line.product_uom_qty,
                          'product_uom': line.product_uom.id,
                          'company_id': line.company_id.id,
                          'date_planned': sale.date_order,
                          'price_unit' : line.purchase_price,
                          }
                        cr.execute("INSERT INTO prepurchase_order_line(name, order_id, sale_id, sale_line_id, product_id, product_qty,product_uom,company_id, price_unit,date_planned, state) values (%s, %s, %s, %s, %s, %s, %s,  %s,%s, %s, %s) returning id" 
                                       ,(order_line['name'],prepurchase_id, sale.id, line.id,order_line['product_id'], order_line['product_qty'], order_line['product_uom'], order_line['company_id'], order_line['price_unit'], order_line['date_planned'], 'draft'))
                else:
                    cr.execute("INSERT INTO prepurchase_order(name, partner_id, branch_id ,sale_id, date_order,company_id, pricelist_id,  state) values (%s,%s,%s,%s, %s, %s, %s, %s) returning id" 
                    ,(order['name'], partner_id, order['branch_id'],sale.id, order['date_order'], order['company_id'], pricelist_id, 'draft'))
                    order_id = cr.fetchone()[0]
                    order_line = {
                              'name': line.name,
                              'product_id': line.product_id.id,
                              'product_qty': line.product_uom_qty,
                              'product_uom': line.product_uom.id,
                              'company_id': line.company_id.id,
                              'date_planned': sale.date_order,
                              'price_unit' : line.purchase_price,
                              }
                    cr.execute("INSERT INTO prepurchase_order_line(name, order_id, sale_id, sale_line_id, product_id, product_qty,product_uom,company_id, price_unit,date_planned, state) values (%s, %s, %s, %s , %s, %s, %s, %s,%s, %s, %s) returning id" 
                            ,(order_line['name'],order_id, sale.id, line.id, order_line['product_id'],order_line['product_qty'], order_line['product_uom'], order_line['company_id'], order_line['price_unit'], order_line['date_planned'], 'draft'))
        wf_service.trg_validate(uid, 'sale.order', ids[0], 'ppo_sent', cr) 
        return True


    def action_button_confirm(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        project_project = self.pool.get('project.project')
        project_task = self.pool.get('project.task')
        model_obj = self.pool.get('ir.model.data')
        warehouse_obj = self.pool.get('stock.warehouse')
        wf_service = netsvc.LocalService('workflow')
        qty = 0
        ac = []
        for sale in self.browse(cr, uid, ids, context):
            if sale.create_warehouse:
                lot_input_stock_id = model_obj.get_object_reference(cr, uid, 'stock', 'stock_location_stock')
                lot_output_id = model_obj.get_object_reference(cr, uid, 'stock', 'stock_location_output')
                vals = {
                        'name':sale.name,
                        'company_id':sale.company_id and sale.company_id.id or False,
                        'partner_id': sale.partner_id and sale.partner_id.id or False,
                        'lot_input_id': lot_input_stock_id and lot_input_stock_id[1] or False ,
                        'lot_stock_id': lot_input_stock_id and lot_input_stock_id[1] or False,
                        'lot_output_id':lot_output_id and lot_output_id[1] or False,
                        }
                warehouse_obj.create(cr, uid, vals, context=context)
            
            if sale.create_project:
                for line in sale.order_line:
                    qty += line.product_uom_qty
                vals = {
                        'complete_name': sale.name + '_project',
                        'name': sale.name,
                        'user_id': sale.user_id and sale.user_id.id or False,
                        'date_start':sale.date_order,
                        'alias_model': 'project.task',
                        'alias_model_id': 1,
                        'alias_name': sale.name,
                        'planned_hours': qty,
                        'partner_id': sale.partner_id and sale.partner_id.id or False,
                        'currency_id': sale.company_id.currency_id and sale.company_id.currency_id.id or False,
                        }
                project_id = project_project.create(cr, uid, vals, context=context)
                self.write(cr, uid, [sale.id], {'project_sale_id':project_id}, context)
                for rumor in sale.extend_ids:
                    task_val = {
                                'name': rumor.code,
                                'planned_hours': rumor.prod_qty,
                                'remaining_hours': rumor.prod_qty,
                                'description': rumor.task_desc,
                                'project_id': project_id,
                                'state': 'draft',
                                }
                    project_task.create(cr, uid, task_val, context=context)
                    
            order = {
                     'name': sale.name, 
                     'date_from': sale.date_order,
                     'date_to': sale.date_order,
                     'code': sale.name,
                     'company_id': sale.company_id and sale.company_id.id or False,
                     'creating_user_id': sale.user_id and sale.user_id.id or False,
                     'state': 'draft',
                     'branch_id': sale.branch_id.id,
                     }
            cr.execute("INSERT INTO crossovered_budget(name, order_id, branch_id, date_from, date_to,code, company_id, creating_user_id, state) values (%s,%s,%s,%s, %s, %s, %s, %s, %s) returning id" 
                            ,(order['name'], sale.id,order['branch_id'],order['date_from'], order['date_to'], order['code'], order['company_id'],order['creating_user_id'], order['state'] ))
            budget_id = cr.fetchone()[0]
            wf_service.trg_delete(uid, 'crossovered.budget', budget_id , cr)
            wf_service.trg_create(uid, 'crossovered.budget', budget_id , cr)
            cr.execute("select id from account_budget_post where name='Purchases' and code='PUR'")
            budget_post_id = cr.fetchone()[0]
            for line in sale.order_line:
                if line.extend_ids:
                    account_id = line.extend_ids[0].analytic_account_id
                    analytic_account_id = account_id and account_id.id or False
                    if analytic_account_id:
                            budget_line = {
                                       'analytic_account_id': analytic_account_id,
                                       'company_id': line.company_id and line.company_id.id or False,
                                       'crossovered_budget_id':budget_id,
                                       'general_budget_id': budget_post_id,
                                       'date_from': sale.date_order,
                                       'date_to': sale.date_order,
                                       'planned_amount': line.price_subtotal,
                                       'product_id': line.product_id and line.product_id.id or False ,
                                       }
                            cr.execute("INSERT INTO crossovered_budget_lines(analytic_account_id, order_id, company_id, crossovered_budget_id, date_from, date_to,planned_amount,general_budget_id,product_id) values (%s, %s,%s, %s, %s,%s,%s, %s,%s) returning id" 
                                         ,(budget_line['analytic_account_id'], sale.id,budget_line['company_id'], budget_line['crossovered_budget_id'], budget_line['date_from'], budget_line['date_to'], budget_line['planned_amount'],budget_line['general_budget_id'],budget_line['product_id']))
        
        wf_service.trg_validate(uid, 'sale.order', ids[0], 'order_confirm', cr)
        pre_purchase_obj = self.pool.get('prepurchase.order')
        pre_purchase_ids = pre_purchase_obj.search(cr, uid, [('sale_id', '=',ids[0])], context=context)
        if pre_purchase_ids:
            for pre_id in pre_purchase_ids:
                pre_purchase_obj.write(cr, uid, pre_id, {'state': 'confirm'})
                
        # redisplay the record as a sales order
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'view_order_form')
        view_id = view_ref and view_ref[1] or False,
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sales Order'),
            'res_model': 'sale.order',
            'res_id': ids[0],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }


class purchase_order(osv.Model):
    _inherit = 'purchase.order'

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
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


class res_users(osv.Model):
    _inherit = 'res.users'

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
        'branch_ids': fields.many2many('res.branch', id1='user_id', id2='branch_id',string='Branch'),
    }

class account_invoice(osv.Model):
    _inherit = 'account.invoice'

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

class account_journal(osv.Model):
    _inherit = 'account.journal'

    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
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



class prepurchase_order(osv.Model):
    _inherit = 'prepurchase.order'
    
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }

class crossovered_budget(osv.Model):
    _inherit = 'crossovered.budget'
    _columns = {
        'branch_id': fields.many2one('res.branch', 'Branch', required=True),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
