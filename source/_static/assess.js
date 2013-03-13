var createHTML_MCMFRandom=function(divid,qnum,qtext,answerString,feedString,corrAnswer)
{
            var j;
            var ar= new Array();
            var fr= new Array();
            var ansArray= new Array();
            var feedArray=new Array();
            var hash=new Array();
            
            arr=answerString.split(",");
            fr=feedString.split("::");
            
            for(j=0;j<arr.length-1;j++)
            {
            ansArray[j]=arr[j];
            hash[ansArray[j]]=fr[j];
            }
            
            var i = ansArray.length;
            if ( i == 0 ) return false;
            while ( --i ) {
            var j = Math.floor( Math.random() * ( i + 1 ) );
            var tempi = ansArray[i];
            var tempj = ansArray[j];
            ansArray[i] = tempj;
            ansArray[j] = tempi;
            }
            
            for(i=0;i<ansArray.length;i++)
            {
            var k=ansArray[i];
            feedArray[i]=hash[k];
            }
            
            var o1="<input type='radio' name='group1' value='0'/>"+"<label for= 'opt_1'>  a) "+ansArray[0]+"</label><br />";
            var o2="<input type='radio' name='group1' value='1'/>"+"<label for= 'opt_2'>  b) "+ansArray[1]+"</label><br />";
            var o3="<input type='radio' name='group1' value='2'/>"+"<label for= 'opt_3'>  c) "+ansArray[2]+"</label><br />";
            var o4="<input type='radio' name='group1' value='3'/>"+"<label for= 'opt_4'>  d) "+ansArray[3]+"</label><br />";
                        
            var qdiv=divid+"_question";
            var opdiv1 = divid+ "_op1";
            var opdiv2 = divid+ "_op2";
            var opdiv3 = divid+ "_op3";
            var opdiv4 = divid+ "_op4";
            var resdiv = "#"+divid+"_test";
            
            $("#"+qdiv).html("<br>"+qnum+" "+ qtext);
            $("#"+opdiv1).html(o1);
            $("#"+opdiv2).html(o2);
            $("#"+opdiv3).html(o3);
            $("#"+opdiv4).html(o4);
            
            var index=ansArray.indexOf(corrAnswer);
            add_button(divid,index,feedArray);  
};
            
var add_button=function(divid,expected,feedArray)
{
    var bdiv = divid+"_bt";
    var element = document.createElement("input");
    element.setAttribute("type", "button");
    element.setAttribute("value", "Check Me!");
    element.setAttribute("name", "do check");
    element.onclick=function(){checkMCMFRandom(divid,expected,feedArray);};
    $("#"+bdiv).html(element);
};

var checkMCMFRandom=function(divid,expected,feed)
{
    var given;
    var feedback = null;
	var buttonObjs = document.forms[divid+"_form"].elements.group1;
	for (var i = buttonObjs.length - 1; i >= 0; i--) {
		if (buttonObjs[i].checked) {
			given = buttonObjs[i].value;
            feedback = feed[i];
		}
	}
	// log the answer
    var answerInfo = 'answer:' + given + ":" + (given == expected ? 'correct' : 'no');
    logBookEvent({'event':'mChoice','act': answerInfo, 'div_id':divid}); 
    
    // give the user feedback
	feedbackMCMFRandom('#'+divid+'_feedback',given == expected, feedback);
};

var feedbackMCMFRandom = function(divid,correct,feedbackText) {
	if (correct) {
		$(divid).html('Correct!!  ' + feedbackText);
        $(divid).css('background-color','#C8F4AD');
	} else {
		$(divid).html("Incorrect.  " + feedbackText );
        $(divid).css('background-color','#F4F4AD');
	}
};

var checkMe = function(divid, expected, feedback) {
	var given;
	var buttonObjs = document.forms[divid+"_form"].elements.group1;
	for (var i = buttonObjs.length - 1; i >= 0; i--) {
		if (buttonObjs[i].checked) {
			given = buttonObjs[i].value;
		}
	}
	// update number of trials??
	// log this to the db
	feedBack('#'+divid+'_feedback',given == expected, feedback);
	var answerInfo = 'answer:' + given + ":"  + (given==expected ? 'correct' : 'no');
	logBookEvent({'event':'assses', 'act':answerInfo, 'div_id':divid});
};

var checkFIB = function(divid, expected, feedback, casi) {
  var given = document.forms[divid+"_form"].elements.blank.value;
  // update number of trials??
  // log this to the db
  modifiers = ''
  if (casi) {
    modifiers = 'i'
  }
  var patt = RegExp(expected,modifiers)
  var isCorrect = patt.test(given)
  if (! isCorrect) {
    fbl = feedback;
    for (var i=0; i< fbl.length; i++) {
      patt = RegExp(fbl[i][0])
      if (patt.test(given)) {
        feedback = fbl[i][1];
        break;
      }
    }

  }
  feedBack('#'+divid+'_feedback',isCorrect, feedback);
  var answerInfo = 'answer:' + given + ":"  + (isCorrect ? 'correct' : 'no');
  logBookEvent({'event':'assses', 'act':answerInfo, 'div_id':divid});
};

var feedBack = function(divid,correct,feedbackText) {
	if (correct) {
      $(divid).html('You are Correct!');
      $(divid).css('background-color','#C8F4AD');
   	} else {
	    $(divid).html("Incorrect.  " + feedbackText );
      $(divid).css('background-color','#F4F4AD');		
	}
};


/* 
Multiple Choice with Feedback for each answer
*/

var checkMCMF = function(divid, expected, feedbackArray) {
	var given;
    var feedback = null;
	var buttonObjs = document.forms[divid+"_form"].elements.group1;
	for (var i = buttonObjs.length - 1; i >= 0; i--) {
		if (buttonObjs[i].checked) {
			given = buttonObjs[i].value;
            feedback = feedbackArray[i];
		}
	}
	// log the answer
  var answerInfo = 'answer:' + given + ":" + (given == expected ? 'correct' : 'no');
  logBookEvent({'event':'mChoice','act': answerInfo, 'div_id':divid}); 
    
    // give the user feedback
	feedBackMCMF('#'+divid+'_feedback',given == expected, feedback);
};


var feedBackMCMF = function(divid,correct,feedbackText) {
	if (correct) {
		$(divid).html('Correct!!  ' + feedbackText);
        $(divid).css('background-color','#C8F4AD');
	} else {
		$(divid).html("Incorrect.  " + feedbackText );
        $(divid).css('background-color','#F4F4AD');
	}
};

var checkMCMA = function(divid, expected, feedbackArray) {
	var given;
    var feedback = "";
    var correctArray = expected.split(",");
    correctArray.sort();
    var givenArray = [];
    //var allThere = true;
    var correctCount = 0;
    var correctIndex = 0;
    var givenIndex = 0;
    var givenlog = '';
	var buttonObjs = document.forms[divid+"_form"].elements.group1;
    
    // loop through the checkboxes
	for (var i = 0;  i < buttonObjs.length; i++) {
		if (buttonObjs[i].checked) { // if checked box
			given = buttonObjs[i].value; // get value of this button
            givenArray.push(given)    // add it to the givenArray
            feedback+=given + ": " + feedbackArray[i] + "<br />"; // add the feedback
            givenlog += given + ",";
		}
	}
    // sort the given array
    givenArray.sort();
    
    //if (givenArray.length != choiceArray.length) {
    //        allThere = false;
    //}
  
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

     // for (var i=0; i < choiceArray.length; i++) {
     //   if (choiceArray[i] != givenArray[i]) {
     //       allThere = false;
     //   }

    } // end while
    
	// log the answer
  var answerInfo = 'answer:' + givenlog.substring(0,givenlog.length-1) + ':' +
    (correctCount == correctArray.length ? 'correct' : 'no');
    logBookEvent({'event':'mChoice','act': answerInfo, 'div_id':divid}); 
    
	// give the user feedback
	feedBackMCMA('#'+divid+'_feedback', correctCount,
                 correctArray.length, givenArray.length, feedback);
};


/*
 Multiple Choice with Multiple Answers
*/
var feedBackMCMA = function(divid,numCorrect,numNeeded,numGiven,feedbackText) {   
    var answerStr = "answers";
    if (numGiven == 1) answerStr = "answer";
    
	if (numCorrect == numNeeded && numNeeded == numGiven) {
		$(divid).html('Correct!  <br />' + feedbackText);
        $(divid).css('background-color','#C8F4AD');
	} else {
		$(divid).html("Incorrect.  " +  "You gave " + numGiven + 
        " " + answerStr + " and got " + numCorrect + " correct of " +
         numNeeded + " needed.<br /> " + feedbackText );
        $(divid).css('background-color','#F4F4AD');
	}
};

/* Randomize options */

var createHTML_MCMFRandom=function(divid,answerString,feedString,corrAnswer)
{
            var i,j,k,l,len;
            var arr= new Array();
            var fr= new Array();
            var alpha=['a','b','c','d','e'];
            var ansArray= new Array();
            var feedArray=new Array();
            var hash=new Array();
            
            arr=answerString.split("*separator*");
            fr=feedString.split("*separator*");
            
            for(j=0;j<arr.length-1;j++)
            {
            ansArray[j]=arr[j];
            hash[ansArray[j]]=fr[j];
            }
            
            i = ansArray.length;
            len=i;
            if ( i == 0 ) return false;
            while ( --i ) {
            var j = Math.floor( Math.random() * ( i + 1 ) );
            var tempi = ansArray[i];
            var tempj = ansArray[j];
            ansArray[i] = tempj;
            ansArray[j] = tempi;
            }
            
            for(i=0;i<ansArray.length;i++)
            {
            k=ansArray[i];
            feedArray[i]=hash[k];
            }
            
            for(l=0;l<len;l++)
            {
                var rad="<input type='radio' name='group1' value='"+l+"'/>"+"<label for= 'opt_"+l+"'>"+"  "+alpha[l]+")  "+ansArray[l]+"</label><br />";
                var opdiv = divid+ "_op"+(l+1);
                $("#"+opdiv).html(rad);

            }
            
            var index=ansArray.indexOf(corrAnswer);
            add_button(divid,index,feedArray);  
};
            
var add_button=function(divid,expected,feedArray)
{
    var bdiv = divid+"_bt";
    var element = document.createElement("input");
    element.setAttribute("type", "button");
    element.setAttribute("value", "Check Me!");
    element.setAttribute("name", "do check");
    element.onclick=function(){checkMCMFRandom(divid,expected,feedArray);
    };
    $("#"+bdiv).html(element);
};

var checkMCMFRandom=function(divid,expected,feed)
{
    var given;
    var feedback = null;
	var buttonObjs = document.forms[divid+"_form"].elements.group1;
	for (var i = buttonObjs.length - 1; i >= 0; i--) {
		if (buttonObjs[i].checked) {
			given = buttonObjs[i].value;
            feedback = feed[i];
		}
	}
        
	// log the answer
    var answerInfo = 'answer:' + given + ":" + (given == expected ? 'correct' : 'no');
    logBookEvent({'event':'mChoice','act': answerInfo, 'div_id':divid}); 
    
    // give the user feedback
	feedbackMCMFRandom('#'+divid+'_feedback',given == expected, feedback);
};

var feedbackMCMFRandom = function(divid,correct,feedbackText) {
	if (correct) {
		$(divid).html('Correct!!  ' + feedbackText);
        $(divid).css('background-color','#C8F4AD');
	} else {
		$(divid).html("Incorrect.  " + feedbackText );
        $(divid).css('background-color','#F4F4AD');
	}
};

/* Local Storage */

var resetPage = function(divid){
    
    var i;
    var id=new Array();
    var keyArr=new Array();
    id=divid.split("_");
    var pageNum=id[1];
    location.reload();
        
    //erasing data from local storage
    var len=localStorage.length;
    if(len>0)
    {
        for(i=0; i<len; i++)
        {
            var key = localStorage.key(i);
            var str = key.substring(0,1);
            if(str===pageNum)
                {
                    keyArr.push(key);
                }
        }
    }
    for(i=0;i<keyArr.length;i++)
        localStorage.removeItem(keyArr[i]);
};

var checkRadio = function(divid){
    
    var qnum=divid.substring(13,divid.length);
    var len=localStorage.length;
    
        //retrieving data from local storage
    if(len>0)
    {
        for(var i=0; i<len; i++)
        {
            var key = localStorage.key(i);
            if(key===qnum)
                {
                    var ex=localStorage.getItem(key);
                    var arr=ex.split(",");
                    var str="test_question"+key+"_opt_"+arr[0];
                    $("#"+str).attr("checked","true");
                }
        }
    }
};

var checkMCMFStorage = function(divid, expected, feedbackArray) {
	var given;
    var feedback = null;
	var buttonObjs = document.forms[divid+"_form"].elements.group1;
	for (var i = buttonObjs.length - 1; i >= 0; i--) {
		if (buttonObjs[i].checked) {
			given = buttonObjs[i].value;
            feedback = feedbackArray[i];
		}
	}
    
    //Saving data in local storage
    var storage_arr=new Array();
    storage_arr.push(given);
    storage_arr.push(expected);
    localStorage.setItem(divid.substring(13,divid.length),  storage_arr.join(","));
    
    // log the answer
  var answerInfo = 'answer:' + given + ":" + (given == expected ? 'correct' : 'no');
  logBookEvent({'event':'mChoice','act': answerInfo, 'div_id':divid}); 
    
    // give the user feedback
	feedBackMCMF('#'+divid+'_feedback',given == expected, feedback);
};



// for each form in the div
//    get the id of the form
//    call checkMe on the form...  -- need metadata what kind of question what parms etc
//    hidden fields for meta data??? each form defines a checkme function with no parameters
//    that calls the actual function that checks the answer properly??
// summarize

