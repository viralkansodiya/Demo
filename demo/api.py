import frappe
from erpnext.accounts.utils import get_balance_on

@frappe.whitelist(allow_guest=True)
def get_ratio(filters =None):
    filters = frappe.parse_json(filters)
    doc = frappe.get_doc("Financial Retio" , filters.get('finatial_ratio'))
    balance_of_nominator = 0
    for row in doc.nominator:
        balance_of_nominator += get_balance_on(account=row.account, company=filters.get('company'))
    balance_of_denominator = 0
    for row in doc.denominator:
        balance_of_denominator += get_balance_on(account=row.account, company=filters.get('company'))
    return abs(balance_of_nominator/balance_of_denominator)

@frappe.whitelist()
def get_customer_item_name(doc):
    doc = frappe.parse_json(doc)
    data = {}
    for row in doc.get('items'):
        ref_code= frappe.db.get_value("Item Customer Detail", 
                                      {"parent":row.get('item_code'), "customer_name":doc.get('customer') },
                                      "ref_code")
        if ref_code:
            data.update({row.get('item_code'):ref_code})
    return data

