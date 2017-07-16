var assignment_release_states = null;

function gradeIndividualItem() {
    var select3 = document.getElementById("gradingoption3");
    var colType = select3.options[select3.selectedIndex].value;

        var col1 = document.getElementById("gradingoption1");
    var col1val = col1.options[col1.selectedIndex].value;

        var col2 = document.getElementById("gradingoption2");
    var col2val = col2.options[col2.selectedIndex].value;

    set_release_button();

    var select = document.getElementById("gradingcolumn3");
    var val = select.options[select.selectedIndex].value;
    var rightSideDiv = $('#rightsideGradingTab');
    if (colType == 'question') {
        //we know the student must come from column 1 now
        document.getElementById("rightsideGradingTab").style.visibility = 'visible';
        var s_column = document.getElementById("gradingcolumn1");
        if (s_column.selectedIndex != -1) {
            //make sure they've selected a student from column 1
           var student = s_column.options[s_column.selectedIndex].value;
            var student_dict = students;
            for (var key in student_dict) {
                if (student_dict[key] == student) {
                    var sid = key;
                }
            }

            getRightSideGradingDiv(rightSideDiv, val, sid);


        }

    }

    else if (colType == 'student') {
        if (col1val == 'assignment' && getSelectedItem('assignment') != null) {
            calculateTotals()
        } else {
            document.getElementById('assignmentTotalform').style.visibility = 'hidden';
        }
        //we know the question must come from column 2 now
        document.getElementById("rightsideGradingTab").style.visibility = 'visible';
        var q_column = document.getElementById("gradingcolumn2");
        if (q_column.selectedIndex != -1) {
            //make sure they've selected a question from column 1
            var question = q_column.options[q_column.selectedIndex].value;
            var student_dict = students;
            for (var key in student_dict) {
                if (student_dict[key] == val) {
                    var sid = key;
                }
            }

            getRightSideGradingDiv(rightSideDiv, question, sid);


        }

    }
}

function getSelectedGradingColumn(type){
    //gradingoption1 has contents of picker for type of stuff in column (e.g., assignment, student)
    //gradingcolumn1 has contents of column (e.g., actual assignments)
    var opt1 = document.getElementById("gradingoption1");
    var col1Type = opt1.options[opt1.selectedIndex].value;

    var opt2 = document.getElementById("gradingoption2");
    var col2Type = opt2.options[opt2.selectedIndex].value;

    var opt3 = document.getElementById("gradingoption3");
    var col3type = opt3.options[opt3.selectedIndex].value;

    if (col1Type == type){
        col = document.getElementById("gradingcolumn1");
    }
    else if (col2Type == type){
        col = document.getElementById("gradingcolumn2");
    }
    else if (col3type == type){
        col = document.getElementById("gradingcolumn3");
    }
    else {
        col = null;
    }
    return col;
}

function getSelectedItem(type){
    var col = getSelectedGradingColumn(type);

    if (col == null){
        return null;
    }
    if (type == "student"){
        if (col.selectedIndex != -1) {
            // they've selected an item; get the id associated with it
            id_diction = students
            var item = col.options[col.selectedIndex].value;
            for (var key in id_diction) {
                // one of these should match, since an item was selected!
                if (id_diction[key] == item) {
                    var id = key;
                }
            }
            return id;
        }
        else {
            return null;
        }
    }
    else if (type == "assignment"){
        if (col.selectedIndex != -1) {
            // they've selected an assignment; return that assignment name
            return col.options[col.selectedIndex].value;
        }
        else {
            return null;
        }
    }
    else if (type == "question"){
        if (col.selectedIndex != -1) {
            // they've selected a question; return that question name
            return col.options[col.selectedIndex].value;
        }
        else {
            return null;
        }
    }
}

function autoGrade(){
    var assignment = getSelectedItem("assignment")
    var question = getSelectedItem("question")
    var studentID = getSelectedItem("student")
    var enforceDeadline = $('#enforceDeadline').is(':checked')
    jQuery.ajax({
        url: eBookConfig.autogradingURL,
        type: "POST",
        dataType: "JSON",
        data: {
            assignment: assignment,
            question: question,
            sid: studentID,
            enforceDeadline: enforceDeadline
        },
        success: function (retdata) {
            $('#assignmentTotalform').css('visibility', 'hidden');
            calculateTotals();
            alert(retdata.message);
            calculateTotals();
        }
    });
}

function calculateTotals(){
    var assignment = getSelectedItem("assignment")
    var question = getSelectedItem("question")
    var studentID = getSelectedItem("student")
    $('#assignmentTotalform').css('visibility', 'hidden');
    jQuery.ajax({
        url: eBookConfig.calcTotalsURL,
        type: "POST",
        dataType: "JSON",
        data: {
            assignment: assignment,
            question: question,
            sid: studentID
        },
        success: function (retdata) {
            if (retdata.computed_score != null) {
                // show the form for setting it manually
                $('#assignmentTotalform').css('visibility', 'visible');
                // populate it with data from retdata
                $('#computed-total-score').val(retdata.computed_score);
                $('#manual-total-score').val(retdata.manual_score);
            }
            else{
                alert(retdata.message);
            }
        }
    });
}

function saveManualTotal(){
    var assignment = getSelectedItem("assignment")
    var studentID = getSelectedItem("student")
    jQuery.ajax({
        url: eBookConfig.setTotalURL,
        type: "POST",
        dataType: "JSON",
        data: {
            assignment: assignment,
            sid: studentID,
            score: $('#manual-total-score').val(),
        },
        success: function (retdata) {
            if (!retdata.success){
                alert(retdata.message);
            }
        }
    });
}


function getRightSideGradingDiv(element, acid, studentId) {
    if (!eBookConfig.gradingURL) {
        alert("Can't grade without a URL");
        return false;
    }


    //make an ajax call to get the htmlsrc for the given question
    var obj = new XMLHttpRequest();
    obj.open("GET", "/runestone/admin/htmlsrc/?acid=" + acid, true);
    obj.send(JSON.stringify({acid: acid}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            var htmlsrc = JSON.parse(obj.responseText);
            //jQuery("#questiondisplay").html(htmlsrc);
            var enforceDeadline = $('#enforceDeadline').is(':checked');
            var dl = new Date(assignment_deadlines[getSelectedItem("assignment")]);
            renderRunestoneComponent(htmlsrc, "questiondisplay", {sid: studentId, graderactive: true, enforceDeadline: enforceDeadline, deadline: dl});
        }

    };



    function save(event) {
        event.preventDefault();

        var form = jQuery(this);
        var grade = jQuery('#input-grade', form).val();
        var comment = jQuery('#input-comments', form).val();
        jQuery.ajax({
            url: eBookConfig.gradeRecordingUrl,
            type: "POST",
            dataType: "JSON",
            data: {
                acid: acid,
                sid: studentId,
                grade: grade,
                comment: comment,
            },
            success: function (data) {
                jQuery('.grade', element).html(data.grade);
                jQuery('.comment', element).html(data.comment);
            }
        });
    }

    function show(data) {
        // get rid of any other modals -- incase they are just hanging out.
        //jQuery('.modal.modal-grader:not(#modal-template .modal)').remove();

        var rightDiv = jQuery('#outerRightDiv');

        jQuery('#gradingform', rightDiv).remove();
        var newForm = document.createElement('form');
        newForm.setAttribute('id', 'gradingform');
        formstr = '<form> <label for="input-grade">Grade</label> <input id="input-grade" type="text" class="form-control" value= ""/> <label for="input-comments">Comments</label> <input id="input-comments" type="text" class="form-control" value="" /> <input type="submit" value="Save Grade" class="btn btn-primary" /> </form> <button class="btn btn-default next" type="button">Save and next</button>';
        newForm.innerHTML = formstr;
        document.getElementById("outerRightDiv").appendChild(newForm);

        jQuery('#rightTitle', rightDiv).html(data.name + ' <em>' + data.acid + '</em>');

        //jQuery('.activecode-target',rightDiv).attr('id',data.acid+"_"+data.username);

        if (data.file_includes) {
            // create divids for any files they might need
            var file_div_template = '<pre id="file_div_template" style = "display:none;">template text</pre>;'
            var index;
            for (index = 0; index < data.file_includes.length; index += 1) {
                if (jQuery('#' + data.file_includes[index].acid).length == 0) {
                    // doesn't exist yet, so add it.
                    jQuery('body').append(file_div_template);
                    jQuery('#file_div_template').text(data.file_includes[index].contents);
                    jQuery('#file_div_template').attr("id", data.file_includes[index].acid);
                }
            }
        }

        // pull in any prefix or suffix code, already retrieved in data
        var complete_code = data.code;
        if (data.includes) {
            complete_code = data.includes + '\n#### end of included code\n\n' + complete_code;
        }
        if (data.suffix_code) {
            complete_code = complete_code + '\n\n#### tests ####\n' + data.suffix_code;
        }



        // outerdiv, acdiv, sid, initialcode, language


        jQuery('form', rightDiv).submit(save);
        jQuery('.next', rightDiv).click(function (event) {
            event.preventDefault();
            jQuery('form', rightDiv).submit();
            var col3 = document.getElementById("gradingcolumn3");
            try {
                var ind = col3.selectedIndex + 1;
                col3.selectedIndex = ind;
                col3.onchange();
            }

            catch (err) {
                //reached end of list
            }


        });
        jQuery('#' + data.id).focus();



        var divid;
        setTimeout(function(){

//        jQuery.ajax({
//        url: eBookConfig.gradeRecordingUrl,
//        type: "POST",
//        dataType: "JSON",
//        data: {
//            acid: acid,
//            sid: studentId,
//        },
//        success: function () {
//            //make an XML request to get the right stuff, pass in divid and studentId, then do the jQuery stuff below
            var obj = new XMLHttpRequest();
            obj.open('GET', '/runestone/admin/getGradeComments?acid=' + acid + '&sid=' + studentId, true);
            obj.send(JSON.stringify({newins: 'studentid'}));
            obj.onreadystatechange = function () {
                if (obj.readyState == 4 && obj.status == 200) {
                    var resp = obj.responseText;
                    var newdata = JSON.parse(resp);
                    if (newdata != "Error") {
                        jQuery('#input-grade', rightDiv).val(newdata['grade']);
                    jQuery('#input-comments', rightDiv).val(newdata['comments']);}
                }}
        },250);
    }

    element.addClass("loading");
    var assignment = getSelectedItem("assignment")
    var enforceDeadline = $('#enforceDeadline').is(':checked')

    jQuery.ajax({
        url: eBookConfig.gradingURL,
        type: "POST",
        dataType: "JSON",
        data: {
            assignment: assignment,
            acid: acid,
            sid: studentId,
            enforceDeadline: enforceDeadline
        },
        success: function (data) {
            show(data);
        }
    });



}


function updateColumn2() {
    var select1 = document.getElementById("gradingoption1");
    var val = select1.options[select1.selectedIndex].value;
    var select = document.getElementById("gradingoption2");
    var val2 = select.options[select.selectedIndex].value;
    var select2 = document.getElementById("gradingcolumn1");
    var column2 = document.getElementById("gradingcolumn2");
    var selectedval = select2.options[select2.selectedIndex].value;
    if (val == 'assignment'){
        set_release_button();
        if (getSelectedItem('student') != null) {
            calculateTotals();
        } else {
             document.getElementById('assignmentTotalform').style.visibility = 'hidden';
        }
    }
    if (val == 'assignment' && val2 == 'question') {
        $("#gradingcolumn2").empty();
        var assignments = JSON.parse(assignmentinfo);
        var assignment_names = assignments[selectedval];
        assignment_names.sort()
        for (i = 0; i < assignment_names.length; i++) {
            var q = assignment_names[i];
            var option = document.createElement("option");
            option.text = q;
            option.value = q;
            column2.add(option);

        }
    }

    else if (val == 'chapter' && val2 == 'question') {
        $("#gradingcolumn2").empty();
        for (i = 0; i < chapters[selectedval].length; i++) {
            var option = document.createElement("option");
            option.text = chapters[selectedval][i];
            option.value = chapters[selectedval][i];
            column2.add(option);
        }

    }

    else if (val == 'student') {
        if (getSelectedItem('student') != null && getSelectedItem('assignment') != null) {
            calculateTotals();
        } else {
            document.getElementById('assignmentTotalform').style.visibility = 'hidden';
        }
    }

    if (val2 != "") {
        column2.style.visibility = 'visible';
    }
}

function updateColumn3() {
    var select1 = document.getElementById("gradingoption2");
    var val = select1.options[select1.selectedIndex].value;
    var select = document.getElementById("gradingoption3");
    var val2 = select.options[select.selectedIndex].value;
    var select2 = document.getElementById("gradingcolumn2");
    var column3 = document.getElementById("gradingcolumn3");
    var selectedval = select2.options[select2.selectedIndex].value;
    if (val == 'assignment'){
        set_release_button();
        if (getSelectedItem('student') != null && getSelectedItem('assignment') != null) {
            calculateTotals();
        } else {
            document.getElementById('assignmentTotalform').style.visibility = 'hidden';
        }
    }
    if (val == 'chapter' && val2 == 'question') {
        $("#gradingcolumn3").empty();
        for (i = 0; i < chapters[selectedval].length; i++) {
            var option = document.createElement("option");
            option.text = chapters[selectedval][i];
            option.value = chapters[selectedval][i];
            column3.add(option);
        }
    }

    else if (val == 'assignment' && val2 == 'question') {
        $("#gradingcolumn3").empty();
        var assignments = JSON.parse(assignmentinfo);
        for (i = 0; i < assignments[selectedval].length; i++) {
            var q = assignments[selectedval][i];
            var option = document.createElement("option");
            option.text = q;
            option.value = q;
            column3.add(option);

        }

    }

    if (val2 != "") {
        var lastcolval = column3.selectedIndex;
        if (lastcolval != -1) {
            gradeIndividualItem();
        }
        column3.style.visibility = 'visible';
    }

}

function pickedAssignments(column) {

    var pickedcolumn = document.getElementById(column);

    $("#" + column).empty();
    var assignments = JSON.parse(assignmentinfo);
    set_release_button();
    autograde_form.style.visibility = 'visible';

    var keys = Object.keys(assignments);
    keys.sort();
    for (var i=0; i<keys.length; i++){
        var option = document.createElement("option");
        var key = keys[i];
        option.text = key;
        option.value = key;
        pickedcolumn.add(option);
        pickedcolumn.style.visibility = 'visible';

    }

}


function displayDefaultQuestion(column) {
    var pickedcolumn = document.getElementById(column);
    $("#" + column).empty();


    var option = document.createElement("option");
    option.text = '<- Choose option';
    option.value = 'default';
    pickedcolumn.add(option);
    $("option[value='default']").attr("disabled", "disabled");
    pickedcolumn.style.visibility = 'visible';
}


function pickedStudents(column) {

    var pickedcolumn = document.getElementById(column);
    $("#" + column).empty();
    // students = students.replace(/&#x27;/g, '"');
    var studentslist = students;
    var keys = [];
    var i;
    for (i in studentslist) {
        if (studentslist.hasOwnProperty(i)) {
            keys.push(i);
        }
    }


    for (i = 0; i < keys.length; i++) {
        var key = keys[i];
        var option = document.createElement("option");
        option.text = studentslist[key];
        option.value = studentslist[key];
        pickedcolumn.add(option);
        pickedcolumn.style.visibility = 'visible';

    }
}


function pickedChapters(column) {
    var pickedcolumn = document.getElementById(column);
    $("#" + column).empty();
    var keys = [];
    var i;
    for (i in chapters) {
        if (chapters.hasOwnProperty(i)) {
            keys.push(i);
        }
    }

    for (i = 0; i < keys.length; i++) {
        var key = keys[i];
        var option = document.createElement("option");
        option.text = key;
        option.value = key;
        pickedcolumn.add(option);
        pickedcolumn.style.visibility = 'visible';


    }

}


function showColumn1() {

    var select1 = document.getElementById("gradingoption1");
    var select = document.getElementById("gradingoption2");
    var select3 = document.getElementById("gradingoption3");
    select.selectedIndex = 0;
    select3.selectedIndex = 0;
    var val2 = select.options[select.selectedIndex].value;
    var val = select1.options[select1.selectedIndex].value;

    set_release_button();
    document.getElementById('assignmentTotalform').style.visibility = 'hidden';
    autograde_form = document.getElementById("autogradingform");
    autograde_form.style.visibility = 'hidden';

    $("#gradingcolumn2").empty();
    $("#gradingcolumn3").empty();
    $("#gradingoption2").empty();
    $("#gradingoption3").empty();

    if (val == 'assignment') {
        var option = document.createElement("option");
        option.text = 'question';
        option.value = 'question';
        var defaultOption = document.createElement("option");
        defaultOption.text = "Select your option";
        defaultOption.value = '';
        select.add(defaultOption);
        select.add(option);
        $("option[value='']").attr("disabled", "disabled");



        var third_default_opt = document.createElement("option");
        third_default_opt.text = 'Select your option';
        third_default_opt.value = '';
        select3.add(third_default_opt);
        $("option[value='']").attr("disabled", "disabled");

        var studentopt = document.createElement("option");
        studentopt.text = 'student';
        studentopt.text = 'student';
        select3.add(studentopt);


        pickedAssignments("gradingcolumn1");
    }


    else if (val == 'chapter') {

        $("#gradingoption2").empty();
        var defaultOption = document.createElement("option");
        defaultOption.text = "Select your option";
        defaultOption.value = '';
        select.add(defaultOption);
        $("option[value='']").attr("disabled", "disabled");
        var option = document.createElement("option");
        option.text = 'question';
        option.value = 'question';
        select.add(option);

        var third_default_opt = document.createElement("option");
        third_default_opt.text = 'Select your option';
        third_default_opt.value = '';
        select3.add(third_default_opt);
        $("option[value='']").attr("disabled", "disabled");

        var studentopt = document.createElement("option");
        studentopt.text = 'student';
        studentopt.text = 'student';
        select3.add(studentopt);



        pickedChapters('gradingcolumn1');
    }

    else if (val == 'student') {
        $("#gradingoption2").empty();
        $("#gradingoption3").empty();

        var defaultOption = document.createElement("option");
        defaultOption.text = "Select your option";
        defaultOption.value = '';
        select.add(defaultOption);

        var thirdDefaultOption = document.createElement("option");
        thirdDefaultOption.text = "Select your option";
        thirdDefaultOption.value = '';
        select3.add(thirdDefaultOption);
        $("option[value='']").attr("disabled", "disabled");
        var q = document.createElement("option");
        q.text = 'question';
        q.value = 'question';
        select3.add(q);

        var options = ['chapter', 'assignment'];
        for (i = 0; i < options.length; i++) {
            var val = options[i];
            var option = document.createElement("option");
            option.text = val;
            option.value = val;
            select.add(option);
        }

        pickedStudents('gradingcolumn1');
    }

}

function showColumn2() {

    var select1 = document.getElementById("gradingoption2");
    var val = select1.options[select1.selectedIndex].value;
    var select = document.getElementById("gradingoption1");
    var first_val = select.options[select.selectedIndex].value;
    var select3 = document.getElementById('gradingoption3');
    select3.selectedIndex = 0;
    $("#gradingcolumn3").empty();


    if (first_val == "") {
        select1.selectedIndex = 0;
        alert("That is not a valid combination");
    }

    else {
        if (val == 'assignment') {
            $("#gradingoption3").empty();
            var defaultOption = document.createElement("option");
            defaultOption.text = "Select your option";
            defaultOption.value = '';
            select3.add(defaultOption);
            $("option[value='']").attr("disabled", "disabled");
            var option = document.createElement("option");
            option.text = 'question';
            option.value = 'question';
            select3.add(option);


            if (first_val == 'assignment') {
                alert("That is not a valid combination");
                select1.selectedIndex = 0;

            }
            else if (first_val == 'chapter') {
                alert("That is not a valid combination");
                select1.selectedIndex = 0;

            }
            else {
                pickedAssignments("gradingcolumn2");
            }
        }

        else if (val == 'chapter') {
            $("#gradingoption3").empty();
            var defaultOption = document.createElement("option");
            defaultOption.text = "Select your option";
            defaultOption.value = '';
            select3.add(defaultOption);
            $("option[value='']").attr("disabled", "disabled");
            var option = document.createElement("option");
            option.text = 'question';
            option.value = 'question';
            select3.add(option);
            document.getElementById('assignmentTotalform').style.visibility = 'hidden';


            if (first_val == 'assignment') {
                alert("That is not a valid combination");
                $("#gradingcolumn2").empty();
                select1.selectedIndex = 0;

            }

            else if (first_val == 'chapter') {
                alert("That is not a valid combination");
                $("#gradingcolumn2").empty();
                select1.selectedIndex = 0;

            }
            else {
                pickedChapters('gradingcolumn2');
            }
        }

        else if (val == 'question') {
            $("#gradingoption3").empty();
            var defaultOption = document.createElement("option");
            defaultOption.text = "Select your option";
            defaultOption.value = '';
            select3.add(defaultOption);
            $("option[value='']").attr("disabled", "disabled");
            var option = document.createElement("option");
            option.text = 'student';
            option.value = 'student';
            select3.add(option);


            var select2 = document.getElementById("gradingcolumn1");
            var preselected = false;
            if (select2.selectedIndex != -1) {
                var selectedval = select2.options[select2.selectedIndex].value;
                preselected = true;
            }

            if (first_val == 'chapter') {
                if (preselected == true) {
                    updateColumn2();
                }
                else {
                    displayDefaultQuestion('gradingcolumn2');
                }
            }


            else if (first_val == 'assignment') {
                if (preselected == true) {
                    updateColumn2();
                }
                else {
                    displayDefaultQuestion('gradingcolumn2');
                }
            }

            else {
                alert("That is not a valid combination");
                $("#gradingcolumn2").empty();
                select1.selectedIndex = 0;

            }
        }

    }
}

function showColumn3() {

    var select1 = document.getElementById("gradingoption3");
    var val = select1.options[select1.selectedIndex].value;
    var select = document.getElementById("gradingoption1");
    var val1 = select.options[select.selectedIndex].value;
    var select2 = document.getElementById("gradingoption2");
    var val2 = select2.options[select2.selectedIndex].value;
    if (val == 'question') {
        var select2 = document.getElementById("gradingcolumn2");
        var preselected = false;
        if (select2.selectedIndex != -1) {
            var selectedval = select2.options[select2.selectedIndex].value;
            preselected = true;
        }

        if (val1 == 'student' && val2 == 'chapter') {
            if (preselected == true) {
                updateColumn3();
            }
            else {
                displayDefaultQuestion('gradingcolumn3');
            }

        }

        else if (val1 == 'student' && val2 == 'assignment') {
            if (preselected == true) {
                updateColumn3();
            }
            else {
                displayDefaultQuestion('gradingcolumn3');
            }

        }

        else {
            alert("That is not a valid combination");
            select1.selectedIndex = 0;
            $("#gradingcolumn3").empty();


        }

    }


    else if (val == 'student') {

        if (val1 == 'chapter' && val2 == 'question') {
            pickedStudents("gradingcolumn3");
        }

        else if (val1 == 'assignment' && val2 == 'question') {
            pickedStudents("gradingcolumn3");
        }

        else {
            alert("That is not a valid combination");
            select1.selectedIndex = 0;
            $("#gradingcolumn3").empty();


        }

    }

}

function getCourseStudents(){
    jQuery.ajax({
        url: eBookConfig.getCourseStudentsURL,
        type: "POST",
        dataType: "JSON",
        data: {},
        success: function (retdata) {
            students = retdata;
        }
    });
}


function getStudents(sectionName) {
    var section = sectionName;

    var studentList = document.getElementById("studentNames");
    studentList.innerHTML = '';

    var obj = new XMLHttpRequest();
    obj.open("GET", "/runestone/sections/students/" + section, true);
    obj.send(JSON.stringify({sectionName: sectionName}));
    obj.onreadystatechange = function () {

        if (obj.readyState == 4 && obj.status == 200) {
            var students = JSON.parse(obj.responseText);
            for (i = 0; i < students.length; i++) {
                studentList.innerHTML += '<a href="#" class="list-group-item"> <h4 style="text-align: center" class="list-group-item-heading">' + students[i][0] + " " + students[i][1] + '</h4> </a>';

            }

            var total = document.getElementById("total");
            if (students == "") {
                total.innerHTML = "Total: 0";
            }
            else {
                total.innerHTML = "Total: " + students.length;
            }

        }
    }
}



// TODO: This function is also defined in admin.html. ???
function getLog() {


    var obj = new XMLHttpRequest();
    obj.open("GET", "/runestone/admin/getChangeLog", true);
    obj.send(JSON.stringify({variable: 'variable'}));
    obj.onreadystatechange = function () {

        if (obj.readyState == 4 && obj.status == 200) {
            changeLog = document.getElementById("changelog");
            changeLog.innerHTML = obj.responseText;
        }
    }
}


function add_instructor() {
    var select = document.getElementById('addins').elements['student'];
    var index = select.selectedIndex;
    var studentid = select.options[index].value; //value gives the value, text gives the actual text
    var studentname = select.options[index].text;

    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/addinstructor/' + studentid, true);
    obj.send(JSON.stringify({newins: 'studentid'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            studlist = document.getElementById('studentlist');
            studlist.remove(index);
            inslist = document.getElementById('instructorlist');
            newopt = document.createElement('option');
            newopt.value = studentid;
            newopt.innerHTML = studentname;
            inslist.appendChild(newopt);
        }
    }
}

function remove_instructor() {
    var select = document.getElementById('removeins').elements['instructor'];
    var index = select.selectedIndex;
    var studentid = select.options[index].value; //value gives the value, text gives the actual text
    var studentname = select.options[index].text;
    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/removeinstructor/' + studentid, true);
    obj.send(JSON.stringify({newins: 'studentid'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            gotdeleted = JSON.parse(obj.responseText);
            if (gotdeleted[0]) {
                inslist = document.getElementById('instructorlist');
                inslist.remove(index);
                studlist = document.getElementById('studentlist');
                newopt = document.createElement('option');
                newopt.value = studentid;
                newopt.innerHTML = studentname;
                studlist.appendChild(newopt);
            } else {
                //flash message that you can't remove yourself
            }
        }
    }
}


function edit_indexrst(form) {
    var newtext = form.editIndex.value;
    newtext =  newtext.replace(/(\r\n|\n|\r)/gm, '%0A'); //encodes all new line characters to preserve them in query string
    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/editindexrst?newtext=' + newtext, true);
    obj.send(JSON.stringify({variable:'variable'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            alert("Successfully edited index.rst");

        }}
}

// *************************
// Assignments tab functions
// *************************
function remove_assignment() {
    var select = document.getElementById('assignlist');
    var assignmentid = select.options[select.selectedIndex].value;
    var assignmentname = select.options[select.selectedIndex].text;

    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/removeassign/' + assignmentid, true);
    obj.send(JSON.stringify({assignid: 'assignmentid'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            select.remove(select.selectedIndex);
            assignmentInfo();
        }
    }
}


 // TODO: This function isn't used anywhere that I can see. Remove it?
function search_students(formdata) {
    var searchterm = formdata.searchterm.value;
    if (searchterm == '') {
        searchterm = '_'
    }
    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/searchstudents/' + searchterm, true);
    obj.send(JSON.stringify({tosearch: 'searchterm'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            studidlist = JSON.parse(obj.responseText);
            var studentlist = document.getElementById('studentlist');
            studentlist.innerHTML = '';
            for (var key in studidlist) {
                if (studidlist.hasOwnProperty(key)) {
                    option = document.createElement('option');
                    option.value = key;
                    option.innerHTML = studidlist[key];
                    studentlist.appendChild(option)

                }
            }
        }
    }
}

// Called when the "Write" button is clicked.
function display_write() {
    var template = document.getElementById('template');
    var questiontype = template.options[template.selectedIndex].value;
    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/gettemplate/' + questiontype, true);
    obj.send();
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            var returns = JSON.parse(obj.responseText);
            tplate = returns['template'];
            $("#qcode").text(tplate);
        }
        $.each(returns['chapters'], function (i, item) {
            $('#qchapter').append($('<option>', {
                value: item,
                text: item
            }));
        });
    };

    var hiddenwrite = document.getElementById('hiddenwrite');
    hiddenwrite.style.visibility = 'visible';
}


// Called when the "Done" button of the "Write" dialog is clicked.
function create_question(formdata) {
    if (! confirm("Have you previewed your question?")) {
        return;
    }
    var activetab = 'formative';
    var select = document.getElementById('assignlist');
    var assignmentid = select.options[select.selectedIndex].value;
    var assignmentname = select.options[select.selectedIndex].text;
    var template = formdata.template.value;
    var qcode = formdata.qcode.value;
    var lines = qcode.split('\n');
    var htmlsrc = formdata.qrawhtml.value;
    for(var i = 0; i < lines.length; i++) {
        if (lines[i] != "") {
            var line = lines[i];
            var match = line.split(/.. \w*:: /);
            var name = match[1];
            break;
        }
    }

    var question = formdata.qcode.value;
    var difficulty = formdata.difficulty;
    for (var i = 0; i < difficulty.length; i++) {
        if (difficulty[i].checked == true) {
            var selectedDifficulty = difficulty[i].value;
        }
    }
    var tags = formdata.qtags.value;
    var chapter = formdata.qchapter.value;
    var isprivate = formdata.isprivate.checked;
    var points = formdata.createpoints.value;
    var timed = formdata.createtimed.checked;

    data = {
        'template' : template,
        'name' : name,
        'question' : question,
        'difficulty' : selectedDifficulty,
        'tags' : tags,
        'chapter' : chapter,
        'isprivate' : isprivate,
        'tab' : activetab,
        'assignmentid' : assignmentid,
        'points' : points,
        'timed' : timed,
        'htmlsrc' : htmlsrc
    }
    url = '/runestone/admin/createquestion'
    jQuery.post(url, data, function (iserror, textStatus, whatever) {
        if (iserror == 'ERROR') {
            errortext = document.getElementById('qnameerror');
            errortext.innerHTML = 'Name is already in use. Please try a different name.'
        } else {
            alert('Question created successfully');
            var newPoints = iserror['points'];
            var q_type = activetab;
            var totalPoints = document.getElementById("totalPoints");
            totalPoints.innerHTML = 'Total points: ' + newPoints;
            updateAssignmentRaw(name, points, 'interact');
        }
    }, 'json');
}


// Given a selected assignment, retrieve it from the server then display it.
function assignmentInfo() {
    // If no assignment is selected, hide all assignment-related panels.
    var select = document.getElementById('assignlist');
    if (select.selectedIndex === -1) {
        $('#rightSection').css('visibility', 'hidden');
        $('#leftpanel1').css('visibility', 'hidden');
        $('#leftpanel2').css('visibility', 'hidden');
        return;
    }

    var assignmentid = select.options[select.selectedIndex].value;
    $('#rightSection').css('visibility', 'visible');
    $("#leftpanel1").css('visibility', 'visible');
    $("#leftpanel2").css('visibility', 'visible');

    $.getJSON('get_assignment', {'assignmentid': assignmentid}, function (data) {
        assignmentData = data['assignment_data'];
        $('#totalPoints').html('Total points: ' + assignmentData['assignment_points']);
        $('#datetimepicker').val(assignmentData['due_date']);
        $('#assignment_description').val(assignmentData['description']);
        $('#readings-threshold').val(assignmentData['threshold']);
        $('#readings-points-to-award').val(assignmentData['points_to_award']);
        $('#readings-autograder').val(assignmentData['readings_autograder']);

        // Update the questions
        ///====================
        // Get the question tree picker.
        var tqp = question_picker.jstree(true);
        // Ignore these checks in the picker, since it's loading existing data, not user interaction.
        tqp.ignore_check = true;
        // Clear all checks initially.
        tqp.uncheck_all();

        // Clear the bootstrap table.
        question_table.bootstrapTable('removeAll');
        for (let question of data['questions_data']) {
            // Put the qeustion in the table.
            let name = question['name'];
            appendToQuestionTable(name, question['points'], question['autograde'], question['autograde_possible_values'], question['which_to_grade'], question['which_to_grade_possible_values']);
            // Check this question in the question tree picker.
            tqp.check_node(tqp.get_node(name));
        }

        // Future checks come from the user.
        tqp.ignore_check = false;

        // Update the readings
        ///===================
        var trp = readings_picker.jstree(true);
        trp.ignore_check = true;
        trp.uncheck_all();

        for (let readings_data of data['pages_data']) {
            id = readings_data['name'];
            trp.check_node(trp.get_node(id));
            appendToReadingsTable(id)
        }
        trp.ignore_check = false;
    });
}


// Append a row to the readings table given the ID of the reading.
function appendToReadingsTable(readings_id) {
    // Find this node in the tree.
    var node = readings_picker.jstree(true).get_node(readings_id);
    readings_table.bootstrapTable('append', [{
        chapter: readings_picker.jstree(true).get_node(node.parent).text,
        subchapter: node.text,
        subchapter_id: node.id,
    }]);
}

// Append a row to the question table.
function appendToQuestionTable(name, points, autograde, autograde_possible_values, which_to_grade, which_to_grade_possible_values) {
    var _id = 'question_table_' + name;
    question_table.bootstrapTable('append', [{
        'question' : name,
        'points' : points,
        'autograde' : autograde,
        'autograde_possible_values': autograde_possible_values,
        'which_to_grade': which_to_grade,
        'which_to_grade_possible_values': which_to_grade_possible_values,
        // Setting an ID for the row is essential: the row reordering plugin depends on a valid row ID for the `drop message <https://github.com/wenzhixin/bootstrap-table/tree/master/src/extensions/reorder-rows#userowattrfunc>`_ to work. Setting the ``_id`` key is one way to accomplish this.
        '_id' : _id,
    }]);
}

// Invoked by the "Create" button of the "Create Assignment" dialog.
function createAssignment(form) {
    var name = form.name.value;

    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/createAssignment/?name=' + name, true);
    obj.send(JSON.stringify({name: name, description: description}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            added = JSON.parse(obj.responseText);
            if (added != 'ERROR') {
                select = document.getElementById('assignlist');
                newopt = document.createElement('option');
                newopt.value = added[name];
                newopt.innerHTML = name;
                select.appendChild(newopt);
                select.selectedIndex = newopt.index;
                assignmentInfo();
            } else {
                alert('Error in creating new assignment.')
            }
        }
    }
}


// Called by the "Preview" button of the "Write" panel.
function preview_question(form){

    var code = $(form.qcode).val();
    var data = {'code': JSON.stringify(code)};
    $.post('/runestone/ajax/preview_question', data, function(result, status) {
            let code = JSON.parse(result);
            $(form.qrawhtml).val(code); // store the un-rendered html for submission
            renderRunestoneComponent(code, "component-preview")
        }
    );
    // get the text as above
    // send the text to an ajax endpoint that will insert it into
    // a sphinx project, run sphinx, and send back the generated index file
    // this generated index can then be displayed...

}


// Render a question in the provided div?
function renderRunestoneComponent(componentSrc, whereDiv, moreOpts) {
    /**
     *  The easy part is adding the componentSrc to the existing div.
     *  The tedious part is calling the right functions to turn the
     *  source into the actual component.
     */

    jQuery(`#${whereDiv}`).html(componentSrc);

    edList = [];
    mcList = [];
    let componentKind = $($(`#${whereDiv} [data-component]`)[0]).data('component')
    let opt = {};
    opt.orig = jQuery(`#${whereDiv} [data-component]`)[0]
    opt.lang = $(opt.orig).data('lang')
    opt.useRunestoneServices = false;
    opt.graderactive = false;
    opt.python3 = true;
    if (typeof moreOpts !== 'undefined') {
        for (let key in moreOpts) {
            opt[key] = moreOpts[key]
        }
    }

    if (typeof component_factory === 'undefined') {
        alert("Error:  Missing the component factory!  Either rebuild your course or clear you browser cache.");
    } else {
        if (!component_factory[componentKind]) {
            jQuery(`#${whereDiv}`).html(`<p>Preview not available for ${componentKind}</p>`)
        } else {
            component_factory[componentKind](opt)
        }
    }
}


// Called to remove a question from an assignment.
function remove_question(question_name) {
    var assignment_id = getAssignmentId();
    $.getJSON('delete_assignment_question/?name=' + question_name + '&assignment_id=' + assignment_id, {variable: 'variable'}).done(function (response_JSON) {
        var totalPoints = document.getElementById("totalPoints");
        totalPoints.innerHTML = 'Total points: ' + response_JSON['total'];
        // Remove the named row from the table. See the `example <http://issues.wenzhixin.net.cn/bootstrap-table/#methods/removeByUniqueId.html>`__.
        question_table.bootstrapTable('removeByUniqueId', question_name);
    });
}

// Remove a reading from an assignment.
function remove_reading(reading_id) {
    $.getJSON('delete_assignment_question', {
        assignment_id: getAssignmentId(),
        name: reading_id,
    }).done(function (response_JSON) {
        readings_table.bootstrapTable('removeByUniqueId', reading_id);
    });
}

// Called by the "Search" button in the "Search question bank" panel.
function questionBank(form) {
    var chapter = form.chapter.value;
    var author = form.author.value;
    var tags = $("#tags").select2("val");
    var term = form.term.value;
    var difficulty = null;
    var difficulty_options = ['rating1', 'rating2', 'rating3', 'rating4', 'rating5'];
    var inputs = document.getElementById('qbankform').getElementsByTagName('input');
    for (var i = 0, length = inputs.length; i < length; i++) {
        if (inputs[i].type == 'radio' && inputs[i].checked) {
            difficulty = inputs[i].value;
        }
    }

    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/questionBank?chapter=' + chapter + '&difficulty=' + difficulty + '&author=' + author + '&tags=' + tags + '&term=' + term + '&qtype=' +'formative', true);
    obj.send(JSON.stringify({variable: 'variable'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            var resp = JSON.parse(obj.responseText);
            var select = document.getElementById('qbankselect');
            select.onchange = getQuestionInfo;
            var questionform = document.getElementById('questionform');
            $("#qbankselect").empty();
            for (i = 0; i < resp.length; i++) {
                var option = document.createElement("option");
                option.text = resp[i];
                option.value = resp[i];
                option.onclick = getQuestionInfo;
                select.add(option);
            }
            if (resp.length == 0) {
                select.style.visibility = 'hidden';
                questionform.style.visibility = 'hidden';
                var q_info = document.getElementById('questionInfo');
                q_info.style.visibility = 'hidden';
                alert("Sorry, no questions matched your search criteria.");

            }
            if (resp.length > 0) {
                select.style.visibility = 'visible';
                questionform.style.visibility = 'visible';
            }
        }
    }
}

// Return the assignment id based on the value selected in the ``assignlist`` item.
function getAssignmentId() {
    var assignlist = document.getElementById('assignlist');
    return assignlist.options[assignlist.selectedIndex].value;
}


// Called by the "Add to assignment" button in the "Search question bank" panel after a search is performed.
function addToAssignment(form) {
    var points = form.points.value;
    var select = document.getElementById('qbankselect');
    var question_name = select.options[select.selectedIndex].text;

    updateAssignmentRaw(question_name, points, '');
}

// Update an assignment.
function updateAssignmentRaw(question_name, points, autograde, which_to_grade) {
    var assignmentid = getAssignmentId();
    $.getJSON('/runestone/admin/add__or_update_assignment_question/?question=' + question_name + '&assignment=' + assignmentid + '&points=' + points + '&autograde=' + autograde + '&which_to_grade=' + which_to_grade, {variable: 'variable'}).done(function (response_JSON) {
        $('#totalPoints').html('Total points: ' + response_JSON['total']);
        // See if this question already exists in the table. Only append if it doesn't exist.
        if (question_table.bootstrapTable('getRowByUniqueId', question_name) === null) {
            appendToQuestionTable(question_name, points, autograde,
                response_JSON['autograde_possible_values'], which_to_grade,
                response_JSON['which_to_grade_possible_values']);
        }
    });
}


// When a user clicks on a question in the select element of the "Search question bank" panel after doing a search, this is called.
function getQuestionInfo() {
    var select = document.getElementById('qbankselect');
    var question_name = select.options[select.selectedIndex].text;
    var assignlist = document.getElementById('assignlist');
    var assignmentid = assignlist.options[assignlist.selectedIndex].value;
    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/getQuestionInfo/?question=' + question_name + '&assignment=' + assignmentid, true);
    obj.send(JSON.stringify({variable: 'variable'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            var question_info = obj.responseText;
            var res = JSON.parse(question_info);
            var data = {};
            var i;
            for (i in res) {
                if (res.hasOwnProperty(i)) {
                    data[i] = res[i];
                }
            }
            var difficulty = data['difficulty'];
            var code = data['code'];
            var author = data['author'];
            var tags = data['tags'];

            var q_difficulty = document.getElementById('q_difficulty');
            if (difficulty == null) {
                q_difficulty.innerHTML = 'Difficulty not set for this question';
            } else {
                q_difficulty.innerHTML = 'Difficulty: ' + difficulty;
            }


            renderRunestoneComponent(data['htmlsrc'], "component-preview")

            var q_author = document.getElementById('q_author');
            if (author == null) {
                q_author.innerHTML = 'No author for this question';
            } else {
                q_author.innerHTML = 'Author: ' + author;
            }

            var q_tags = document.getElementById('q_tags');
            q_tags.innerHTML = 'Tags:' + tags;
            var q_info = document.getElementById('questionInfo');
            q_info.style.visibility = 'visible';

        }
    }
}


// Called inside the "Write Assignment" panel?
function edit_question(form) {
    var select = document.getElementById('qbankselect');
    var question_name = select.options[select.selectedIndex].text;
    var tags = $("#addTags").select2("val");
    var name = form.changename.value;
    var difficulty = null;
    var difficulty_options = ['r1', 'r2', 'r3', 'r4', 'r5'];
    var inputs = document.getElementById('editForm').getElementsByTagName('input');
    for (var i = 0, length = inputs.length; i < length; i++) {
        if (inputs[i].type == 'radio' && inputs[i].checked) {
            difficulty = inputs[i].value;
        }
    }
    var question_text = form.editRST.value;
          question_text =  question_text.replace(/(\r\n|\n|\r)/gm, '%0A'); //encodes all new line characters to preserve them in query string

    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/edit_question/?question=' + question_name + '&tags=' + tags + '&difficulty=' + difficulty + '&name=' + name + '&questiontext=' + question_text, true);
    obj.send(JSON.stringify({variable: 'variable'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            if (obj.responseText == 'Success') {
                alert('You successfully edited the selected question.');
            }
        }
    }

}


// More preview panel functionality I don't understand.
function getQuestionText() {
    var select = document.getElementById('qbankselect');
    var question_name = select.options[select.selectedIndex].text;
    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/question_text?question_name=' + question_name, true);
    obj.send(JSON.stringify({variable: 'variable'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            var textarea = document.getElementById('editRST');
            textarea.innerHTML = obj.responseText;
        }
    }
}

// More preview panel functionality I don't understand.
function questions2Rst() {
    var select = document.getElementById('assignlist');
    var assignmentid = select.options[select.selectedIndex].value;
    $.getJSON('/runestone/admin/questions2rst/' + assignmentid, {}, function () {
        alert("done")
    });
}


// Change the due date.
function changeDueDate(form) {
    var newdate = form.changedate.value;
    var select = document.getElementById('assignlist');
    var assignmentid = select.options[select.selectedIndex].value;
    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/changeDate?newdate=' + newdate + '&assignmentid=' + assignmentid, true);
    obj.send(JSON.stringify({variable: 'variable'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            if (obj.responseText == 'success') {
                alert("Successfully changed due date");
                document.getElementById("assignment_duedate").innerHTML = "Due: " + newdate;
            }

            else if (obj.responseText == 'error') {
                alert("There was an error changing your due date");
            }
        }
    }

}

// Update the grading parameters used for a reading assignment.
function update_readings_grading(form) {
    $.getJSON('save_assignment', $(form).serialize() + '&assignment_id=' + getAssignmentId());
}


// ***********
// Grading tab
// ***********
// Return whether the assignment has been released for grading.
function get_assignment_release_states(){
    if (assignment_release_states == null){
        // This has to be a synchronous call because we have to set assignment_release_states
        // before going on to later code that uses it
        jQuery.ajax({
        url: eBookConfig.get_assignment_release_statesURL,
        type: "POST",
        dataType: "JSON",
        async: false,
        success: function (retdata) {
            assignment_release_states = retdata;
        }
        });
    }
}

// Update the release button in the grading panel?
function set_release_button() {

    // first find out if there is an assignment selected
    var col1 = document.getElementById("gradingoption1");
    var col1val = col1.options[col1.selectedIndex].value;

    var col2 = document.getElementById("gradingoption2");
    var col2val = col2.options[col2.selectedIndex].value;
    var assignment = null;

    if (col1val == 'assignment') {
        var assignmentcolumn = document.getElementById("gradingcolumn1");
        if (assignmentcolumn.selectedIndex != -1) {
            assignment = assignmentcolumn.options[assignmentcolumn.selectedIndex].value;
        }
    }

    else if (col2val == 'assignment') {
        var assignmentcolumn = document.getElementById("gradingcolumn2");
        if (assignmentcolumn.selectedIndex != -1) {
            assignment = assignmentcolumn.options[assignmentcolumn.selectedIndex].value;
        }
    }

    // change the release button appropriately
    // var release_button = document.getElementById("releasebutton");
    var release_button = $('#releasebutton');
    if (assignment == null) {
        //hide the release grades button
        release_button.css('visibility', 'hidden');
    }

    else{
        release_button.css('visibility', 'visible');
        // see whether grades are currently live for this assignment
        get_assignment_release_states();
        var release_state = assignment_release_states[assignment];
        // If so, set the button text appropriately
        if (release_state == true){
            release_button.text("Hide Grades from Students for " + assignment);
        }
        else{
            release_button.text("Release Grades to Students for " + assignment);
        }
    }
}

function toggle_release_grades() {
    var col1 = document.getElementById("gradingoption1");
    var col1val = col1.options[col1.selectedIndex].value;

    var col2 = document.getElementById("gradingoption2");
    var col2val = col2.options[col2.selectedIndex].value;
    var assignment = null;

    if (col1val == 'assignment') {
        var assignmentcolumn = document.getElementById("gradingcolumn1");
        if (assignmentcolumn.selectedIndex != -1) {
            assignment = assignmentcolumn.options[assignmentcolumn.selectedIndex].value;

        }

        else {
            alert("Please choose an assignment first");
        }
    }

    else if (col2val == 'assignment') {

        var assignmentcolumn = document.getElementById("gradingcolumn2");
        if (assignmentcolumn.selectedIndex != -1) {
            assignment = assignmentcolumn.options[assignmentcolumn.selectedIndex].value;

        }

        else {
            alert("Please choose an assignment first");
        }

    }

    if (assignment != null) {
        //go release the grades now
        get_assignment_release_states()
        release_state = assignment_release_states[assignment];
        var ids = JSON.parse(assignmentids);
        var assignmentid = ids[assignment];
        var obj = new XMLHttpRequest();
        if (release_state == true){
            // Have to toggle the local variable before making the asynch call, so that button will be updated correctly
            assignment_release_states[assignment] = null;
            obj.open('POST', '/runestone/admin/releasegrades?assignmentid=' + assignmentid + '&released=no', true);
            obj.send(JSON.stringify({variable: 'variable'}));
            obj.onreadystatechange = function () {
                if (obj.readyState == 4 && obj.status == 200) {
                    alert("Grades are now hidden from students for " + assignment);
                }
            }
        }

        else{
            // Have to toggle the local variable before making the asynch call, so that button will be updated correctly
            assignment_release_states[assignment] = true;
            obj.open('POST', '/runestone/admin/releasegrades?assignmentid=' + assignmentid + '&released=yes', true);
            obj.send(JSON.stringify({variable: 'variable'}));
            obj.onreadystatechange = function () {
                if (obj.readyState == 4 && obj.status == 200) {
                    alert("Grades are now visible to students for " + assignment);
                }
            }
        }
        set_release_button();
    }
}

