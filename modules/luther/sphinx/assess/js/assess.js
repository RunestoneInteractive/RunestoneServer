
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
        $(divid).html('Correct!  ' + feedbackText);
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
    localStorage.setItem(eBookConfig.email + ":" + divid, storage_arr.join(";"));

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
        $(divid).html('Correct!  ' + feedbackText);
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
    // This function repopulates a MCMF question with a user's previous answer,
    // which was previously stored into local storage

    var len = localStorage.length;

    //retrieving data from local storage
    if (len > 0) {
      var ex = localStorage.getItem(eBookConfig.email + ":" + divid);
      if (ex !== null)
      {
      	var arr = ex.split(";");
      	var str = divid + "_opt_" + arr[0];
      	$("#" + str).attr("checked", "true");
      	document.getElementById(divid + '_bcomp').disabled = false;
      } // end if not null
    } // end if (len > 0)
};

function getMCAnswerForDivid(divid) {
var len = localStorage.length;

    //retrieving answer from local storage
    if (len > 0) {
      var ex = localStorage.getItem(eBookConfig.email + ":" + divid);
      if (ex !== null)
      {
      	var arr = ex.split(";");
      	return arr[0];
      }
    }
    return null;
}

var checkTimedRadio = function (divid) {
    // This function repopulates a MCMF question with a user's previous answer,
    // which was previously stored into local storage

    var len = localStorage.length;

    //retrieving data from local storage
    if (len > 0) {
      var ex = localStorage.getItem(eBookConfig.email + ":" + divid);
      if (ex !== null)
      {
      	var arr = ex.split(";");
      	var str = divid + "_opt_" + arr[0];
      	$("#" + str).attr("checked", "true");
      	document.getElementById(str).disabled = true;
      } // end if not null
    } // end if (len > 0)
};

var tookTimedExam = function () {

   $("#output").css({
			'width': '50%',
			'margin': '0 auto',
			'background-color': '#DFF0D8',
			'text-align': 'center',
			'border': '2px solid #DFF0D8',
			'border-radius': '25px'
		});
		
		$("#results").css({
			'width': '50%',
			'margin': '0 auto',
			'background-color': '#DFF0D8',
			'text-align': 'center',
			'border': '2px solid #DFF0D8',
			'border-radius': '25px'
		});

        $(".tooltipTime").css({
		    'margin': '0',
		    'padding': '0',
		    'background-color': 'black',
		    'color' : 'white'
		});

   var len = localStorage.length;
   var pageName = getPageName();
   if (len > 0) {
      if (localStorage.getItem(eBookConfig.email + ":timedExam:" + pageName) !== null) 
         return 1;
      else return 0;
   }
   else return 0;
}

var checkMultipleSelect = function (divid) {
    // This function repopulates MCMA questions with a user's previous answers,
    // which were stored into local storage.

    var len = localStorage.length;
    if (len > 0) {
        
    	var ex = localStorage.getItem(eBookConfig.email + ":" + divid);
    	if (ex !== null) {
           var arr = ex.split(";");
           var answers = arr[0].split(",");
           for (var a = 0; a < answers.length; a++) {
              var str = key + "_opt_" + answers[a];
              $("#" + str).attr("checked", "true");
              document.getElementById(divid + '_bcomp').disabled = false;
           } // end for
        } // end if
    } // end if len > 0
};

var checkPreviousFIB = function (divid) {
    // This function repoplulates FIB questions with a user's previous answers,
    // which were stored into local storage

    var len = localStorage.length;

    if (len > 0) {
    	var ex = localStorage.getItem(eBookConfig.email + ":" + divid);
    	if (ex !== null) {
           var arr = ex.split(";");
           var str = key + "_ans1";
           $("#" + str).attr("value", arr[0]);
           document.getElementById(divid + '_bcomp').disabled = false;                
        } // end if ex not null
    } // end if len > 0
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
    localStorage.setItem(eBookConfig.email + ":" + divid, storage_arr.join(";"));

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
    localStorage.setItem(eBookConfig.email + ":" + divid, storage_arr.join(";"));

    // log the answer
    var answerInfo = 'answer:' + given + ":" + (given == expected ? 'correct' : 'no');
    logBookEvent({'event': 'mChoice', 'act': answerInfo, 'div_id': divid});

    // give the user feedback
    feedBackMCMF('#' + divid + '_feedback', given == expected, feedback);
    document.getElementById(divid + '_bcomp').disabled = false;
};

var correctArray = [];
var feedbackArray = [];
var divArray = [];


var populateArrays = function (divid, expected, feedbackList){
	correctArray.push(expected);	
	divArray.push(divid);
	feedbackArray.push(feedbackList);
};

function getPageName() {

    var pageName = window.location.pathname.split("/").slice(-1);
	var name = pageName[0];
	return name;
}

function checkTimedMCMFStorage(){
    var given;
    var divid;
    var feedback = null;
    var hasAns;
    var expected;
    var numQuest = divArray.length;
    var op;
    var correct = 0;
    var skipped = 0;
    var answer = " ";

    if(!taken) {
	$('#pause').attr('disabled',true);
	$('#finish').attr('disabled',true);
	
	// loop through the items in the divArray
    for (var j = 0; j<= divArray.length -1;j++){

	    divid = divArray[j];
	    var buttonObjs = document.forms[divid + "_form"].elements.group1;
	    hasAns = 0; // reset each iteration of the loop 
	    answer = " "; // reset each iteration of the loop
	    
	    // loop through each option since we are showing feedback for each option
	    for (var i = 0 ; i <=buttonObjs.length - 1; i++) 
	    {
		    given = buttonObjs[i].value;
		    expected = correctArray[j];
		    feedback = feedbackArray[j][i];
		    
		    // give the user feedback
		    op = String.fromCharCode(i+97);
		    var selected = buttonObjs[i].checked
		    buttonObjs[i].disabled = true;
		    feedBackTimedMCMF('#' + divid + '_eachFeedback_' + op, given == expected, feedback);
		    
		    // if this was the selected choice
		    if (selected)
		    {
		       answer = given;
               hasAns = selected; 
                
               // log the answer
	           var answerInfo = 'answer:' + answer + ":" + (given == expected ? 'correct' : 'no');
	           logBookEvent({'event': 'mChoice', 'act': answerInfo, 'div_id': divid});

	    	   if (given == expected)
	    	   {
	    	      correct++;
	    	   }
	    	} // end if selected
	     } // end for
	     
	     // if no answer was selected
	     if(!hasAns) {
	       given = 1;
	       expected = 0;
		   feedback = '';	
		   skipped++;	
	    }

	    //Save answer in local storage
	    if (hasAns) {
	       var storage_arr = new Array();
	       storage_arr.push(answer);
	       storage_arr.push(expected);
	       localStorage.setItem(eBookConfig.email + ":" + divid, storage_arr.join(";"));
	    }

    }
    
    // show the results
	var percent = (correct/numQuest)*100;
	var wrong = numQuest - correct - skipped;
	document.getElementById("results").innerHTML = "Num Correct: " + correct + " Num Wrong: " + wrong + " Num Skipped: " + skipped + " Percent Correct: " + percent + "%";
	var result = correct + ";" + wrong + ";" + skipped;
	logBookEvent({'event': 'timedExam', 'act': 'end:' + correct + ":" + wrong + ":" + skipped, 'div_id': getPageName()});
	localStorage.setItem(eBookConfig.email + ":timedExamResult:" + getPageName(), result);
	
	taken = 1;
    running = 0;
  } // end if !taken
  
};

function resetTimedMCMFStorage(){
    var given;
    var divid;
    var feedback = null;
    var expected;
    var op;
	
	// loop through the items in the divArray
    for (var j = 0; j<= divArray.length -1;j++) {
    
	    divid = divArray[j];
	    var buttonObjs = document.forms[divid + "_form"].elements.group1;
	    
	    // loop through each option since we are showing feedback for each option
	    for (var i = 0 ; i <=buttonObjs.length - 1; i++) 
	    {
		    op = String.fromCharCode(i+97);
		    buttonObjs[i].disabled = true;
		    given = buttonObjs[i].value;
		    expected = correctArray[j];
		    feedback = feedbackArray[j][i];
		    feedBackTimedMCMF('#' + divid + '_eachFeedback_' + op, given == expected, feedback);
	     } // end for
	    
    } // end for loop through divArray
    
    
    var result = localStorage.getItem(eBookConfig.email + ":timedExamResult:" + getPageName());
    if (result !== null)
    {
       var resultArr = result.split(";");
       var correct = resultArr[0];
       var wrong = resultArr[1];
       var skipped = resultArr[2];
       var percent = correct / divArray.length * 100;
       document.getElementById("results").innerHTML = "Num Correct: " + correct + " Num Wrong: " + wrong + " Num Skipped: " + skipped + " Percent Correct: " + percent + "%";
    }
  
};


var feedBackTimedMCMF = function (divid, correct, feedbackText) {
    if (correct) {
        $(divid).html('Correct Answer.  ' + feedbackText);
        $(divid).attr('class','alert alert-success');
	
    } else {
        if (feedbackText == null) {
            feedbackText = '';
        }
        $(divid).html("Incorrect Answer.  " + feedbackText);
        $(divid).attr('class','alert alert-danger');
    }
};

var checkIfFinished = function () {
   if(tookTimedExam())
   {
        $('#start').attr('disabled',true);
		$('#pause').attr('disabled',true);
		$('#finish').attr('disabled',true);
		resetTimedMCMFStorage();
		$("#timed_Test").show();
	}
};


var paused = 0;
var running = 0;
var done = 0;
var taken = 0;


function start(){

	if(tookTimedExam() == 0){

		$('#start').attr('disabled',true);
		if(running == 0 && paused == 0){
			running = 1;
			$("#timed_Test").show();
			//document.getElementById("button_show").innerHTML = "Currently Taking Timed Quiz";
			increment();
			var name = getPageName();
	        logBookEvent({'event': 'timedExam', 'act': 'start', 'div_id': name});
	        localStorage.setItem(eBookConfig.email + ":timedExam:" + name, "started");
		}
	} 
};



function pause(){
	if(done == 0){
		if(running == 1){
			running = 0;
			paused = 1;
			//document.getElementById("button_show").innerHTML = "Timed Quiz Paused/Not Started";
			document.getElementById("pause").innerHTML = "Resume";
			$("#timed_Test").hide();
			

		}else{
			running = 1;
			paused = 0;
			increment();
			//document.getElementById("button_show").innerHTML = "Currently Taking Timed Quiz";
			document.getElementById("pause").innerHTML = "Pause";
			$("#timed_Test").show();
			
		}
	}
};

function getTime() {
        var mins = Math.floor(time/60);
		var secs = Math.floor(time) % 60;
		
		if(mins<10){
			mins = "0" + mins;
		}
		if(secs<10){
			secs = "0" + secs;
		}
		return mins + ":" + secs;
}

function showTime(time){
		var mins = Math.floor(time/60);
		var secs = Math.floor(time) % 60;
		
		if(mins<10){
			mins = "0" + mins;
		}
		if(secs<10){
			secs = "0" + secs;
		}
		
		document.getElementById("output").innerHTML = "Time Remaining  " + mins + ":" + secs;
		var timeTips = document.getElementsByClassName("timeTip");
			for(var i = 0; i<= timeTips.length - 1; i++){
				timeTips[i].title = mins + ":" + secs;
		}
}		
		
function increment(){

    // if running (not paused) and not taken
	if(running == 1 & !taken) {
	
		setTimeout(function() {
		time--;
		showTime(time);
		
		   if(time>0){
			  increment();
			  
			// ran out of time
		   }else{
			   running = 0;
			   done = 1;
			
			   if(taken == 0){
			     checkTimedMCMFStorage();
			   }
		  }
		},1000);		
	}

};








// for each form in the div
//    get the id of the form
//    call checkMe on the form...  -- need metadata what kind of question what parms etc
//    hidden fields for meta data??? each form defines a checkme function with no parameters
//    that calls the actual function that checks the answer properly??
// summarize

