// Copyright (c) 2023, viral patel and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Ratio"] = {
	"filters": [
		{
			fieldname:"from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.month_start(), -1),
			reqd: 1
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.month_start(),-1),
			reqd: 1
		},
		
		{
			fieldname:"company",
			label: __("Company"),
			fieldtype: "Link",
			options:"Company",
			reqd: 1
		},
		{
			fieldname:"financial_retio",
			label: __("Financial Retio"),
			fieldtype: "Link",
			options:"Financial Retio",
			reqd: 1
		},
		
	]
};
