function markComplete(assignment_id, student_id, is_submit) {
    jQuery.ajax({
        url: eBookConfig.app + '/assignments/update_submit',
        type: "POST",
        dataType: "JSON",
        data: {
            assignment_id: assignment_id,
            student_id:student_id,
            is_submit:is_submit,
        },
        success: function (retdata) {
            window.location.reload(true);
        }
    });
}