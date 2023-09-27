import frappe
from frappe.desk.form.assign_to import add as add_assignment
from frappe.utils import  get_link_to_form
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def create_new_task_from_issue(issue , assign_to):
    issue = frappe.json.loads(issue)
    target_doc = None
    doclist = get_mapped_doc(
		"Issue",
		issue.get('name'),
		{
			"Issue": {
				"doctype": "Task",
				
			}
		},
		target_doc,
		
	)
    doclist.save()
    args = {
	        "assign_to": [assign_to],
	        "doctype": 'Task' ,
	        "name": doclist.name,
	}
    add_assignment(args)
    frappe.msgprint("Task Created Successfully: {0}".format(get_link_to_form("Task",doclist.name)))


@frappe.whitelist()
def get_if_task_exist(issue):
    issue = frappe.json.loads(issue)
    if name := frappe.db.exists("Task" , {"issue":issue.get('name')}):
        return name
    else:
        return