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