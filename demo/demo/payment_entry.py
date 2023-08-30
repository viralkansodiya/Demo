import frappe
from frappe.utils import (
    cint,
    create_batch,
    cstr,
    flt,
    formatdate,
    get_number_format_info,
    getdate,
    now,
    nowdate,
)
from frappe import _, qb, throw


@frappe.whitelist()
def deallocate_payment(child_doc_name,parent_doc_name,reference_doctype,reference_name,self):
    self = frappe.json.loads(self)
    if reference_doctype in ['Sales Invoice','Purchase Invoice']:
        frappe.db.sql(f"delete from `tabPayment Entry Reference` where name = '{child_doc_name}'")
        doc = frappe.get_doc("Payment Entry",parent_doc_name)
        doc.set_amounts()

        doc.db_update()
        doc.make_gl_entries(cancel=1)
        doc.make_gl_entries(cancel=0)	
        if self.get('payment_type') == "Receive":
            account_type = 'Receivable'
            account = self.get('paid_from')
        if self.get('payment_type') == "Pay":
            account_type = 'Payable'
            account = self.get('paid_to')
        # frappe.throw(str(self.get('party_type') +" "+ account_type+" "+self.get("party")+" "+ self.get('paid_from')))
        frappe.db.sql("""Update  `tabPayment Ledger Entry` 
                        SET delinked=1,modified=%(date)s,modified_by=%(user)s 
                        WHERE company=%(company)s AND account_type=%(account_type)s
                        AND account=%(account)s  AND party=%(party)s
                        AND voucher_type='Payment Entry' AND voucher_no=%(name)s AND against_voucher_type=%(against_voucher_type)s 
                        AND against_voucher_no=%(against_voucher_no)s""",
                        { 
                            'date': now(), 
                            "user":frappe.session.user ,
                            "company":self.get('company'),
                            "account_type":account_type,
                            "account":account,
                            
                            "name":self.get('name'),
                            "against_voucher_type":reference_doctype,
                            'against_voucher_no':reference_name,
                            "party":self.get("party")

                        }
                    )
        update_outstanding_amt(
            doc.paid_from if doc.payment_type == "Receive" else doc.paid_to,
            doc.party_type,
            doc.party,
            reference_doctype,
            reference_name
        )

        ref_doc = frappe.get_doc(reference_doctype, reference_name)
        ref_doc.delink_advance_entries(doc.name)


        return "Payment Unallocated Successfully"
    else:
        return "Not able to Unallocate the Payment"


def update_outstanding_amt(account, party_type, party, against_voucher_type, against_voucher):
    if party_type and party:
        party_condition = " and party_type={0} and party={1}"\
            .format(frappe.db.escape(party_type), frappe.db.escape(party))
    else:
        party_condition = ""

    if against_voucher_type == "Sales Invoice":
        party_account = frappe.db.get_value(against_voucher_type, against_voucher, "debit_to")
        account_condition = "and account in ({0}, {1})".format(frappe.db.escape(account), frappe.db.escape(party_account))
    else:
        account_condition = " and account = {0}".format(frappe.db.escape(account))

    # get final outstanding amt
    bal = flt(frappe.db.sql("""
        select sum(debit_in_account_currency) - sum(credit_in_account_currency)
        from `tabGL Entry`
        where is_cancelled = 0 and against_voucher_type=%s and against_voucher=%s
        and voucher_type != 'Invoice Discounting'
        {0} {1}""".format(party_condition, account_condition),
        (against_voucher_type, against_voucher))[0][0] or 0.0)

    if against_voucher_type == 'Purchase Invoice':
        bal = -bal

    if against_voucher_type in ["Sales Invoice", "Purchase Invoice"]:
        ref_doc = frappe.get_doc(against_voucher_type, against_voucher)

        # Didn't use db_set for optimisation purpose
        ref_doc.outstanding_amount = bal
        frappe.db.set_value(against_voucher_type, against_voucher, 'outstanding_amount', bal)

        ref_doc.set_status(update=True)