/**
 * Created by IntelliJ IDEA.
 * User: bmiller
 * Date: 4/20/11
 * Time: 2:01 PM
 * To change this template use File | Settings | File Templates.
 */

/*

Copyright (C) 2011  Brad Miller  bonelake@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

*/

/* This should come from a config object loaded by the book...
   something like configjs  */



function handleEdKeys(ed, e) {
    if (e.keyCode === 13) {
        if (e.ctrlKey) {
            e.stop();
            runit(ed.parentDiv);
        }
        else if (e.shiftKey) {
            e.stop();
            eval(Sk.importMainWithBody("<stdin>", false, ed.selection()));
        }
    } else {
        if (ed.acEditEvent == false || ed.acEditEvent === undefined) {
            $('#'+ed.parentDiv+' .CodeMirror').css('border-top', '2px solid #b43232');
            $('#'+ed.parentDiv+' .CodeMirror').css('border-bottom', '2px solid #b43232');
        }
        ed.acEditEvent = true;
    }
}

cm_editors = {}

function pyStr(x) {
    if (x instanceof Array ) {
        return '[' + x.join(", ") + ']';
    } else {
        return x
    }
}

function outf(text) {
    var mypre = document.getElementById(Sk.pre);
    // bnm python 3
    x = text;
    if (x.charAt(0) == '(') {
        x = x.slice(1,-1);
    x = '['+x+']'
    try {
        var xl = eval(x);
        xl = xl.map(pyStr);
        x = xl.join(' ');
    } catch(err) {
        }
    }
    text = x;
    text = text.replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, "<br/>");
    mypre.innerHTML = mypre.innerHTML + text;
}

function createEditors() {
    var edList = new Array();
    edList = document.getElementsByClassName("active_code");
    for (var i = 0; i < edList.length; i++) {
        newEdId = edList[i].id;
        cm_editors[newEdId] = CodeMirror.fromTextArea(edList[i], {
            mode: {name: "python",
                version: 2,
                singleLineStringErrors: false},
            lineNumbers: true,
            indentUnit: 4,
            indentWithTabs: false,
            matchBrackets: true,
            extraKeys: {"Tab":"indentMore", "Shift-Tab": "indentLess"},
            onKeyEvent:handleEdKeys
        }
                );
        cm_editors[newEdId].parentDiv = edList[i].parentNode.id;
        //requestCode(edList[i].parentNode.id) // populate with user's code
    }

}

function builtinRead(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
        throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
}

function runit(myDiv,theButton,includes) {
    //var prog = document.getElementById(myDiv + "_code").value;

    $(theButton).attr('disabled','disabled');
    Sk.isTurtleProgram = false;
    if (theButton !== undefined) {
        Sk.runButton = theButton;
    }
    $("#"+myDiv+"_errinfo").remove()
    var editor = cm_editors[myDiv+"_code"];
    if (editor.acEditEvent) {
        logBookEvent({'event':'activecode','act': 'edit', 'div_id':myDiv}); // Log the edit event
        editor.acEditEvent = false;
    }
    var prog = "";
    var text = "";
    if (includes !== undefined ) {
        // iterate over the includes, in-order prepending to prog
        for (var x in includes) {
            text = cm_editors[includes[x] + "_code"].getValue();
            prog = prog + text + "\n"
        }
    }
    prog = prog + editor.getValue();
    var mypre = document.getElementById(myDiv + "_pre");
    if (mypre) mypre.innerHTML = '';
    Sk.canvas = myDiv + "_canvas";
    Sk.pre = myDiv + "_pre";
    var can = document.getElementById(Sk.canvas);
    // The following lines reset the canvas so that each time the run button
    // is pressed the turtle(s) get a clean canvas.
    if (can) {
        can.width = can.width;
        if (Sk.tg) {
            Sk.tg.canvasInit = false;
            Sk.tg.turtleList = [];
        }
    }
    // set execLimit in milliseconds  -- for student projects set this to
    // 25 seconds -- just less than Chrome's own timer.
    Sk.execLimit = 25000;
    // configure Skulpt output function, and module reader
    Sk.configure({output:outf,
                read: builtinRead
            });
    try {
        Sk.importMainWithBody("<stdin>", false, prog);
        logRunEvent({'div_id':myDiv, 'code':prog, 'errinfo':'success'}); // Log the run event
    } catch (e) {
        logRunEvent({'div_id':myDiv, 'code':prog, 'errinfo':e.toString()}); // Log the run event
        //alert(e);
    addErrorMessage(e,myDiv)
    }
    if (! Sk.isTurtleProgram ) {
        $(theButton).removeAttr('disabled');
    }
    if (typeof(allVisualizers) != "undefined") {
        $.each(allVisualizers, function(i, e) {
            e.redrawConnectors();
          });
    }
}

function addErrorMessage(err, myDiv) {
    var errHead = $('<h3>').html('Error')
    var divEl = document.getElementById(myDiv)
    var eContainer = divEl.appendChild(document.createElement('div'))
    eContainer.className = 'error'
    eContainer.id = myDiv + '_errinfo'
    eContainer.appendChild(errHead[0])
    var errText = eContainer.appendChild(document.createElement('pre'))
    var errString = err.toString()
    errText.innerHTML = errString
    var to = errString.indexOf(":")
    var errName = errString.substring(0,to)
    $(eContainer).append('<h3>Description</h3>')
    var errDesc = eContainer.appendChild(document.createElement('p'))
    errDesc.innerHTML = errorText[errName]
    $(eContainer).append('<h3>To Fix</h3>')
    var errFix = eContainer.appendChild(document.createElement('p'))
    errFix.innerHTML = errorText[errName+'Fix']
    var moreInfo = '../ErrorHelp/'+errName.toLowerCase()+'.html'
}

var errorText = {}

errorText.ParseError = "A parse error means that Python does not understand the syntax on the line the error message points out.  Common examples are forgetting commas beteween arguments or forgetting a : on a for statement"
errorText.ParseErrorFix = "To fix a parse error you just need to look carefully at the line with the error and possibly the line before it.  Make sure it conforms to all of Python's rules."
errorText.TypeError = "Type errors most often occur when an expression tries to combine two objects with types that should not be combined.  Like raising a string to a power"
errorText.TypeErrorFix = "To fix a type error you will most likely need to trace through your code and make sure the variables have the types you expect them to have.  It may be helpful to print out each variable along the way to be sure its value is what you think it should be."
errorText.NameError = "A name error almost always means that you have used a variable before it has a value.  Often this may be a simple typo, so check the spelling carefully."
errorText.NameErrorFix = "Check the right hand side of assignment statements and your function calls, this is the most likely place for a NameError to be found."
errorText.ValueError = "A ValueError most often occurs when you pass a parameter to a function and the function is expecting one type and you pass another."
errorText.ValueErrorFix = "The error message gives you a pretty good hint about the name of the function as well as the value that is incorrect.  Look at the error message closely and then trace back to the variable containing the problematic value."
errorText.AttributeError = "This error message is telling you that the object on the left hand side of the dot, does not have the attribute or method on the right hand side."
errorText.AttributeErrorFix = "The most common variant of this message is that the object undefined does not have attribute X.  This tells you that the object on the left hand side of the dot is not what you think. Trace the variable back and print it out in various places until you discover where it becomes undefined.  Otherwise check the attribute on the right hand side of the dot for a typo."
errorText.TokenError= "Most of the time this error indicates that you have forgotten a right parenthesis or have forgotten to close a pair of quotes."
errorText.TokenErrorFix= "Check each line of your program and make sure that your parenthesis are balanced."
errorText.TimeLimitError = "Your program is running too long.  Most programs in this book should run in less than 10 seconds easily. This probably indicates your program is in an infinite loop."
errorText.TimeLimitErrorFix = "Add some print statements to figure out if your program is in an infinte loop.  If it is not you can increase the run time with sys.setExecutionLimit(msecs)"
errorText.Error = "Your program is running for too long.  Most programs in this book should run in less than 30 seconds easily. This probably indicates your program is in an infinite loop."
errorText.ErrorFix = "Add some print statements to figure out if your program is in an infinte loop.  If it is not you can increase the run time with sys.setExecutionLimit(msecs)"
errorText.SyntaxError = "This message indicates that Python can't figure out the syntax of a particular statement.  Some examples are assigning to a literal, or a function call"
errorText.SyntaxErrorFix = "Check your assignment statments and make sure that the left hand side of the assignment is a variable, not a literal or a function."
errorText.IndexError = "This message means that you are trying to index past the end of a string or a list.  For example if your list has 3 things in it and you try to access the item at position 3 or more."
errorText.IndexErrorFix = "Remember that the first item in a list or string is at index position 0, quite often this message comes about because you are off by one.  Remember in a list of length 3 the last legal index is 2"
errorText.URIError = ""
errorText.URIErrorFix = ""
errorText.ImportError = "This error message indicates that you are trying to import a module that does not exist"
errorText.ImportErrorFix = "One problem may simply be that you have a typo.  It may also be that you are trying to import a module that exists in 'real' Python, but does not exist in this book.  If this is the case, please submit a feature request to have the module added."
errorText.ReferenceError = "This is most likely an internal error, particularly if the message references the console."
errorText.ReferenceErrorFix = "Try refreshing the webpage, and if the error continues, submit a bug report along with your code"
errorText.ZeroDivisionError = "This tells you that you are trying to divide by 0. Typically this is because the value of the variable in the denominator of a division expression has the value 0"
errorText.ZeroDivisionErrorFix = "You may need to protect against dividing by 0 with an if statment, or you may need to rexamine your assumptions about the legal values of variables, it could be an earlier statment that is unexpectedly assigning a value of zero to the variable in question."
errorText.RangeError = "This message almost always shows up in the form of Maximum call stack size exceeded."
errorText.RangeErrorFix = "This always occurs when a function calls itself.  Its pretty likely that you are not doing this on purpose. Except in the chapter on recursion.  If you are in that chapter then its likely you haven't identified a good base case."
errorText.InternalError = "An Internal error may mean that you've triggered a bug in our Python"
errorText.InternalErrorFix = "Report this error, along with your code as a bug."
errorText.IndentationError = "This error occurs when you have not indented your code properly.  This is most likely to happen as part of an if, for, while or def statement."
errorText.IndentationErrorFix = "Check your if, def, for, and while statements to be sure the lines are properly indented beneath them.  Another source of this error comes from copying and pasting code where you have accidentally left some bits of code lying around that don't belong there anymore."

function logBookEvent(eventInfo) {
    eventInfo.course = eBookConfig.course
    if (eBookConfig.logLevel > 0){
       jQuery.get(eBookConfig.ajaxURL+'hsblog',eventInfo); // Log the run event
    }
}

function logRunEvent(eventInfo) {
    eventInfo.course = eBookConfig.course
    if (eBookConfig.logLevel > 0){
       jQuery.post(eBookConfig.ajaxURL+'runlog',eventInfo); // Log the run event
    }
}

function saveSuccess(data,status,whatever) {
    if (data.redirect) {
        alert("Did not save!  It appears you are not logged in properly")
    } else if (data == "") {
        alert("Error:  Program not saved");
    }
    else {
        var acid = eval(data)[0];
        if (acid.indexOf("ERROR:") == 0) {
            alert(acid);
        } else {
            $('#'+acid+' .CodeMirror').css('border-top', '2px solid #aaa');
            $('#'+acid+' .CodeMirror').css('border-bottom', '2px solid #aaa');
        }
    }
}

function saveEditor(divName) {
    // get editor from div name
    var editor = cm_editors[divName+"_code"];
    var data = {acid:divName, code:editor.getValue()};
    $(document).ajaxError(function(e,jqhxr,settings,exception){alert("Request Failed for"+settings.url)});
    jQuery.post(eBookConfig.ajaxURL+'saveprog',data,saveSuccess);
    if (editor.acEditEvent) {
        logBookEvent({'event':'activecode','act': 'edit', 'div_id':divName}); // Log the run event
        editor.acEditEvent = false;
    }
    logBookEvent({'event':'activecode' ,'act':'save', 'div_id':divName}); // Log the run event

}

function requestCode(divName,sid) {
    var editor = cm_editors[divName+"_code"];


    var data = {acid: divName}
    if (sid !== undefined) {
        data['sid'] = sid;
    }
    logBookEvent({'event':'activecode', 'act':'load', 'div_id':divName}); // Log the run event
    jQuery.get(eBookConfig.ajaxURL+'getprog',data, loadEditor);
}

function loadEditor(data, status, whatever) {
    // function called when contents of database are returned successfully
    var res = eval(data)[0];
    var editor;
    if (res.sid) {
        editor = cm_editors[res.acid+"_"+res.sid+"_code"];
    } else {
        editor = cm_editors[res.acid+"_code"];
    }

    if (res.source) {
        editor.setValue(res.source);
    }
    // need to get the divId back with the result...
}

function createActiveCode(divid,suppliedSource,sid) {
    var eNode;
    var acblockid;
    if (sid !== undefined) {
        acblockid = divid + "_" + sid;
    } else {
        acblockid = divid;
    }

    edNode = document.getElementById(acblockid);
    if (edNode.children.length == 0 ) {
    //edNode.style.display = 'none';
    edNode.style.backgroundColor = "white";
    var editor;
    editor = CodeMirror(edNode, {
                mode: {name: "python",
                    version: 2,
                    singleLineStringErrors: false},
                lineNumbers: true,
                indentUnit: 4,
                tabMode: "indent",
                matchBrackets: true,
                onKeyEvent:handleEdKeys
            });


    var myRun = function() {
        runit(acblockid);
    }
    var mySave = function() {
        saveEditor(divid);
    }
    var myLoad = function() {
        requestCode(divid,sid);
    }
    cm_editors[acblockid+"_code"] = editor;
    editor.parentDiv = acblockid;
    var runButton = document.createElement("input");
    runButton.setAttribute('type','button');
    runButton.setAttribute('value','run');
    runButton.onclick = myRun;
    edNode.appendChild(runButton);
    if (sid === undefined) { // We don't need load and save buttons for grading
        if(isLoggedIn() == true) {
            var saveButton = document.createElement("input");
            saveButton.setAttribute('type','button');
            saveButton.setAttribute('value','save');
            saveButton.onclick = mySave;
            edNode.appendChild(saveButton);

            var loadButton = document.createElement("input");
            loadButton.setAttribute('type','button');
            loadButton.setAttribute('value','load');
            loadButton.onclick = myLoad;
            edNode.appendChild(loadButton);
        }
    }
    edNode.appendChild(document.createElement('br'));
    var newCanvas = edNode.appendChild(document.createElement("canvas"));
    newCanvas.id = acblockid+"_canvas";
    newCanvas.height = 400;
    newCanvas.width = 400;
    newCanvas.style.border = '2px solid black';
    newCanvas.style.display = 'none';
    var newPre = edNode.appendChild(document.createElement("pre"));
    newPre.id = acblockid + "_pre";
    newPre.className = "active_out";

    myLoad();
    if (! suppliedSource ) {
        suppliedSource = '\n\n\n\n\n';
    }
    if (! editor.getValue()) {
        suppliedSource = suppliedSource.replace(new RegExp('%22','g'),'"');
        suppliedSource = suppliedSource.replace(new RegExp('%27','g'),"'");
        editor.setValue(suppliedSource);
    }
}
   // $('#'+divid).modal({minHeight:700, minWidth: 410, maxWidth:450, containerCss:{width:420, height:750}});
}


function comment(blockid) {
    $.modal('<iframe width="600" height="400" src="/getcomment?id='+blockid+'" style="background-color: white">', {
    //$.modal('<form><textarea name="content"></textarea><input type="submit" name="submit" > </form>', {
    overlayClose: true,
    closeHTML:"",
    containerCss:{
        width:600,
        height:400,
        backgroundColor: "#fff"
    }
            });
}

function sendGrade(grade,sid,acid,id) {
    data = {'sid':sid, 'acid':acid, 'grade':grade, 'id':id};
    jQuery.get(eBookConfig.ajaxURL+'savegrade',data);
}

function gotUser(data, status, whatever) {
    var mess = '';
    var caughtErr = false;
    var d;
    try {
        d = eval(data)[0];
    } catch (err) {
        if (eBookConfig.loginRequired) {
            if (confirm("Error: " + err.toString() + "Please report this error!  Click OK to continue without logging in.  Cancel to retry.")) {
                caughtErr = true;
                mess = "Not logged in";
	            $('button.ac_opt').hide();
	            $('span.loginout').html('<a href="' + eBookConfig.app + '/default/user/login">login</a>')
            } else {
                window.location.href = eBookConfig.app + '/default/user/login?_next=' + window.location.href
            }
        }
    }
    if (d.redirect) {
        if (eBookConfig.loginRequired) {
            window.location.href = eBookConfig.app + '/default/user/login?_next=' + window.location.href
        } else {
            mess = "Not logged in";
            $('button.ac_opt').hide();
            $('span.loginout').html('<a href="' + eBookConfig.app + '/default/user/login">login</a>')
        }
    } else {
        if (!caughtErr) {
            mess = d.email;
            eBookConfig.isLoggedIn = true;
			enableUserHighlights();
            timedRefresh();
        }
    }
    x = $(".footer").text();
    $(".footer").text(x + mess);
    logBookEvent({
        'event': 'page',
        'act': 'view',
        'div_id': window.location.pathname
    })
}


function timedRefresh() {
    timeoutPeriod = 4500000;  // 75 minutes
    $(document).bind("idle.idleTimer",function(){
        // After timeout period send the user back to the index.  This will force a login
        // if needed when they want to go to a particular page.  This may not be perfect
        // but its an easy way to make sure laptop users are properly logged in when they
        // take quizzes and save stuff.
        if (location.href.indexOf('index.html') < 0)
            location.href = eBookConfig.app+'/static/'+eBookConfig.course + '/index.html'
    });
    $.idleTimer(timeoutPeriod);
}

function shouldLogin() {
    var sli = true;

    if (window.location.href.indexOf('file://') > -1)
        sli = false

    return sli;
}

function isLoggedIn() {
    if (typeof eBookConfig.isLoggedIn !== undefined ){
        return eBookConfig.isLoggedIn;
    }
    return false;
}

function addUserToFooter() {
    // test to see if online before doing this.
    if (shouldLogin()) {
        jQuery.get(eBookConfig.ajaxURL+'getuser',null,gotUser)
    } else {
        x = $(".footer").text();
        $(".footer").text(x + 'not logged in');
        $('button.ac_opt').hide();
        $('span.loginout').html('<a href="'+ eBookConfig.app+'/default/user/login">login</a>')
        logBookEvent({'event':'page', 'act':'view', 'div_id':window.location.pathname})
    }


}

/*
Since I don't want to modify the codelens code I'll attach the logging functionality this way.
This actually seems like a better way to do it maybe across the board to separate logging
from the real funcionality.  It would also allow a better way of turning off/on logging..
As long as Philip doesn't go and change the id values for the buttons and slider this will
continue to work.... In the best of all worlds we might add a function to the visualizer to
return the buttons, but I'm having a hard time thinking of any other use for that besides mine.
*/
function attachLoggers(codelens,divid) {
    codelens.domRoot.find("#jmpFirstInstr").click(function() {
        logBookEvent({'event':'codelens', 'act': 'first', 'div_id':divid});
    });
    codelens.domRoot.find("#jmpLastInstr").click(function() {
        logBookEvent({'event':'codelens', 'act': 'last', 'div_id':divid});
    });
    codelens.domRoot.find("#jmpStepBack").click(function() {
        logBookEvent({'event':'codelens', 'act': 'back', 'div_id':divid});
    });
    codelens.domRoot.find("#jmpStepFwd").click(function() {
        logBookEvent({'event':'codelens', 'act': 'fwd', 'div_id':divid});
    });
    codelens.domRoot.find("#executionSlider").bind('slide',function(evt,ui) {
        logBookEvent({'event':'codelens', 'act': 'slide', 'div_id':divid});
    });

}

function redrawAllVisualizerArrows() {
    if (allVisualizers !== undefined) {
	for(var v in allVisualizers)
	    allVisualizers[v].redrawConnectors();
    }
}

function getNumUsers() {
    $.getJSON(eBookConfig.ajaxURL+'getnumusers',setNumUsers)
}

function getOnlineUsers() {
    $.getJSON(eBookConfig.ajaxURL+'getnumonline',setOnlineUsers)
}

function setOnlineUsers(data) {
    var d = data[0]
    $("#numuserspan").text(d.online);
}

function setNumUsers(data) {
    var d = data[0]
    $("#totalusers").text(d.numusers);
}
