/*

Online Python Tutor
https://github.com/pgbovine/OnlinePythonTutor/

Copyright (C) 2010-2013 Philip J. Guo (philip@pgbovine.net)

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*/


// Pre-reqs: pytutor.js and jquery.ba-bbq.min.js should be imported BEFORE this file


// backend scripts to execute (Python 2 and 3 variants, if available)
// make two copies of ../web_exec.py and give them the following names,
// then change the first line (starting with #!) to the proper version
// of the Python interpreter (i.e., Python 2 or Python 3).
// Note that your hosting provider might have stringent rules for what
// kind of scripts are allowed to execute. For instance, my provider
// (Webfaction) seems to let scripts execute only if permissions are
// something like:
// -rwxr-xr-x 1 pgbovine pgbovine 2.5K Jul  5 22:46 web_exec_py2.py*
// (most notably, only the owner of the file should have write
//  permissions)
//var python2_backend_script = 'web_exec_py2.py';
//var python3_backend_script = 'web_exec_py3.py';

// uncomment below if you're running on Google App Engine using the built-in app.yaml
var python2_backend_script = 'exec';
var python3_backend_script = null;

// KRAZY experimental KODE!!! Use a custom hacked CPython interpreter
var python2crazy_backend_script = 'web_exec_py2-crazy.py';
// On Google App Engine, simply run dev_appserver.py with the
// crazy custom CPython interpreter to get 2crazy
//var python2crazy_backend_script = 'exec';

var appMode = 'edit'; // 'edit', 'display', or 'display_no_frills'

var preseededCode = null;     // if you passed in a 'code=<code string>' in the URL, then set this var
var preseededCurInstr = null; // if you passed in a 'curInstr=<number>' in the URL, then set this var

var rawInputLst = []; // a list of strings inputted by the user in response to raw_input or mouse_input events

var myVisualizer = null; // singleton ExecutionVisualizer instance


function enterEditMode() {
  $.bbq.pushState({ mode: 'edit' }, 2 /* completely override other hash strings to keep URL clean */);
}

function enterDisplayNoFrillsMode() {
  $.bbq.pushState({ mode: 'display_no_frills' }, 2 /* completely override other hash strings to keep URL clean */);
}

var pyInputCodeMirror; // CodeMirror object that contains the input text

function setCodeMirrorVal(dat) {
  pyInputCodeMirror.setValue(dat.rtrim() /* kill trailing spaces */);
  $('#urlOutput,#embedCodeOutput').val('');

  // also scroll to top to make the UI more usable on smaller monitors
  $(document).scrollTop(0);
}


$(document).ready(function() {

  $("#embedLinkDiv").hide();

  pyInputCodeMirror = CodeMirror(document.getElementById('codeInputPane'), {
    mode: 'python',
    lineNumbers: true,
    tabSize: 4,
    indentUnit: 4,
    // convert tab into four spaces:
    extraKeys: {Tab: function(cm) {cm.replaceSelection("    ", "end");}}
  });

  pyInputCodeMirror.setSize(null, '420px');



  // be friendly to the browser's forward and back buttons
  // thanks to http://benalman.com/projects/jquery-bbq-plugin/
  $(window).bind("hashchange", function(e) {
    appMode = $.bbq.getState('mode'); // assign this to the GLOBAL appMode

    if (appMode === undefined || appMode == 'edit') {
      $("#pyInputPane").show();
      $("#pyOutputPane").hide();
      $("#embedLinkDiv").hide();

      // destroy all annotation bubbles (NB: kludgy)
      if (myVisualizer) {
        myVisualizer.destroyAllAnnotationBubbles();
      }
    }
    else if (appMode == 'display') {
      $("#pyInputPane").hide();
      $("#pyOutputPane").show();

      $("#embedLinkDiv").show();

      $('#executeBtn').html("Visualize execution");
      $('#executeBtn').attr('disabled', false);


      // do this AFTER making #pyOutputPane visible, or else
      // jsPlumb connectors won't render properly
      myVisualizer.updateOutput();

      // customize edit button click functionality AFTER rendering (NB: awkward!)
      $('#pyOutputPane #editCodeLinkDiv').show();
      $('#pyOutputPane #editBtn').click(function() {
        enterEditMode();
      });
    }
    else if (appMode == 'display_no_frills') {
      $("#pyInputPane").hide();
      $("#pyOutputPane").show();
      $("#embedLinkDiv").show();
    }
    else {
      assert(false);
    }

    $('#urlOutput,#embedCodeOutput').val(''); // clear to avoid stale values
  });


  function executeCode(forceStartingInstr) {
      var backend_script = null;
      if ($('#pythonVersionSelector').val() == '2') {
          backend_script = python2_backend_script;
      }
      else if ($('#pythonVersionSelector').val() == '3') {
          backend_script = python3_backend_script;
      }
      // experimental KRAZY MODE!!!
      else if ($('#pythonVersionSelector').val() == '2crazy') {
          backend_script = python2crazy_backend_script;
      }

      if (!backend_script) {
        alert('Error: This server is not configured to run Python ' + $('#pythonVersionSelector').val());
        return;
      }

      $('#executeBtn').html("Please wait ... processing your code");
      $('#executeBtn').attr('disabled', true);
      $("#pyOutputPane").hide();
      $("#embedLinkDiv").hide();


      // set up all options in a JS object
      var options = {cumulative_mode: ($('#cumulativeModeSelector').val() == 'true'),
                     heap_primitives: ($('#heapPrimitivesSelector').val() == 'true'),
                     show_only_outputs: ($('#showOnlyOutputsSelector').val() == 'true'),
                     py_crazy_mode: ($('#pythonVersionSelector').val() == '2crazy')};

      $.get(backend_script,
            {user_script : pyInputCodeMirror.getValue(),
             raw_input_json: rawInputLst.length > 0 ? JSON.stringify(rawInputLst) : '',
             options_json: JSON.stringify(options)},
            function(dataFromBackend) {
              var trace = dataFromBackend.trace;

              // don't enter visualize mode if there are killer errors:
              if (!trace ||
                  (trace.length == 0) ||
                  (trace[trace.length - 1].event == 'uncaught_exception')) {

                if (trace.length == 1) {
                  var errorLineNo = trace[0].line - 1; /* CodeMirror lines are zero-indexed */
                  if (errorLineNo !== undefined) {
                    // highlight the faulting line in pyInputCodeMirror
                    pyInputCodeMirror.focus();
                    pyInputCodeMirror.setCursor(errorLineNo, 0);
                    pyInputCodeMirror.setLineClass(errorLineNo, null, 'errorLine');

                    pyInputCodeMirror.setOption('onChange', function() {
                      pyInputCodeMirror.setLineClass(errorLineNo, null, null); // reset line back to normal
                      pyInputCodeMirror.setOption('onChange', null); // cancel
                    });
                  }

                  alert(trace[0].exception_msg);
                }
                else if (trace[trace.length - 1].exception_msg) {
                  alert(trace[trace.length - 1].exception_msg);
                }
                else {
                  alert("Whoa, unknown error! Reload to try again, or report a bug to philip@pgbovine.net\n\n(Click the 'Generate URL' button to include a unique URL in your email bug report.)");
                }

                $('#executeBtn').html("Visualize execution");
                $('#executeBtn').attr('disabled', false);
              }
              else {
                var startingInstruction = 0;

                // only do this at most ONCE, and then clear out preseededCurInstr
                if (preseededCurInstr && preseededCurInstr < trace.length) { // NOP anyways if preseededCurInstr is 0
                  startingInstruction = preseededCurInstr;
                  preseededCurInstr = null;
                }

                // forceStartingInstr overrides everything else
                if (forceStartingInstr !== undefined) {
                  startingInstruction = forceStartingInstr;
                }

                myVisualizer = new ExecutionVisualizer('pyOutputPane',
                                                       dataFromBackend,
                                                       {startingInstruction:  startingInstruction,
                                                        updateOutputCallback: function() {$('#urlOutput,#embedCodeOutput').val('');},
                                                        // tricky: selector 'true' and 'false' values are strings!
                                                        disableHeapNesting: ($('#heapPrimitivesSelector').val() == 'true'),
                                                        drawParentPointers: ($('#drawParentPointerSelector').val() == 'true'),
                                                        textualMemoryLabels: ($('#textualMemoryLabelsSelector').val() == 'true'),
                                                        showOnlyOutputs: ($('#showOnlyOutputsSelector').val() == 'true'),
                                                        executeCodeWithRawInputFunc: executeCodeWithRawInput,

                                                        // undocumented experimental modes:
                                                        pyCrazyMode: ($('#pythonVersionSelector').val() == '2crazy'),
                                                        //allowEditAnnotations: true,
                                                       });


                // set keyboard bindings
                // VERY IMPORTANT to clear and reset this every time or
                // else the handlers might be bound multiple times
                $(document).unbind('keydown');
                $(document).keydown(function(k) {
                  if (k.keyCode == 37) { // left arrow
                    if (myVisualizer.stepBack()) {
                      k.preventDefault(); // don't horizontally scroll the display
                    }
                  }
                  else if (k.keyCode == 39) { // right arrow
                    if (myVisualizer.stepForward()) {
                      k.preventDefault(); // don't horizontally scroll the display
                    }
                  }
                });

                // also scroll to top to make the UI more usable on smaller monitors
                $(document).scrollTop(0);

                $.bbq.pushState({ mode: 'display' }, 2 /* completely override other hash strings to keep URL clean */);
              }
            },
            "json");
  }

  function executeCodeFromScratch() {
    // reset these globals
    rawInputLst = [];

    executeCode();
  }

  function executeCodeWithRawInput(rawInputStr, curInstr) {
    enterDisplayNoFrillsMode();

    // set some globals
    rawInputLst.push(rawInputStr);

    executeCode(curInstr);
  }

  $("#executeBtn").attr('disabled', false);
  $("#executeBtn").click(executeCodeFromScratch);


  // canned examples

  $("#tutorialExampleLink").click(function() {
    $.get("example-code/py_tutorial.txt", setCodeMirrorVal);
    return false;
  });

  $("#strtokExampleLink").click(function() {
    $.get("example-code/strtok.txt", setCodeMirrorVal);
    return false;
  });

  $("#listCompLink").click(function() {
    $.get("example-code/list-comp.txt", setCodeMirrorVal);
    return false;
  });

  $("#fibonacciExampleLink").click(function() {
    $.get("example-code/fib.txt", setCodeMirrorVal);
    return false;
  });

  $("#memoFibExampleLink").click(function() {
    $.get("example-code/memo_fib.txt", setCodeMirrorVal);
    return false;
  });

  $("#factExampleLink").click(function() {
    $.get("example-code/fact.txt", setCodeMirrorVal);
    return false;
  });

  $("#filterExampleLink").click(function() {
    $.get("example-code/filter.txt", setCodeMirrorVal);
    return false;
  });

  $("#insSortExampleLink").click(function() {
    $.get("example-code/ins_sort.txt", setCodeMirrorVal);
    return false;
  });

  $("#aliasExampleLink").click(function() {
    $.get("example-code/aliasing.txt", setCodeMirrorVal);
    return false;
  });

  $("#happyExampleLink").click(function() {
    $.get("example-code/happy.txt", setCodeMirrorVal);
    return false;
  });

  $("#newtonExampleLink").click(function() {
    $.get("example-code/sqrt.txt", setCodeMirrorVal);
    return false;
  });

  $("#oopSmallExampleLink").click(function() {
    $.get("example-code/oop_small.txt", setCodeMirrorVal);
    return false;
  });

  $("#mapExampleLink").click(function() {
    $.get("example-code/map.txt", setCodeMirrorVal);
    return false;
  });

  $("#rawInputExampleLink").click(function() {
    $.get("example-code/raw_input.txt", setCodeMirrorVal);
    return false;
  });

  $("#oop1ExampleLink").click(function() {
    $.get("example-code/oop_1.txt", setCodeMirrorVal);
    return false;
  });

  $("#oop2ExampleLink").click(function() {
    $.get("example-code/oop_2.txt", setCodeMirrorVal);
    return false;
  });

  $("#inheritanceExampleLink").click(function() {
    $.get("example-code/oop_inherit.txt", setCodeMirrorVal);
    return false;
  });

  $("#sumExampleLink").click(function() {
    $.get("example-code/sum.txt", setCodeMirrorVal);
    return false;
  });

  $("#pwGcdLink").click(function() {
    $.get("example-code/wentworth_gcd.txt", setCodeMirrorVal);
    return false;
  });

  $("#pwSumListLink").click(function() {
    $.get("example-code/wentworth_sumList.txt", setCodeMirrorVal);
    return false;
  });

  $("#towersOfHanoiLink").click(function() {
    $.get("example-code/towers_of_hanoi.txt", setCodeMirrorVal);
    return false;
  });

  $("#pwTryFinallyLink").click(function() {
    $.get("example-code/wentworth_try_finally.txt", setCodeMirrorVal);
    return false;
  });

  $("#sumCubesLink").click(function() {
    $.get("example-code/sum-cubes.txt", setCodeMirrorVal);
    return false;
  });

  $("#decoratorsLink").click(function() {
    $.get("example-code/decorators.txt", setCodeMirrorVal);
    return false;
  });

  $("#genPrimesLink").click(function() {
    $.get("example-code/gen_primes.txt", setCodeMirrorVal);
    return false;
  });

  $("#genExprLink").click(function() {
    $.get("example-code/genexpr.txt", setCodeMirrorVal);
    return false;
  });


  $('#closure1Link').click(function() {
    $.get("example-code/closures/closure1.txt", setCodeMirrorVal);
    return false;
  });
  $('#closure2Link').click(function() {
    $.get("example-code/closures/closure2.txt", setCodeMirrorVal);
    return false;
  });
  $('#closure3Link').click(function() {
    $.get("example-code/closures/closure3.txt", setCodeMirrorVal);
    return false;
  });
  $('#closure4Link').click(function() {
    $.get("example-code/closures/closure4.txt", setCodeMirrorVal);
    return false;
  });
  $('#closure5Link').click(function() {
    $.get("example-code/closures/closure5.txt", setCodeMirrorVal);
    return false;
  });
  $('#lambdaParamLink').click(function() {
    $.get("example-code/closures/lambda-param.txt", setCodeMirrorVal);
    return false;
  });
  $('#tortureLink').click(function() {
    $.get("example-code/closures/student-torture.txt", setCodeMirrorVal);
    return false;
  });



  $('#aliasing1Link').click(function() {
    $.get("example-code/aliasing/aliasing1.txt", setCodeMirrorVal);
    return false;
  });
  $('#aliasing2Link').click(function() {
    $.get("example-code/aliasing/aliasing2.txt", setCodeMirrorVal);
    return false;
  });
  $('#aliasing3Link').click(function() {
    $.get("example-code/aliasing/aliasing3.txt", setCodeMirrorVal);
    return false;
  });
  $('#aliasing4Link').click(function() {
    $.get("example-code/aliasing/aliasing4.txt", setCodeMirrorVal);
    return false;
  });
  $('#aliasing5Link').click(function() {
    $.get("example-code/aliasing/aliasing5.txt", setCodeMirrorVal);
    return false;
  });
  $('#aliasing6Link').click(function() {
    $.get("example-code/aliasing/aliasing6.txt", setCodeMirrorVal);
    return false;
  });
  $('#aliasing7Link').click(function() {
    $.get("example-code/aliasing/aliasing7.txt", setCodeMirrorVal);
    return false;
  });
  $('#aliasing8Link').click(function() {
    $.get("example-code/aliasing/aliasing8.txt", setCodeMirrorVal);
    return false;
  });


  $('#ll1Link').click(function() {
    $.get("example-code/linked-lists/ll1.txt", setCodeMirrorVal);
    return false;
  });
  $('#ll2Link').click(function() {
    $.get("example-code/linked-lists/ll2.txt", setCodeMirrorVal);
    return false;
  });
  $('#sumListLink').click(function() {
    $.get("example-code/sum-list.txt", setCodeMirrorVal);
    return false;
  });

  $('#varargsLink').click(function() {
    $.get("example-code/varargs.txt", setCodeMirrorVal);
    return false;
  });

  $('#forElseLink').click(function() {
    $.get("example-code/for-else.txt", setCodeMirrorVal);
    return false;
  });

  $('#nonlocalLink').click(function() {
    $.get("example-code/nonlocal.txt", setCodeMirrorVal);
    return false;
  });


  // handle hash parameters passed in when loading the page
  preseededCode = $.bbq.getState('code');
  if (preseededCode) {
    setCodeMirrorVal(preseededCode);
  }
  else {
    // select a canned example on start-up:
    $("#aliasExampleLink").trigger('click');
  }

  // parse query string options ...
  // ugh, ugly tristate due to the possibility of them being undefined
  var cumulativeState = $.bbq.getState('cumulative');
  if (cumulativeState !== undefined) {
    $('#cumulativeModeSelector').val(cumulativeState);
  }
  var heapPrimitivesState = $.bbq.getState('heapPrimitives');
  if (heapPrimitivesState !== undefined) {
    $('#heapPrimitivesSelector').val(heapPrimitivesState);
  }
  var drawParentPointerState = $.bbq.getState('drawParentPointers');
  if (drawParentPointerState !== undefined) {
    $('#drawParentPointerSelector').val(drawParentPointerState);
  }
  var textRefsState = $.bbq.getState('textReferences');
  if (textRefsState !== undefined) {
    $('#textualMemoryLabelsSelector').val(textRefsState);
  }
  var showOnlyOutputsState = $.bbq.getState('showOnlyOutputs');
  if (showOnlyOutputsState !== undefined) {
    $('#showOnlyOutputsSelector').val(showOnlyOutputsState);
  }

  var pyState = $.bbq.getState('py');
  if (pyState !== undefined) {
    $('#pythonVersionSelector').val(pyState);
  }

  appMode = $.bbq.getState('mode'); // assign this to the GLOBAL appMode
  if ((appMode == "display") && preseededCode /* jump to display only with pre-seeded code */) {
    preseededCurInstr = Number($.bbq.getState('curInstr'));
    $("#executeBtn").trigger('click');
  }
  else {
    if (appMode === undefined) {
      // default mode is 'edit', don't trigger a "hashchange" event
      appMode = 'edit';
    }
    else {
      // fail-soft by killing all passed-in hashes and triggering a "hashchange"
      // event, which will then go to 'edit' mode
      $.bbq.removeState();
    }
  }


  // log a generic AJAX error handler
  $(document).ajaxError(function() {
    alert("Server error (possibly due to memory/resource overload). Report a bug to philip@pgbovine.net\n\n(Click the 'Generate URL' button to include a unique URL in your email bug report.)");

    $('#executeBtn').html("Visualize execution");
    $('#executeBtn').attr('disabled', false);
  });


  // redraw connector arrows on window resize
  $(window).resize(function() {
    if (appMode == 'display') {
      myVisualizer.redrawConnectors();
    }
  });

  $('#genUrlBtn').bind('click', function() {
    var myArgs = {code: pyInputCodeMirror.getValue(),
                  mode: appMode,
                  cumulative: $('#cumulativeModeSelector').val(),
                  heapPrimitives: $('#heapPrimitivesSelector').val(),
                  drawParentPointers: $('#drawParentPointerSelector').val(),
                  textReferences: $('#textualMemoryLabelsSelector').val(),
                  showOnlyOutputs: $('#showOnlyOutputsSelector').val(),
                  py: $('#pythonVersionSelector').val()};

    if (appMode == 'display') {
      myArgs.curInstr = myVisualizer.curInstr;
    }

    var urlStr = $.param.fragment(window.location.href, myArgs, 2 /* clobber all */);
    $('#urlOutput').val(urlStr);
  });


  $('#genEmbedBtn').bind('click', function() {
    assert(appMode == 'display');
    var myArgs = {code: pyInputCodeMirror.getValue(),
                  cumulative: $('#cumulativeModeSelector').val(),
                  heapPrimitives: $('#heapPrimitivesSelector').val(),
                  drawParentPointers: $('#drawParentPointerSelector').val(),
                  textReferences: $('#textualMemoryLabelsSelector').val(),
                  showOnlyOutputs: $('#showOnlyOutputsSelector').val(),
                  py: $('#pythonVersionSelector').val(),
                  curInstr: myVisualizer.curInstr,
                 };

    var embedUrlStr = $.param.fragment('http://pythontutor.com/iframe-embed.html', myArgs, 2 /* clobber all */);
    var iframeStr = '<iframe width="800" height="500" frameborder="0" src="' + embedUrlStr + '"> </iframe>';
    $('#embedCodeOutput').val(iframeStr);
  });
});

