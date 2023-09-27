frappe.pages['financial-ratio'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Financial Ratio',
		single_column: true
	});
	frappe.financialratio.make(page);
	// frappe.financialratio.run(page); 
}
frappe.financialratio = {
	start: 0,
	make: function(page) {
		var me = frappe.financialratio;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('financial_ratio', data)).appendTo(me.body);
	}
};