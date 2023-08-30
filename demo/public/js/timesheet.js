frappe.ui.form.on('Timesheet', {

})
console.log('ask')
frappe.ui.form.on('Timesheet Detail', {
    start_time:function(frm,cdt,cdn){
        let d = locals[cdt][cdn];
        let date = d.date
        let currentDate = `${date} ${d.start_time}`;
        console.log(currentDate)
        d.from_date = currentDate
        frappe.model.set_value(cdt , cdn , 'from_time' , currentDate)
       
        cur_frm.refresh_field('time_logs')
    },
    date:function(frm,cdt,cdn){
        let d = locals[cdt][cdn];
        let date = d.date
        let currentDate = `${date} ${d.start_time}`;
        console.log(currentDate)
        d.from_date = currentDate
        frappe.model.set_value(cdt , cdn , 'from_time' , currentDate)
       
        cur_frm.refresh_field('time_logs')
    }
})