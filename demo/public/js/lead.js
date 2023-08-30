frappe.ui.form.on('Lead', {
    onload:function(frm){
        frm.page.remove_inner_button("Customer", "Create");
    }
});