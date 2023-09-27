import frappe

@frappe.whitelist(allow_guest=True)
def new_alert():
    return {"name":'viral'}

