function markComplete(assignment_id, student_id) {
    jQuery.ajax({
        url: eBookConfig.app + '/assignments/update_submit',
        type: "POST",
        dataType: "JSON",
        data: {
            assignment_id: assignment_id,
            student_id:student_id
        },
        success: function (retdata) {
            window.location.reload(true);
        }
    });
}