function gradeIndividualItem() {
    var select3 = document.getElementById("gradingoption3");
    var colType = select3.options[select3.selectedIndex].value;

        var col1 = document.getElementById("gradingoption1");
    var col1val = col1.options[col1.selectedIndex].value;

        var col2 = document.getElementById("gradingoption2");
    var col2val = col2.options[col2.selectedIndex].value;
    release_button = document.getElementById("releasebutton");


    if (col1val == 'assignment' | col2val == 'assignment') {
        //show the release grades button
        release_button.style.visibility = 'visible';
    }

    else {
        //hide the release grades button
        release_button.style.visibility = 'hidden';
    }

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
            alert(retdata.message);
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
            jQuery("#questiondisplay").html(htmlsrc);
            //ACFactory.createScratchActivecode();
            $('[data-component=activecode]').each(function (index) {
                if ($(this.parentNode).data("component") !== "timedAssessment") {   // If this element exists within a timed component, don't render it here
                    edList[this.id] = ACFactory.createActiveCode(this, $(this).data('lang'), {sid: studentId, graderactive: true, python3:false});
                }
            });
            if (loggedout) {
                for (k in edList) {
                    edList[k].disableSaveLoad();
                }
            }


        }

    }



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




            var myobj = new XMLHttpRequest();
            myobj.open('GET', '/runestone/admin/checkQType?acid=' + acid + '&sid=' + studentId, true);
            myobj.send(JSON.stringify({newins: 'studentid'}));
            myobj.onreadystatechange = function () {
                if (myobj.readyState == 4 && myobj.status == 200) {
                    var answer = myobj.responseText;
                    if (answer == "null") {
                        jQuery("#shortanswerresponse").empty();
                        //do nothing else, it wasn't a short answer question and the answer should already automatically be loaded
                    }

                    else {
                        //manually show the answer now
                        answer = JSON.parse(answer);
                        jQuery("#shortanswerresponse").empty();
                        var answerheader = $("<b>Student's Answer</b> <br>")
                        jQuery("#shortanswerresponse").append(answerheader);
                        jQuery("#shortanswerresponse").append(answer);
                        $('#shortanswerresponse').css('display', 'inline');
                        $('#shortanswerresponse').css('margin-bottom', '50px');
                        $('#shortanswerresponse').css('background-color', '#fefce7');
                    }
                }
            }
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
       release_button = document.getElementById("releasebutton");
    release_button.style.visibility = 'visible';
    autograde_form.style.visibility = 'visible';
    calc_totals_form.style.visibility = 'visible';

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

    release_button = document.getElementById("releasebutton");
    release_button.style.visibility = 'hidden';
    autograde_form = document.getElementById("autogradingform");
    autograde_form.style.visibility = 'hidden';
    calc_totals_form = document.getElementById("calculateTotalsForm");
    calc_totals_form.style.visibility = 'hidden';

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


function remove_assignment() {
    var select = document.getElementById('assignlist');
    var assignmentid = select.options[select.selectedIndex].value;
    var assignmentname = select.options[select.selectedIndex].text;

    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/removeassign/' + assignmentid, true);
    obj.send(JSON.stringify({assignid: 'assignmentid'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            select.remove(select.selectedIndex)
        }
    }
}


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


function create_question(formdata) {


    var activetab;
    var formativetab = $('#formative').hasClass('clickedtab');
    var summativetab = $('#summative').hasClass('clickedtab');
    var externaltab = $('#external').hasClass('clickedtab');

    if (formativetab == true) {
        activetab = 'formative';
    }
    else if (summativetab == true) {
        activetab = 'summative';
    }

    else if (externaltab == true) {
        activetab = 'external';
    }

    var select = document.getElementById('assignlist');
    var assignmentid = select.options[select.selectedIndex].value;
    var assignmentname = select.options[select.selectedIndex].text;

    var template = formdata.template.value;


    var qcode = formdata.qcode.value;
    var lines = qcode.split('\n');
for(var i = 0;i < lines.length;i++){
    if (lines[i] != "") {
        var line = lines[i];
var match = line.split(/.. \w*:: /);
        var name = match[1];
        break

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
        'timed' : timed
    }
    url = '/runestone/admin/createquestion'
    jQuery.post(url, data, function (iserror, textStatus, whatever) {
            if (iserror == 'ERROR') {
                errortext = document.getElementById('qnameerror');
                errortext.innerHTML = 'Name is alerady in use. Please try a different name.'
            } else {
                alert('Question created successfully');
                var newPoints = iserror['points'];
                var q_type = activetab;
                var totalPoints = document.getElementById("totalPoints");
                totalPoints.innerHTML = 'Total points: ' + newPoints;
                var tableBody = document.getElementById("tableBody");
                var row = document.createElement("TR");
                row.setAttribute("class", q_type);
                row.setAttribute("id", name);
                row.style.textAlign = 'center';
                row.style.border = '1px solid black';
                tableBody.appendChild(row);

                var qid = document.createElement("TD");
                qid.style.border = '1px solid black';
                var qid_data = document.createTextNode(name);
                qid.appendChild(qid_data);
                row.appendChild(qid);

                var pts = document.createElement("TD");
                pts.style.border = '1px solid black';
                var pts_data = document.createTextNode(points);
                pts.appendChild(pts_data);
                row.appendChild(pts);

                var time = document.createElement("TD");
                time.style.border = '1px solid black';
                var time_data = document.createTextNode(timed);

                time.appendChild(time_data);
                row.appendChild(time);
            }
        }, 'json');
}


function assignmentInfo() {
    var select = document.getElementById('assignlist');
    var assignmentid = select.options[select.selectedIndex].value;
    var assignmentname = select.options[select.selectedIndex].text;
    $('#summative').css('background-color', 'gainsboro');
    $('#formative').css('background-color', 'transparent');
    $('#external').css('background-color', 'transparent');
    $('#rightSection').css('visibility','visible');


    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/assignmentInfo/?assignmentid=' + assignmentid, true);
    obj.send(JSON.stringify({variable: 'variable'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            var question_info = obj.responseText;
            var res = JSON.parse(question_info);
            var keys = [];
            var i;
            for (i in res) {
                if (res.hasOwnProperty(i) && i != 'assignment_points' && i != 'due_date' && i !=
                    'description') {
                    keys.push(i);
                }
            }
            var assignment_points = res['assignment_points'];
            var totalPoints = document.getElementById("totalPoints");
            totalPoints.innerHTML = 'Total points: ' + assignment_points;

            var duedate = res['due_date'];
            document.getElementById('assignment_duedate').innerHTML = 'Due: ' + duedate;

            var description = res['description'];
            document.getElementById('assignment_description').innerHTML = description;
            var tableBody = document.getElementById("tableBody");
            $("#tableBody").empty(); //clear the table body first, before adding anything
            for (k = 0; k < keys.length; k++) {
                var key = keys[k];
                question = res[key];

                //now populate entire table but only show rows with class 'summative'
                var type = question['type'];

                var row = document.createElement("TR");
                row.setAttribute("class", type);
                row.setAttribute("id", question['name']);
                row.style.textAlign = 'center';
                row.style.border = '1px solid black';
                tableBody.appendChild(row);

                var qid = document.createElement("TD");
                qid.style.border = '1px solid black';
                var qid_data = document.createTextNode(question['name']);
                qid.appendChild(qid_data);
                row.appendChild(qid);

                var pts = document.createElement("TD");
                pts.style.border = '1px solid black';
                var pts_data = document.createTextNode(question['points']);
                pts.appendChild(pts_data);
                row.appendChild(pts);

                var timed = document.createElement("TD");
                timed.style.border = '1px solid black';
                var timed_data = document.createTextNode(question['timed']);

                timed.appendChild(timed_data);
                row.appendChild(timed);
            }
            //by default hide the formative and external questions
            $(".formative").hide();
            $(".external").hide();
        }
        var leftpanel1 = document.getElementById("leftpanel1");
        leftpanel1.style.visibility = 'visible';
        var leftpanel2 = document.getElementById("leftpanel2");
        leftpanel2.style.visibility = 'visible';
    }
}


function createAssignment(form) {
    var name = form.name.value;
    var description = form.description.value;
    var duedate = form.datetimepicker.value;

    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/createAssignment/?name=' + name + '&description=' + description + '&due=' + duedate, true);
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
            } else {
                alert('Error in creating new assignment.')
            }
        }
    }
}


function showQuestions(type) {

    //New functionality, clear out the right hand side, blank search with no results showing
    $('#qbankselect').empty();
    $('#qbankselect').css('visibility', 'hidden');
    $('#questionform').css('visibility', 'hidden');
    $('#questionInfo').css('visibility', 'hidden');


    //Show all questions in table with class matching the type passed in, hide all other questions
    var typeToHide1;
    var typeToHide2;


    if (type == 'summative') {
        typeToHide1 = '.formative';
        typeToHide2 = '.external';
    }

    if (type == 'formative') {
        typeToHide1 = '.summative';
        typeToHide2 = '.external';
    }

    if (type == 'external') {
        typeToHide1 = '.formative';
        typeToHide2 = '.summative';
    }
    var question_type = '.' + type;
    $(question_type).show();
    $(typeToHide1).hide();
    $(typeToHide2).hide();
}


function getQuestions() {
    var select = document.getElementById('assignlist');
    var assignmentid = select.options[select.selectedIndex].value;
    var assignmentname = select.options[select.selectedIndex].text;
    var questions_list = document.getElementById('questions_list');
    //drop any of the questions that have been previously added to the select
    $("#questions_list").empty();
    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/getQuestions/?assignmentid=' + assignmentid, true);
    obj.send(JSON.stringify({variable: 'variable'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            var questions = JSON.parse(obj.responseText);
            for (i = 0; i < questions.length; i++) {
                var option = document.createElement("option");
                option.text = questions[i];
                option.value = assignmentid;
                questions_list.add(option);
            }
        }
    }
}


function remove_question() {
    var select = document.getElementById('questions_list');
    var question_name = select.options[select.selectedIndex].text;
    var assignment_id = select.options[select.selectedIndex].value;
    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/removeQuestion/?name=' + question_name + '&assignment_id=' + assignment_id, true);
    obj.send(JSON.stringify({variable: 'variable'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            var totalPoints = document.getElementById("totalPoints");
            totalPoints.innerHTML = 'Total points: ' + JSON.parse(obj.responseText);
            //remove from the select dropdown and remove from the table
            select.remove(select.selectedIndex);
            row = document.getElementById(question_name);
            row.parentNode.removeChild(row);
        }
    }
}


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

    var activetab;
    var formativetab = $('#formative').hasClass('clickedtab');
    var summativetab = $('#summative').hasClass('clickedtab');
    var externaltab = $('#external').hasClass('clickedtab');

    if (formativetab == true) {
        activetab = 'formative';
    }
    else if (summativetab == true) {
        activetab = 'summative';
    }

    else if (externaltab == true) {
        activetab = 'external';
    }

    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/questionBank?chapter=' + chapter + '&difficulty=' + difficulty + '&author=' + author + '&tags=' + tags + '&term=' + term + '&qtype=' + activetab, true);
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


function addToAssignment(form) {
    var points = form.points.value;
    var checked = document.getElementById('timed').checked;
    var select = document.getElementById('qbankselect');
    var question_name = select.options[select.selectedIndex].text;
    var assignlist = document.getElementById('assignlist');
    var assignmentid = assignlist.options[assignlist.selectedIndex].value;
    var activetab;
    var formativetab = $('#formative').hasClass('clickedtab');
    var summativetab = $('#summative').hasClass('clickedtab');
    var externaltab = $('#external').hasClass('clickedtab');

    if (formativetab == true) {
        activetab = 'formative';
    }
    else if (summativetab == true) {
        activetab = 'summative';
    }

    else if (externaltab == true) {
        activetab = 'external';
    }


    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/addToAssignment/?question=' + question_name + '&assignment=' + assignmentid + '&points=' + points + '&timed=' + checked + '&type=' + activetab, true);
    obj.send(JSON.stringify({variable: 'variable'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            var newPoints = JSON.parse(obj.responseText)[0];
            var q_type = JSON.parse(obj.responseText)[1];
            var totalPoints = document.getElementById("totalPoints");
            totalPoints.innerHTML = 'Total points: ' + newPoints;
            var tableBody = document.getElementById("tableBody");
            var row = document.createElement("TR");
            row.setAttribute("class", q_type);
            row.setAttribute("id", question_name);
            row.style.textAlign = 'center';
            row.style.border = '1px solid black';
            tableBody.appendChild(row);

            var qid = document.createElement("TD");
            qid.style.border = '1px solid black';
            var qid_data = document.createTextNode(question_name);
            qid.appendChild(qid_data);
            row.appendChild(qid);

            var pts = document.createElement("TD");
            pts.style.border = '1px solid black';
            var pts_data = document.createTextNode(points);
            pts.appendChild(pts_data);
            row.appendChild(pts);

            var timed = document.createElement("TD");
            timed.style.border = '1px solid black';
            var timed_data = document.createTextNode(checked);

            timed.appendChild(timed_data);
            row.appendChild(timed);

            if (q_type == 'summative') {
                $(".summative").show();
                $(".formative").hide();
                $(".external").hide();

                $('#summative').css('background-color', 'gainsboro');
                $('#formative').css('background-color', 'transparent');
                $('#external').css('background-color', 'transparent');

            }

            if (q_type == 'formative') {
                $(".formative").show();
                $(".summative").hide();
                $(".external").hide();

                $('#formative').css('background-color', 'gainsboro');
                $('#summative').css('background-color', 'transparent');
                $('#external').css('background-color', 'transparent');
            }
            if (q_type == 'external') {
                $(".external").show();
                $(".formative").hide();
                $(".summative").hide();

                $('#external').css('background-color', 'gainsboro');
                $('#summative').css('background-color', 'transparent');
                $('#formative').css('background-color', 'transparent');
            }

        }
    }
}


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

            var q_code = document.getElementById('q_code');
            q_code.innerHTML = code;

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

function questions2Rst() {
    var select = document.getElementById('assignlist');
    var assignmentid = select.options[select.selectedIndex].value;
    $.getJSON('/runestone/admin/questions2rst/' + assignmentid, {}, function () {
        alert("done")
    });
}


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


function changeDescription(form) {
    var newdescription = form.newdescription.value;
    var select = document.getElementById('assignlist');
    var assignmentid = select.options[select.selectedIndex].value;
    var obj = new XMLHttpRequest();
    obj.open('POST', '/runestone/admin/changeDescription?newdescription=' + newdescription + '&assignmentid=' + assignmentid, true);
    obj.send(JSON.stringify({variable: 'variable'}));
    obj.onreadystatechange = function () {
        if (obj.readyState == 4 && obj.status == 200) {
            if (obj.responseText == 'success') {
                alert("Successfully changed description");
                document.getElementById("assignment_description").innerHTML = newdescription;
            }

            else if (obj.responseText == 'error') {
                alert("There was an error changing your due date");
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




function release_grades() {
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
        var ids = JSON.parse(assignmentids);
        var assignmentid = ids[assignment];
        var obj = new XMLHttpRequest();
        obj.open('POST', '/runestone/admin/releasegrades?assignmentid=' + assignmentid, true);
        obj.send(JSON.stringify({variable: 'variable'}));
        obj.onreadystatechange = function () {
            if (obj.readyState == 4 && obj.status == 200) {
                alert("Grades released");
            }
        }
    }
}
