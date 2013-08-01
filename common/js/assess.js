var add_button = function (divid, expected, feedArray) {
    var bdiv = divid + "_bt";
    var element = document.createElement("input");
    element.setAttribute("type", "button");
    element.setAttribute("value", "Check Me!");
    element.setAttribute("name", "do check");
    element.onclick = function () {
        checkMCMFRandom(divid, expected, feedArray);
    };
    $("#" + bdiv).html(element);
};

var feedbackMCMFRandom = function (divid, correct, feedbackText) {
    if (correct) {
        $(divid).html('Correct!!  ' + feedbackText);
        //$(divid).css('background-color', '#C8F4AD');
        $(divid).attr('class','alert alert-success');
    } else {
        if (feedbackText == null) {
            feedbackText = '';
        }
        $(divid).html("Incorrect.  " + feedbackText);
        //$(divid).css('background-color', '#F4F4AD');
        $(divid).attr('class','alert alert-danger')
    }
};

var checkFIBStorage = function (divid, blankid, expected, feedback, casi) {
    var given = document.getElementById(blankid).value;
    // update number of trials??
    // log this to the db
    modifiers = '';
    if (casi) {
        modifiers = 'i'
    }
    var patt = RegExp(expected, modifiers);
    var isCorrect = patt.test(given);
    if (!isCorrect) {
        fbl = feedback;
        for (var i = 0; i < fbl.length; i++) {
            patt = RegExp(fbl[i][0]);
            if (patt.test(given)) {
                feedback = fbl[i][1];
                break;
            }
        }
    }

    // store the answer in local storage
    var storage_arr = new Array();
    storage_arr.push(given);
    storage_arr.push(expected);
    localStorage.setItem(divid, storage_arr.join(";"));

    feedBack('#' + divid + '_feedback', isCorrect, feedback);
    var answerInfo = 'answer:' + given + ":" + (isCorrect ? 'correct' : 'no');
    logBookEvent({'event': 'fillb', 'act': answerInfo, 'div_id': divid});
    document.getElementById(divid + '_bcomp').disabled = false;    
};

var feedBack = function (divid, correct, feedbackText) {
    if (correct) {
        $(divid).html('You are Correct!');
        //$(divid).css('background-color', '#C8F4AD');
        $(divid).attr('class','alert alert-success');
    } else {
        if (feedbackText == null) {
            feedbackText = '';
        }
        $(divid).html("Incorrect.  " + feedbackText);
        //$(divid).css('background-color', '#F4F4AD');
        $(divid).attr('class','alert alert-danger');
    }
};


/* 
 Multiple Choice with Feedback for each answer
 */
var feedBackMCMF = function (divid, correct, feedbackText) {
    if (correct) {
        $(divid).html('Correct!!  ' + feedbackText);
        //$(divid).css('background-color', '#C8F4AD');
        $(divid).attr('class','alert alert-success');
    } else {
        if (feedbackText == null) {
            feedbackText = '';
        }
        $(divid).html("Incorrect.  " + feedbackText);
        //$(divid).css('background-color', '#F4F4AD');
        $(divid).attr('class','alert alert-danger');
    }
};

/*
 Multiple Choice with Multiple Answers
 */
var feedBackMCMA = function (divid, numCorrect, numNeeded, numGiven, feedbackText) {
    var answerStr = "answers";
    if (numGiven == 1) answerStr = "answer";

    if (numCorrect == numNeeded && numNeeded == numGiven) {
        $(divid).html('Correct!  <br />' + feedbackText);
        //$(divid).css('background-color', '#C8F4AD');
        $(divid).attr('class', 'alert alert-success');
    } else {
        $(divid).html("Incorrect.  " + "You gave " + numGiven +
            " " + answerStr + " and got " + numCorrect + " correct of " +
            numNeeded + " needed.<br /> " + feedbackText);
        //$(divid).css('background-color', '#F4F4AD');
        $(divid).attr('class', 'alert alert-danger');
    }
};

/* Randomize options */

var createHTML_MCMFRandom = function (divid, answerString, feedString, corrAnswer) {
    var i, j, k, l, len;
    var arr = new Array();
    var fr = new Array();
    var alpha = ['a', 'b', 'c', 'd', 'e'];
    var ansArray = new Array();
    var feedArray = new Array();
    var hash = new Array();

    arr = answerString.split("*separator*");
    fr = feedString.split("*separator*");

    for (j = 0; j < arr.length - 1; j++) {
        ansArray[j] = arr[j];
        hash[ansArray[j]] = fr[j];
    }

    i = ansArray.length;
    len = i;
    if (i == 0) return false;
    while (--i) {
        var j = Math.floor(Math.random() * ( i + 1 ));
        var tempi = ansArray[i];
        var tempj = ansArray[j];
        ansArray[i] = tempj;
        ansArray[j] = tempi;
    }

    for (i = 0; i < ansArray.length; i++) {
        k = ansArray[i];
        feedArray[i] = hash[k];
    }

    for (l = 0; l < len; l++) {
        var rad = "<input type='radio' name='group1' value='" + l + "'/>" + "<label for= 'opt_" + l + "'>" + "  " + alpha[l] + ")  " + ansArray[l] + "</label><br />";
        var opdiv = divid + "_op" + (l + 1);
        $("#" + opdiv).html(rad);

    }

    var index = ansArray.indexOf(corrAnswer);
    add_button(divid, index, feedArray);

    return true;
};

var checkMCMFRandom = function (divid, expected, feed) {
    var given;
    var feedback = null;
    var buttonObjs = document.forms[divid + "_form"].elements.group1;
    for (var i = buttonObjs.length - 1; i >= 0; i--) {
        if (buttonObjs[i].checked) {
            given = buttonObjs[i].value;
            feedback = feed[i];
        }
    }

    // log the answer
    var answerInfo = 'answer:' + given + ":" + (given == expected ? 'correct' : 'no');
    logBookEvent({'event': 'mChoice', 'act': answerInfo, 'div_id': divid});

    // give the user feedback
    feedbackMCMFRandom('#' + divid + '_feedback', given == expected, feedback);
};

/* Local Storage */

var resetPage = function (divid) {

    var i;
    var id = new Array();
    var keyArr = new Array();
    id = divid.split("_");
    var pageNum = id[1];
    location.reload();

    //erasing data from local storage
    var len = localStorage.length;
    if (len > 0) {
        for (i = 0; i < len; i++) {
            var key = localStorage.key(i);
            var str = key.substring(0, 1);
            if (str === pageNum) {
                keyArr.push(key);
            }
        }
    }
    for (i = 0; i < keyArr.length; i++)
        localStorage.removeItem(keyArr[i]);
};

var checkRadio = function (divid) {
    // This function repopulates MCMF questions with a user's previous answers,
    // which were previously stored into local storage

    var qnum = divid;
    var len = localStorage.length;

    //retrieving data from local storage
    if (len > 0) {
        for (var i = 0; i < len; i++) {
            var key = localStorage.key(i);
            if (key === qnum) {
                var ex = localStorage.getItem(key);
                var arr = ex.split(";");
                var str = key + "_opt_" + arr[0];
                $("#" + str).attr("checked", "true");
                document.getElementById(divid + '_bcomp').disabled = false;
            }
        }
    }
};

var checkMultipleSelect = function (divid) {
    // This function repopulates MCMA questions with a user's previous answers,
    // which were stored into local storage.

    var qnum = divid;
    var len = localStorage.length;

    if (len > 0) {
        for (var i = 0; i < len; i++) {
            var key = localStorage.key(i);
            if (key === qnum) {
                var ex = localStorage.getItem(key);
                var arr = ex.split(";");
                var answers = arr[0].split(",");
                for (var a = 0; a < answers.length; a++) {
                    var str = key + "_opt_" + answers[a];
                    $("#" + str).attr("checked", "true");
                    document.getElementById(divid + '_bcomp').disabled = false;
                }
            }
        }
    }
};

var checkPreviousFIB = function (divid) {
    // This function repoplulates FIB questions with a user's previous answers,
    // which were stored into local storage

    var qnum = divid;
    var len = localStorage.length;

    if (len > 0) {
        for (var i = 0; i < len; i++) {
            var key = localStorage.key(i);
            if (key === qnum) {
                var ex = localStorage.getItem(key);
                var arr = ex.split(";");
                var str = key + "_ans1";
                $("#" + str).attr("value", arr[0]);
                document.getElementById(divid + '_bcomp').disabled = false;                
            }
        }
    }
};

var checkMCMAStorage = function (divid, expected, feedbackArray) {
    var given;
    var feedback = "";
    var correctArray = expected.split(",");
    correctArray.sort();
    var givenArray = [];
    var correctCount = 0;
    var correctIndex = 0;
    var givenIndex = 0;
    var givenlog = '';
    var buttonObjs = document.forms[divid + "_form"].elements.group1;

    // loop through the checkboxes
    for (var i = 0; i < buttonObjs.length; i++) {
        if (buttonObjs[i].checked) { // if checked box
            given = buttonObjs[i].value; // get value of this button
            givenArray.push(given)    // add it to the givenArray
            feedback += given + ": " + feedbackArray[i] + "<br />"; // add the feedback
            givenlog += given + ",";
        }
    }
    // sort the given array
    givenArray.sort();

    while (correctIndex < correctArray.length &&
        givenIndex < givenArray.length) {
        if (givenArray[givenIndex] < correctArray[correctIndex]) {
            givenIndex++;
        }
        else if (givenArray[givenIndex] == correctArray[correctIndex]) {
            correctCount++;
            givenIndex++;
            correctIndex++;
        }
        else {
            correctIndex++;
        }

    } // end while

    // save the data into local storage
    var storage_arr = new Array();
    storage_arr.push(givenArray);
    storage_arr.push(expected);
    localStorage.setItem(divid, storage_arr.join(";"));

    // log the answer
    var answerInfo = 'answer:' + givenlog.substring(0, givenlog.length - 1) + ':' +
        (correctCount == correctArray.length ? 'correct' : 'no');
    logBookEvent({'event': 'mChoice', 'act': answerInfo, 'div_id': divid});

    // give the user feedback
    feedBackMCMA('#' + divid + '_feedback', correctCount,
        correctArray.length, givenArray.length, feedback);

    document.getElementById(divid + '_bcomp').disabled = false;
};

var checkMCMFStorage = function (divid, expected, feedbackArray) {
    var given;
    var feedback = null;
    var buttonObjs = document.forms[divid + "_form"].elements.group1;
    for (var i = buttonObjs.length - 1; i >= 0; i--) {
        if (buttonObjs[i].checked) {
            given = buttonObjs[i].value;
            feedback = feedbackArray[i];
        }
    }

    //Saving data in local storage
    var storage_arr = new Array();
    storage_arr.push(given);
    storage_arr.push(expected);
    localStorage.setItem(divid, storage_arr.join(";"));

    // log the answer
    var answerInfo = 'answer:' + given + ":" + (given == expected ? 'correct' : 'no');
    logBookEvent({'event': 'mChoice', 'act': answerInfo, 'div_id': divid});

    // give the user feedback
    feedBackMCMF('#' + divid + '_feedback', given == expected, feedback);
    document.getElementById(divid + '_bcomp').disabled = false;
};


// for each form in the div
//    get the id of the form
//    call checkMe on the form...  -- need metadata what kind of question what parms etc
//    hidden fields for meta data??? each form defines a checkme function with no parameters
//    that calls the actual function that checks the answer properly??
// summarize

