frappe.ui.form.on('Payment Entry Reference', {
	deallocate_payment: function(frm,cdt,cdn){
		let d = locals[cdt][cdn];
		if (frm.doc.docstatus == 1){
			frappe.call({
				method:"demo.demo.payment_entry.deallocate_payment",
				args:{
					"child_doc_name":d.name,
					"parent_doc_name":frm.doc.name,
					"reference_doctype":d.reference_doctype,
					"reference_name":d.reference_name,
                    "self":frm.doc
				},
				callback: function(r){
					if (r.message){
						frappe.msgprint(r.message)
					}
				}
			})
		}
	}
});