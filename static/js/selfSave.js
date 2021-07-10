function selfSave(assignment_id, student_num,) { 
    jQuery.ajax({
        url: eBookConfig.app + '/assignments/update_submit_button',
        type: "POST",
        dataType: "JSON",
        data: {
            assignment_id: assignment_id,
            student_num: student_num
        },
        success: function (retdata) {
            window.location.reload(true);
        }
    });
}

// self grade function takes two parameters, assignment and student ID
// it creates a URL and uses the student auto grade method
// and its data is a dict that might take in the assignment ID 
// If function is a success it does something with a window (reload)
//
// Description of Post: Send data to the server using a HTTP POST request.
// Makes data type JSON which to my knowledge are dictionaries easily transferable
