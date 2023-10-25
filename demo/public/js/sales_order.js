
frappe.ui.form.on('Sales Order', {
    customer:function(frm){
        frappe.call({
            method:"demo.api.get_customer_item_name",
            args:{
                'doc':frm.doc
            },
            callback:function(r){
                console.log(r.message)
            }
        })
    }

})