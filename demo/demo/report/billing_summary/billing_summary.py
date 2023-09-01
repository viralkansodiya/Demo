# Copyright (c) 2023, viral patel and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe import _
from frappe.utils import flt, time_diff_in_hours


def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	return columns, data



def get_columns():
	return [
		{
			"label": _("Employee ID"),
			"fieldtype": "Link",
			"fieldname": "employee",
			"options": "Employee",
			"width": 300,
		},
		{
			"label": _("Employee Name"),
			"fieldtype": "data",
			"fieldname": "employee_name",
			"hidden": 1,
			"width": 200,
		},
		{
			"label": _("Timesheet"),
			"fieldtype": "Link",
			"fieldname": "timesheet",
			"options": "Timesheet",
			"width": 150,
		},
		{"label": _("Working Hours"), "fieldtype": "Float", "fieldname": "total_hours", "width": 150},
		{
			"label": _("Billable Hours"),
			"fieldtype": "Float",
			"fieldname": "total_billable_hours",
			"width": 150,
		},
		{"label": _("Billing Amount"), "fieldtype": "Currency", "fieldname": "amount", "width": 150},
	]


def get_data(filters):
	data = []
	if filters.from_date > filters.to_date:
		frappe.msgprint(_("From Date can not be greater than To Date"))
		return data
	condition =""
	if filters.get('include_draft_timesheets'):
		condition += "t.docstatus != 2"
	else:
		condition += "t.docstatus = 1"
	if filters.get('from_date') and filters.get("to_date"):
		condition += f" and t.start_date >= '{filters.get('from_date')}'"
		condition += f" and t.end_date <= '{filters.get('to_date')}'"

	timesheets = frappe.db.sql(f"""SELECT t.name , t.employee , t.start_date , t.end_date,
			    			td.from_time , td.to_time , td.billing_hours
		      				from `tabTimesheet` as t
		      				left join `tabTimesheet Detail` as td on td.parent = td.name
			    			Where {condition} """,as_dict = 1)
	frappe.throw(str(timesheets))
	return data


def get_timesheets(filters):
	record_filters = [
		["start_date", "<=", filters.to_date],
		["end_date", ">=", filters.from_date],
	]
	if not filters.get("include_draft_timesheets"):
		record_filters.append(["docstatus", "=", 1])
	else:
		record_filters.append(["docstatus", "!=", 2])
	
	timesheets = frappe.get_all(
		"Timesheet", filters=record_filters, fields=["employee", "employee_name", "name" , "parent_project"]
	)

	timesheet_map = frappe._dict()

	for d in timesheets:
		timesheet_map.setdefault(d.name, d)

	return timesheet_map


def get_timesheet_details(filters, timesheet_list):
	timesheet_details_filter = {"parent": ["in", timesheet_list]}

	if "project" in filters:
		timesheet_details_filter["project"] = filters.project

	timesheet_details = frappe.get_all(
		"Timesheet Detail",
		filters=timesheet_details_filter,
		fields=[
			"project",
			"from_time",
			"to_time",
			"hours",
			"is_billable",
			"billing_hours",
			"billing_rate",
			"parent",
		],
	)

	timesheet_details_map = frappe._dict()
	for d in timesheet_details:
		timesheet_details_map.setdefault(d.parent, []).append(d)

	return timesheet_details_map


def get_billable_and_total_duration(activity, start_time, end_time):
	precision = frappe.get_precision("Timesheet Detail", "hours")
	activity_duration = time_diff_in_hours(end_time, start_time)
	billing_duration = 0.0
	if activity.is_billable:
		billing_duration = activity.billing_hours
		if activity_duration != activity.billing_hours:
			billing_duration = activity_duration * activity.billing_hours / activity.hours

	return flt(activity_duration, precision), flt(billing_duration, precision)


	