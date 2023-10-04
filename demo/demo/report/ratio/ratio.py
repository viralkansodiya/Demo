# Copyright (c) 2023, viral patel and contributors
# For license information, please see license.txt

import frappe
from erpnext.accounts.report.general_ledger.general_ledger import get_result
from frappe import _

def execute(filters=None):
	columns, data = [], []
	nominator = get_ledger_of_nominator(filters)
	denominator = get_ledger_of_denominator(filters)
	
	columns = [
		{
			
			'fieldname':"amount",
			'label': _("Amount"),
			'fieldtype': "Float",
	
		}
	]
	data = [{'amount' : nominator / denominator}]
	
	return columns , data

def get_ledger_of_nominator(filters):
	doc = frappe.get_doc("Financial Retio" , filters.get('financial_retio'))
	total_amount_of_nominator = 0
	account = []
	for row in doc.nominator:
		account.append(row.account)
	for d in account:
		doc = frappe.get_doc("Account" , d)
		if doc.is_group:
			child_account = frappe.db.get_list("Account" ,{'lft' : ['<' , doc.lft ] , 'rgt' : ['>' , doc.rgt] ,'is_group' : 0} , pluck='name' )
			for row in child_account:
				filters['account'] = row
			data = get_account_total(filters , row)
			total_amount_of_nominator += data[0].get('amount') or  0
		else:
			filters['account'] = d
			data = get_account_total(filters , d)
			total_amount_of_nominator += data[0].get('amount') or 0
	return total_amount_of_nominator

def get_account_total(filters , d):
	data = frappe.db.sql(f""" SELECT sum(debit - credit) as amount From `tabGL Entry` where account="{d}" and company ="{filters.get('company')}" and is_cancelled = 0 """,as_dict = 1)
	return data
def get_ledger_of_denominator(filters):
	doc = frappe.get_doc("Financial Retio" , filters.get('financial_retio'))
	total_amount_of_denominator = 0
	account = []
	for row in doc.denominator:
		account.append(row.account)
	for d in account:
		doc = frappe.get_doc("Account" , d)
		if doc.is_group:
			child_account = frappe.db.get_list("Account" ,{'lft' : ['<' , doc.lft ] , 'rgt' : ['>' , doc.rgt] ,'is_group' : 0} , pluck='name' )
			for row in child_account:
				filters['account'] = row
			data = get_account_total(filters , row)
			total_amount_of_denominator += data[0].get('amount') or  0
		else:
			filters['account'] = d
			data = get_account_total(filters , d)
			total_amount_of_denominator += data[0].get('amount') or 0
	return abs(total_amount_of_denominator)