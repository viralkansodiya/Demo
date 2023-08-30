frappe.ui.form.on('Issue', {
    onload:function(frm){
        frm.trigger('create_button')
    },
    validate:function(frm){
        frm.trigger("create_button")
    },
    create_button:function(frm){
        if(!frm.doc.__islocal) {
        frm.add_custom_button(__('Create Task'), function () {
            frappe.call({
                method: "erpnext.support.doctype.issue.issue.get_if_task_exist",
                args: {
                    self:frm.doc
                },
                callback:function(r){
                    var name = r.message
                    if(name){
                        frappe.confirm('Task is Already Created.<br>Do you want to create another Task?',
                    () => {
                        frm.trigger('opendiolog')
                    }, () => {
                        
                    })
                    }
                    else{
                        frm.trigger('opendiolog')
                    }
                    
                }
            })
            
        }
        );
    }
    },
    opendiolog:function(frm){
        var d = new frappe.ui.Dialog({
            title: __('Task Assignment'),
            fields: [
                {
                    "label" : "Assignment To",
                    "fieldname": "assign_to",
                    "fieldtype": "Link",
                    "options":"User",
                    "reqd": 1,
                }
            ],
            primary_action: function() {
                var data = d.get_values();
                frappe.call({
                    method: "erpnext.support.doctype.issue.issue.create_new_task_from_issue",
                    args: {
                        self:frm.doc,
                        assign_to:data.assign_to
                    },
                    callback: function(r) {
                        if(!r.exc) {
                            
                            d.hide();
                        }
                        d.hide();
                    }
                });
            },
            primary_action_label: __('Create')
        });
        d.show();
    }
});