import frappe

def execute():
    doc = frappe.get_meta("Payment Entry Reference")
    if doc.has_field("deallocate_payment"):
        return
    doc = frappe.new_doc("Custom Field")
    doc.dt = "Payment Entry Reference"
    doc.label = "Deallocate Payment"
    doc.fieldname = "deallocate_payment"
    doc.insert_after ="payment_term"
    doc.fieldtype = "Button"
    doc.allow_on_submit = 1
    doc.save()
