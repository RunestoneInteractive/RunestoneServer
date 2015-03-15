/**
 * Created by bmiller on 3/13/15.
 */

//var API_KEY = '2AAA7A5415B4A9B394B54BF1D2E9D';  //# A working (100/hr) key on Jobe2
var API_KEY = "67033pV7eUUvqo07OJDIV8UZ049aLEK1"
var USE_API_KEY = true;
var JOBE_SERVER = 'http://jobe2.cosc.canterbury.ac.nz';
var resource = '/jobe/index.php/restapi/runs/';

function runlive (divid, language) {
    var xhr, stdin;
    var runspec = {};
    var data, host, source, editor;
    var sfilemap = { java: 'test.java', cpp : 'test.cpp', c : 'test.c', python3: 'test.py', python2: 'test.py'}
    xhr = new XMLHttpRequest();
    editor = cm_editors[divid + "_code"];
    source = editor.getValue();

    stdin = $("#" + divid + "_stdin").val()

    runspec = {
        language_id: language,
        sourcecode: source,
        sourcefilename: sfilemap[language]
    };

    if (stdin) {
        runspec.input = stdin
    }
    data = JSON.stringify({'run_spec': runspec});
    host = JOBE_SERVER + resource
    xhr.open("POST", host, true);
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.setRequestHeader('X-API-KEY', API_KEY);

    xhr.onload = function () {
        var result = JSON.parse(xhr.responseText);
        var odiv = "#" + divid + "_pre";
        switch (result.outcome) {
            case 15:
                $(odiv).html(result.stdout.replace(/\n/g, "<br>"));
                break;
            case 11: // compiler error
                addJobeErrorMessage(result.cmpinfo, divid);
                break;
            case 12:  // run time error
                $(odiv).html(result.stdout.replace(/\n/g, "<br>"));
                if (result.stderr) {
                    addJobeErrorMessage(result.stderr, divid);
                }
                break;
            case 13:  // time limit
                $(odiv).html(result.stdout.replace(/\n/g, "<br>"));
                addJobeErrorMessage("Time Limit Exceeded on your program", divid);
                break;
            default:
                $(odiv).html(result.stderr.replace(/\n/g, "<br>"));
        }

        // todo: handle server busy and timeout errors too
    };

    $("#" + divid + "_errinfo").remove();
    $("#" + divid + "_pre").html("Compiling and Running your Code Now...")

    xhr.onerror = function() {
        addJobeErrorMessage("Error communicating with the server.", divid);
    };

    xhr.send(data);
};

function addJobeErrorMessage(err, myDiv) {
    var errHead = $('<h3>').html('Error')
    var divEl = document.getElementById(myDiv)
    var eContainer = divEl.appendChild(document.createElement('div'))
    eContainer.className = 'error alert alert-danger';
    eContainer.id = myDiv + '_errinfo';
    eContainer.appendChild(errHead[0]);
    var errText = eContainer.appendChild(document.createElement('pre'))
    errText.innerHTML = err;
}
// add onload event to attache run to all buttons?