import frappe
from frappe.desk.form.assign_to import add
from frappe.utils import  get_link_to_form

@frappe.whitelist()
def create_new_task_from_issue(self , assign_to):
    self = frappe.json.loads(self)
    doc = frappe.new_doc("Task")
    doc.subject = self.get('subject')
    doc.issue = self.get('name')
    doc.description = self.get('description')
    doc.priority = self.get('priority')
    doc.status = self.get('status')
    doc.project = self.get('project')
    doc.save()
    args = {
	        "assign_to": [assign_to],
	        "doctype": 'Task' ,
	        "name": doc.name,
	}
    add(args)
    frappe.msgprint("Task Created Successfully , {0}".format(get_link_to_form("Task",doc.name)))


@frappe.whitelist()
def get_if_task_exist(self):
    self = frappe.json.loads(self)
    if name := frappe.db.exists("Task" , {"issue":self.get('name')}):
        return name
    else:
        return