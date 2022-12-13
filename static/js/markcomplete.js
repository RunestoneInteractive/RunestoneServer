function markComplete(assignment_id, student_id) {
    // This function is deprecated as of December 2022
    jQuery.ajax({
        url: eBookConfig.app + '/assignments/update_submit',
        type: "POST",
        dataType: "JSON",
        data: {
            assignment_id: assignment_id,
            student_id: student_id
        },
        success: function(retdata) {
            window.location.reload(true);
        }
    });
}



async function updateAssignmentProgress (newState, assignmentId) {

    let data = {
        assignment_id: assignmentId,
        new_state: newState,
    };
    let jsheaders = new Headers({
        "Content-type": "application/json; charset=utf-8",
        Accept: "application/json",
    });
    let request = new Request(`${eBookConfig.app}/assignments/update_submit`, {
        method: "POST",
        headers: jsheaders,
        body: JSON.stringify(data),
    });
    let resp = await fetch(request);
    if (!resp.ok) {
        alert(`Status Not Updated ${resp.statusText}`);
    } else {
        if (location.href.indexOf("doAssignment") > -1) {
            window.location.reload(true);
        }
    }

    console.log(newState);
}
