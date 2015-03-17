/**
 * Created by bmiller on 3/13/15.
 */
var Jobe = new (function() {
//var API_KEY = '2AAA7A5415B4A9B394B54BF1D2E9D';  //# A working (100/hr) key on Jobe2
    var API_KEY = "67033pV7eUUvqo07OJDIV8UZ049aLEK1"
    var USE_API_KEY = true;
    var JOBE_SERVER = 'http://jobe2.cosc.canterbury.ac.nz';
    var resource = '/jobe/index.php/restapi/runs/';
    var div2id = {}

// todo:  set up a request to push a data file to the server

    var runlive = function (divid, language, sourcefile, datafile) {
        var xhr, stdin;
        var runspec = {};
        var data, host, source, editor;
        var sfilemap = {java: '', cpp: 'test.cpp', c: 'test.c', python3: 'test.py', python2: 'test.py'}

        xhr = new XMLHttpRequest();
        editor = cm_editors[divid + "_code"];
        source = editor.getValue();

        stdin = $("#" + divid + "_stdin").val()

        if (! sourcefile ) {
            sourcefile = sfilemap[language];
        }

        runspec = {
            language_id: language,
            sourcecode: source,
            sourcefilename: sourcefile
        };


        if (stdin) {
            runspec.input = stdin
        }

        if (datafile !== "False") {
            runspec['file_list'] = [[div2id[datafile],datafile]];
        }
        data = JSON.stringify({'run_spec': runspec});
        host = JOBE_SERVER + resource
        xhr.open("POST", host, true);
        xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.setRequestHeader('X-API-KEY', API_KEY);

        xhr.onload = function () {
            var logresult;
            try {
                var result = JSON.parse(xhr.responseText);
            } catch (e) {
                result = {};
                result.outcome = -1;
            }
            var odiv = "#" + divid + "_pre";
            if (result.outcome === 15) {
                logresult = 'success';
            } else {
                logresult = result.outcome;
            }
            logRunEvent({'div_id': divid, 'code': source, 'errinfo': logresult, 'event':'livecode'});
            switch (result.outcome) {
                case 15:
                    $(odiv).html(result.stdout.replace(/\n/g, "<br>"));
                    break;
                case 11: // compiler error
                    $(odiv).html("There were errors compiling your code. See below.");
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
                    if(result.stderr) {
                        $(odiv).html(result.stderr.replace(/\n/g, "<br>"));
                    } else {
                        addJobeErrorMessage("A server error occurred: " + xhr.status + " " + xhr.statusText);
                    }
            }

            // todo: handle server busy and timeout errors too
        };

        $("#" + divid + "_errinfo").remove();
        $("#" + divid + "_pre").html("Compiling and Running your Code Now...")

        xhr.onerror = function () {
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


    function pushDataFile(datadiv) {

        var file_id = 'runestone'+Math.floor(Math.random()*100000);
        var contents = $(document.getElementById(datadiv)).text();
        var contentsb64 = btoa(contents);
        var data = JSON.stringify({ 'file_contents' : contentsb64 });
        var resource = '/jobe/index.php/restapi/files/' + file_id
        var host = JOBE_SERVER + resource
        var xhr = new XMLHttpRequest();

        if (div2id[datadiv] === undefined ) {
            div2id[datadiv] = file_id;

            xhr.open("PUT", host, true);
            xhr.setRequestHeader('Content-type', 'application/json');
            xhr.setRequestHeader('Accept', 'text/plain');
            xhr.setRequestHeader('X-API-KEY', API_KEY);

            xhr.onload = function () {
                console.log("successfully sent file " + xhr.responseText);
            }

            xhr.onerror = function () {
                console.log("error sending file" + xhr.responseText);
            }

            xhr.send(data)
        }
    }

    return {
        runlive : runlive,
        pushDataFile : pushDataFile
    };

})();
