frappe.pages['register'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'None',
		single_column: true
	});
	frappe.register.make(page);
	frappe.register.run(page); 
}
frappe.register = {
	start: 0,
	make: function(page) {
		var me = frappe.register;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('register', data)).appendTo(me.body);
	}
}