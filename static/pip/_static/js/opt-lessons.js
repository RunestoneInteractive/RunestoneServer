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

var backend_script = 'exec'; // URL of backend script, which must eventually call pg_logger.py

var myVisualizer = null; // singleton ExecutionVisualizer instance

var lessonScript = null;
var metadataJSON = null;

function parseLessonFile(dat) {
  var toks = dat.split('======');

  // globals
  lessonScript = toks[0].rtrim();
  metadataJSON = $.parseJSON(toks[1]);

  $('#lessonTitle').html(metadataJSON.title);
  $('#lessonDescription').html(metadataJSON.description);

  document.title = metadataJSON.title + ' - Online Python Tutor (v3)';

  $.get(backend_script,
        {user_script : lessonScript},
        function(dataFromBackend) {
          var trace = dataFromBackend.trace;
          
          // don't enter visualize mode if there are killer errors:
          if (!trace ||
              (trace.length == 0) ||
              (trace[trace.length - 1].event == 'uncaught_exception')) {

            if (trace.length == 1) {
              alert(trace[0].exception_msg);
            }
            else {
              alert("Whoa, unknown error! Reload to try again, or report a bug to philip@pgbovine.net\n\n(Click the 'Generate URL' button to include a unique URL in your email bug report.)");
            }
          }
          else {
            myVisualizer = new ExecutionVisualizer('pyOutputPane',
                                                   dataFromBackend,
                                                   {embeddedMode: true,
                                                    updateOutputCallback: updateLessonNarration});

            myVisualizer.updateOutput();
          }
        },
        "json");
}

function updateLessonNarration(myViz) {
  var curInstr = myViz.curInstr;

  assert(metadataJSON);

  var annotation = metadataJSON[curInstr + 1]; // adjust for indexing diffs
  if (annotation) {
    $('#lessonNarration').html(annotation);
  }
  else {
    $('#lessonNarration').html('');
  }

  // hack from John DeNero to ensure that once a div grows it height, it
  // never shrinks again
  $('#lessonNarration').css('min-height', $('#lessonNarration').css('height'));
}

$(document).ready(function() {

  //$.get("lessons/aliasing.txt", parseLessonFile);
  //$.get("lessons/dive-into-python-311.txt", parseLessonFile);
  //$.get("lessons/for-else.txt", parseLessonFile);
  $.get("lessons/varargs.txt", parseLessonFile);

  // log a generic AJAX error handler
  $(document).ajaxError(function() {
    alert("Server error (possibly due to memory/resource overload).");
  });


  // redraw connector arrows on window resize
  $(window).resize(function() {
    if (myVisualizer) {
      myVisualizer.redrawConnectors();
    }
  });

});
