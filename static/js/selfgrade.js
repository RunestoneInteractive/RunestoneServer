function selfGrade(assignment_id) {
    jQuery.ajax({
        url: eBookConfig.app + '/assignments/student_autograde',
        type: "POST",
        dataType: "JSON",
        data: {
            assignment_id: assignment_id,
        },
        success: function (retdata) {
            window.location.reload(true);
        }
    });
}