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


/* To import, put this at the top of your HTML page:

<!-- requirements for pytutor.js -->
<script type="text/javascript" src="js/d3.v2.min.js"></script>
<script type="text/javascript" src="js/jquery-1.8.2.min.js"></script>
<script type="text/javascript" src="js/jquery.ba-bbq.min.js"></script> <!-- for handling back button and URL hashes -->
<script type="text/javascript" src="js/jquery.jsPlumb-1.3.10-all-min.js "></script> <!-- for rendering SVG connectors
                                                                                         DO NOT UPGRADE ABOVE 1.3.10 OR ELSE BREAKAGE WILL OCCUR -->
<script type="text/javascript" src="js/jquery-ui-1.8.24.custom.min.js"></script> <!-- for sliders and other UI elements -->
<link type="text/css" href="css/ui-lightness/jquery-ui-1.8.24.custom.css" rel="stylesheet" />

<!-- for annotation bubbles -->
<script type="text/javascript" src="js/jquery.qtip.min.js"></script>
<link type="text/css" href="css/jquery.qtip.css" rel="stylesheet" />

<script type="text/javascript" src="js/pytutor.js"></script>
<link rel="stylesheet" href="css/pytutor.css"/>

*/


/* Coding gotchas:

- NEVER use naked $(__) or d3.select(__) statements to select DOM elements.

  ALWAYS use myViz.domRoot or myViz.domRootD3 for jQuery and D3, respectively.

  Otherwise things will break in weird ways when you have more than one visualization
  embedded within a webpage, due to multiple matches in the global namespace.


- always use generateID to generate unique CSS IDs, or else things will break
  when multiple ExecutionVisualizer instances are displayed on a webpage

*/


var SVG_ARROW_POLYGON = '0,3 12,3 12,0 18,5 12,10 12,7 0,7';
var SVG_ARROW_HEIGHT = 10; // must match height of SVG_ARROW_POLYGON

var curVisualizerID = 1; // global to uniquely identify each ExecutionVisualizer instance

// domRootID is the string ID of the root element where to render this instance
// dat is data returned by the Python Tutor backend consisting of two fields:
//   code  - string of executed code
//   trace - a full execution trace
//
// params is an object containing optional parameters, such as:
//   jumpToEnd - if non-null, jump to the very end of execution
//   startingInstruction - the (zero-indexed) execution point to display upon rendering
//   hideOutput - hide "Program output" display
//   codeDivHeight - maximum height of #pyCodeOutputDiv (in integer pixels)
//   codeDivWidth  - maximum width  of #pyCodeOutputDiv (in integer pixels)
//   editCodeBaseURL - the base URL to visit when the user clicks 'Edit code' (if null, then 'Edit code' link hidden)
//   allowEditAnnotations - allow user to edit per-step annotations (default: false)
//   embeddedMode         - shortcut for hideOutput=true, allowEditAnnotations=false
//   disableHeapNesting   - if true, then render all heap objects at the top level (i.e., no nested objects)
//                          codeDivWidth=350, codeDivHeight=400
//   drawParentPointers   - if true, then draw environment diagram parent pointers for all frames
//                          WARNING: there are hard-to-debug MEMORY LEAKS associated with activating this option
//   textualMemoryLabels  - render references using textual memory labels rather than as jsPlumb arrows.
//                          this is good for slow browsers or when used with disableHeapNesting
//                          to prevent "arrow overload"
//   showOnlyOutputs      - show only program outputs and NOT internal data structures
//   updateOutputCallback - function to call (with 'this' as parameter)
//                          whenever this.updateOutput() is called
//                          (BEFORE rendering the output display)
//   heightChangeCallback - function to call (with 'this' as parameter)
//                          whenever the HEIGHT of #dataViz changes
//   verticalStack - if true, then stack code display ON TOP of visualization
//                   (else place side-by-side)
//   executeCodeWithRawInputFunc - function to call when you want to re-execute the given program
//                                 with some new user input (somewhat hacky!)
//   highlightLines - highlight current and previously executed lines (default: false)
//   arrowLines     - draw arrows pointing to current and previously executed lines (default: true)
//   pyCrazyMode    - run with Py2crazy, which provides expression-level
//                    granularity instead of line-level granularity (HIGHLY EXPERIMENTAL!)
function ExecutionVisualizer(domRootID, dat, params) {
  this.curInputCode = dat.code.rtrim(); // kill trailing spaces
  this.curTrace = dat.trace;


  // optional filtering to remove redundancy ...
  // ok, we're gonna filter out all trace entries of 'call' events,
  // because each one contains IDENTICAL state information as the
  // 'step_line' entry immediately following it. this filtering allows the
  // visualization to not show as much redundancy.
  this.curTrace = this.curTrace.filter(function(e) {return e.event != 'call';});

  // if the final entry is raw_input or mouse_input, then trim it from the trace and
  // set a flag to prompt for user input when execution advances to the
  // end of the trace
  if (this.curTrace.length > 0) {
    var lastEntry = this.curTrace[this.curTrace.length - 1];
    if (lastEntry.event == 'raw_input') {
      this.promptForUserInput = true;
      this.userInputPromptStr = lastEntry.prompt;
      this.curTrace.pop() // kill last entry so that it doesn't get displayed
    }
    else if (lastEntry.event == 'mouse_input') {
      this.promptForMouseInput = true;
      this.userInputPromptStr = lastEntry.prompt;
      this.curTrace.pop() // kill last entry so that it doesn't get displayed
    }
  }

  this.curInstr = 0;

  this.params = params;
  if (!this.params) {
    this.params = {}; // make it an empty object by default
  }

  var arrowLinesDef = (this.params.arrowLines !== undefined);
  var highlightLinesDef = (this.params.highlightLines !== undefined);

  if (!arrowLinesDef && !highlightLinesDef) {
      // neither is set
      this.params.highlightLines = false;
      this.params.arrowLines = true;
  }
  else if (arrowLinesDef && highlightLinesDef) {
      // both are set, so just use their set values
  }
  else if (arrowLinesDef) {
      // only arrowLines set
      this.params.highlightLines = !(this.params.arrowLines);
  }
  else {
      // only highlightLines set
      this.params.arrowLines = !(this.params.highlightLines);
  }

  // audible!
  if (this.params.pyCrazyMode) {
      this.params.arrowLines = this.params.highlightLines = false;
  }

  // David's original logic ...
  /*
  if (!this.params.arrowLines && !this.params.highlightLines) {
      this.params.highlightLines = false;
      this.params.arrowLines = true;
  }
  else if (this.params.arrowLines) {
      this.params.arrowLines = (this.params.arrowLines == true);
      this.params.highlightLines = !(this.params.arrowLines);
  }
  else if (this.params.highlightLines) {
      this.params.highlightLines = (this.params.highlightLines == true);
      this.params.arrowLines = !(this.params.highlightLines);
  }
  else {
      this.params.arrowLines = (this.params.arrowLines == true);
      this.params.highlightLines = (this.params.highlightLines == true);
  }
  */

  // needs to be unique!
  this.visualizerID = curVisualizerID;
  curVisualizerID++;


  this.leftGutterSvgInitialized = false;
  this.arrowOffsetY = undefined;
  this.codeRowHeight = undefined;

  // avoid 'undefined' state
  this.disableHeapNesting = (this.params.disableHeapNesting == true);
  this.drawParentPointers = (this.params.drawParentPointers == true);
  this.textualMemoryLabels = (this.params.textualMemoryLabels == true);
  this.showOnlyOutputs = (this.params.showOnlyOutputs == true);

  this.executeCodeWithRawInputFunc = this.params.executeCodeWithRawInputFunc;

  // cool, we can create a separate jsPlumb instance for each visualization:
  this.jsPlumbInstance = jsPlumb.getInstance({
    Endpoint: ["Dot", {radius:3}],
    EndpointStyles: [{fillStyle: connectorBaseColor}, {fillstyle: null} /* make right endpoint invisible */],
    Anchors: ["RightMiddle", "LeftMiddle"],
    PaintStyle: {lineWidth:1, strokeStyle: connectorBaseColor},

    // bezier curve style:
    //Connector: [ "Bezier", { curviness:15 }], /* too much 'curviness' causes lines to run together */
    //Overlays: [[ "Arrow", { length: 14, width:10, foldback:0.55, location:0.35 }]],

    // state machine curve style:
    Connector: [ "StateMachine" ],
    Overlays: [[ "Arrow", { length: 10, width:7, foldback:0.55, location:1 }]],
    EndpointHoverStyles: [{fillStyle: connectorHighlightColor}, {fillstyle: null} /* make right endpoint invisible */],
    HoverPaintStyle: {lineWidth: 1, strokeStyle: connectorHighlightColor},
  });


  // true iff trace ended prematurely since maximum instruction limit has
  // been reached
  var instrLimitReached = false;


  // the root elements for jQuery and D3 selections, respectively.
  // ALWAYS use these and never use naked $(__) or d3.select(__)
  this.domRoot = $('#' + domRootID);
  this.domRoot.data("vis",this);  // bnm store a reference to this as div data for use later.
  this.domRootD3 = d3.select('#' + domRootID);

  // stick a new div.ExecutionVisualizer within domRoot and make that
  // the new domRoot:
  this.domRoot.html('<div class="ExecutionVisualizer"></div>');

  this.domRoot = this.domRoot.find('div.ExecutionVisualizer');
  this.domRootD3 = this.domRootD3.select('div.ExecutionVisualizer');


  // initialize in renderPyCodeOutput()
  this.codeOutputLines = null;
  this.breakpoints = null;           // set of execution points to set as breakpoints
  this.sortedBreakpointsList = null; // sorted and synced with breakpointLines
  this.hoverBreakpoints = null;      // set of breakpoints because we're HOVERING over a given line

  this.enableTransitions = false; // EXPERIMENTAL - enable transition effects


  this.hasRendered = false;

  this.render(); // go for it!
  
}


// create a unique ID, which is often necessary so that jsPlumb doesn't get confused
// due to multiple ExecutionVisualizer instances being displayed simultaneously
ExecutionVisualizer.prototype.generateID = function(original_id) {
  // (it's safer to start names with a letter rather than a number)
  return 'v' + this.visualizerID + '__' + original_id;
}


ExecutionVisualizer.prototype.render = function() {
  if (this.hasRendered) {
    alert('ERROR: You should only call render() ONCE on an ExecutionVisualizer object.');
    return;
  }


  var myViz = this; // to prevent confusion of 'this' inside of nested functions

  var codeDisplayHTML =
    '<div id="codeDisplayDiv">\
       <div id="pyCodeOutputDiv"/>\
       <div id="editCodeLinkDiv"><a id="editBtn">Edit code</a></div>\
       <div id="executionSlider"/>\
       <div id="vcrControls">\
         <button id="jmpFirstInstr", type="button">&lt;&lt; First</button>\
         <button id="jmpStepBack", type="button">&lt; Back</button>\
         <span id="curInstr">Step ? of ?</span>\
         <button id="jmpStepFwd", type="button">Forward &gt;</button>\
         <button id="jmpLastInstr", type="button">Last &gt;&gt;</button>\
       </div>\
       <div id="errorOutput"/>\
       <div id="legendDiv"/>\
       <div id="stepAnnotationDiv">\
         <textarea class="annotationText" id="stepAnnotationEditor" cols="60" rows="3"></textarea>\
         <div class="annotationText" id="stepAnnotationViewer"></div>\
       </div>\
       <div id="annotateLinkDiv"><button id="annotateBtn" type="button">Annotate this step</button></div>\
     </div>';

  var outputsHTML =
    '<div id="htmlOutputDiv"></div>\
     <div id="progOutputs">\
       Program output:<br/>\
       <textarea id="pyStdout" cols="50" rows="10" wrap="off" readonly></textarea>\
     </div>';

  var codeVizHTML =
    '<div id="dataViz">\
       <table id="stackHeapTable">\
         <tr>\
           <td id="stack_td">\
             <div id="globals_area">\
               <div id="stackHeader">Frames</div>\
             </div>\
             <div id="stack"></div>\
           </td>\
           <td id="heap_td">\
             <div id="heap">\
               <div id="heapHeader">Objects</div>\
             </div>\
           </td>\
         </tr>\
       </table>\
     </div>';

  var vizHeaderHTML =
    '<div id="vizHeader">\
       <textarea class="vizTitleText" id="vizTitleEditor" cols="60" rows="1"></textarea>\
       <div class="vizTitleText" id="vizTitleViewer"></div>\
       <textarea class="vizDescriptionText" id="vizDescriptionEditor" cols="75" rows="2"></textarea>\
       <div class="vizDescriptionText" id="vizDescriptionViewer"></div>\
    </div>';

  if (this.params.verticalStack) {
    this.domRoot.html(vizHeaderHTML + '<table border="0" class="visualizer"><tr><td class="vizLayoutTd" id="vizLayoutTdFirst"">' +
                      codeDisplayHTML + '</td></tr><tr><td class="vizLayoutTd" id="vizLayoutTdSecond">' +
                      codeVizHTML + '</td></tr></table>');
  }
  else {
    this.domRoot.html(vizHeaderHTML + '<table border="0" class="visualizer"><tr><td class="vizLayoutTd" id="vizLayoutTdFirst">' +
                      codeDisplayHTML + '</td><td class="vizLayoutTd" id="vizLayoutTdSecond">' +
                      codeVizHTML + '</td></tr></table>');
  }

  if (this.showOnlyOutputs) {
    myViz.domRoot.find('#dataViz').hide();
    this.domRoot.find('#vizLayoutTdSecond').append(outputsHTML);

    if (this.params.verticalStack) {
      this.domRoot.find('#vizLayoutTdSecond').css('padding-top', '25px');
    }
    else {
      this.domRoot.find('#vizLayoutTdSecond').css('padding-left', '25px');
    }
  }
  else {
    this.domRoot.find('#vizLayoutTdFirst').append(outputsHTML);
  }

  if (this.params.arrowLines) {
      this.domRoot.find('#legendDiv')
          .append('<svg id="prevLegendArrowSVG"/> line that has just executed')
          .append('<p style="margin-top: 4px"><svg id="curLegendArrowSVG"/> next line to execute</p>');
      
      myViz.domRootD3.select('svg#prevLegendArrowSVG')
          .append('polygon')
          .attr('points', SVG_ARROW_POLYGON)
          .attr('fill', lightArrowColor);
      
      myViz.domRootD3.select('svg#curLegendArrowSVG')
          .append('polygon')
          .attr('points', SVG_ARROW_POLYGON)
          .attr('fill', darkArrowColor);
  }
  else if (this.params.highlightLines) {
      myViz.domRoot.find('#legendDiv')
          .append('<span class="highlight-legend highlight-prev">line that has just executed</span> ')
          .append('<span class="highlight-legend highlight-cur">next line to execute</span>')
  }
  else if (this.params.pyCrazyMode) {
      myViz.domRoot.find('#legendDiv')
          .append('<a href="https://github.com/pgbovine/Py2crazy">Py2crazy</a> mode!')
          .append(' Stepping through (roughly) each executed expression. Color codes:<p/>')
          .append('<span class="pycrazy-highlight-prev">expression that just executed</span><br/>')
          .append('<span class="pycrazy-highlight-cur">next expression to execute</span>');
  }


  if (this.params.editCodeBaseURL) {
    var urlStr = $.param.fragment(this.params.editCodeBaseURL,
                                  {code: this.curInputCode},
                                  2);
    this.domRoot.find('#editBtn').attr('href', urlStr);
  }
  else {
    this.domRoot.find('#editCodeLinkDiv').hide(); // just hide for simplicity!
    this.domRoot.find('#editBtn').attr('href', "#");
    this.domRoot.find('#editBtn').click(function(){return false;}); // DISABLE the link!
  }

  if (this.params.allowEditAnnotations !== undefined) {
    this.allowEditAnnotations = this.params.allowEditAnnotations;
  }
  else {
    this.allowEditAnnotations = false;
  }

  if (this.params.pyCrazyMode !== undefined) {
    this.pyCrazyMode = this.params.pyCrazyMode;
  }
  else {
    this.pyCrazyMode = false;
  }

  this.domRoot.find('#stepAnnotationEditor').hide();

  if (this.params.embeddedMode) {
    this.params.hideOutput = true; // put this before hideOutput handler

    // don't override if they've already been set!
    if (this.params.codeDivWidth === undefined) {
      this.params.codeDivWidth = 350;
    }

    if (this.params.codeDivHeight === undefined) {
      this.params.codeDivHeight = 400;
    }
    
    this.allowEditAnnotations = false;
  }

  myViz.editAnnotationMode = false;

  if (this.allowEditAnnotations) {
    var ab = this.domRoot.find('#annotateBtn');

    ab.click(function() {
      if (myViz.editAnnotationMode) {
        myViz.enterViewAnnotationsMode();

        myViz.domRoot.find("#jmpFirstInstr,#jmpLastInstr,#jmpStepBack,#jmpStepFwd,#executionSlider,#editCodeLinkDiv,#stepAnnotationViewer").show();
        myViz.domRoot.find('#stepAnnotationEditor').hide();
        ab.html('Annotate this step');
      }
      else {
        myViz.enterEditAnnotationsMode();

        myViz.domRoot.find("#jmpFirstInstr,#jmpLastInstr,#jmpStepBack,#jmpStepFwd,#executionSlider,#editCodeLinkDiv,#stepAnnotationViewer").hide();
        myViz.domRoot.find('#stepAnnotationEditor').show();
        ab.html('Done annotating');
      }
    });
  }
  else {
    this.domRoot.find('#annotateBtn').hide();
  }

  
  // not enough room for these extra buttons ...
  if (this.params.codeDivWidth &&
      this.params.codeDivWidth < 470) {
    this.domRoot.find('#jmpFirstInstr').hide();
    this.domRoot.find('#jmpLastInstr').hide();
  }


  if (this.params.codeDivWidth) {
    // set width once
    this.domRoot.find('#codeDisplayDiv').width(
      this.params.codeDivWidth);
    // it will propagate to the slider
  }

  // enable left-right draggable pane resizer (originally from David Pritchard)
  var syncStdoutWidth = function(event, ui){
    $("#vizLayoutTdFirst #pyStdout").width(ui.size.width-2*parseInt($("#pyStdout").css("padding-left")));};
  $('#codeDisplayDiv').resizable({handles:"e", resize: syncStdoutWidth});
  syncStdoutWidth(null, {size: {width: $('#codeDisplayDiv').width()}});


  if (this.params.codeDivHeight) {
    this.domRoot.find('#pyCodeOutputDiv')
      .css('max-height', this.params.codeDivHeight + 'px');
  }


  // create a persistent globals frame
  // (note that we need to keep #globals_area separate from #stack for d3 to work its magic)
  this.domRoot.find("#globals_area").append('<div class="stackFrame" id="'
    + myViz.generateID('globals') + '"><div id="' + myViz.generateID('globals_header')
    + '" class="stackFrameHeader">Global variables</div><table class="stackFrameVarTable" id="'
    + myViz.generateID('global_table') + '"></table></div>');


  if (this.params.hideOutput) {
    this.domRoot.find('#progOutputs').hide();
  }

  this.domRoot.find("#jmpFirstInstr").click(function() {
    myViz.curInstr = 0;
    myViz.updateOutput();
  });

  this.domRoot.find("#jmpLastInstr").click(function() {
    myViz.curInstr = myViz.curTrace.length - 1;
    myViz.updateOutput();
  });

  this.domRoot.find("#jmpStepBack").click(function() {
    myViz.stepBack();
  });

  this.domRoot.find("#jmpStepFwd").click(function() {
    myViz.stepForward();
  });

  // disable controls initially ...
  this.domRoot.find("#vcrControls #jmpFirstInstr").attr("disabled", true);
  this.domRoot.find("#vcrControls #jmpStepBack").attr("disabled", true);
  this.domRoot.find("#vcrControls #jmpStepFwd").attr("disabled", true);
  this.domRoot.find("#vcrControls #jmpLastInstr").attr("disabled", true);



  // must postprocess curTrace prior to running precomputeCurTraceLayouts() ...
  var lastEntry = this.curTrace[this.curTrace.length - 1];

  this.instrLimitReached = (lastEntry.event == 'instruction_limit_reached');

  if (this.instrLimitReached) {
    this.curTrace.pop() // kill last entry
    var warningMsg = lastEntry.exception_msg;
    myViz.domRoot.find("#errorOutput").html(htmlspecialchars(warningMsg));
    myViz.domRoot.find("#errorOutput").show();
  }

  // set up slider after postprocessing curTrace

  var sliderDiv = this.domRoot.find('#executionSlider');
  sliderDiv.slider({min: 0, max: this.curTrace.length - 1, step: 1});
  //disable keyboard actions on the slider itself (to prevent double-firing of events)
  sliderDiv.find(".ui-slider-handle").unbind('keydown');
  // make skinnier and taller
  sliderDiv.find(".ui-slider-handle").css('width', '0.8em');
  sliderDiv.find(".ui-slider-handle").css('height', '1.4em');
  this.domRoot.find(".ui-widget-content").css('font-size', '0.9em');

  this.domRoot.find('#executionSlider').bind('slide', function(evt, ui) {
    // this is SUPER subtle. if this value was changed programmatically,
    // then evt.originalEvent will be undefined. however, if this value
    // was changed by a user-initiated event, then this code should be
    // executed ...
    if (evt.originalEvent) {
      myViz.curInstr = ui.value;
      myViz.updateOutput();
    }
  });


  if (this.params.startingInstruction) {
    assert(0 <= this.params.startingInstruction &&
           this.params.startingInstruction < this.curTrace.length);
    this.curInstr = this.params.startingInstruction;
  }

  if (this.params.jumpToEnd) {
    this.curInstr = this.curTrace.length - 1;
  }


  this.precomputeCurTraceLayouts();

  this.renderPyCodeOutput();

  this.updateOutput();

  this.hasRendered = true;
}


ExecutionVisualizer.prototype.showVizHeaderViewMode = function() {
  var titleVal = this.domRoot.find('#vizTitleEditor').val().trim();
  var  descVal = this.domRoot.find('#vizDescriptionEditor').val().trim();

  this.domRoot.find('#vizTitleEditor,#vizDescriptionEditor').hide();

  if (!titleVal && !descVal) {
    this.domRoot.find('#vizHeader').hide();
  }
  else {
    this.domRoot.find('#vizHeader,#vizTitleViewer,#vizDescriptionViewer').show();
    if (titleVal) {
      this.domRoot.find('#vizTitleViewer').html(htmlsanitize(titleVal)); // help prevent HTML/JS injection attacks
    }

    if (descVal) {
      this.domRoot.find('#vizDescriptionViewer').html(htmlsanitize(descVal)); // help prevent HTML/JS injection attacks
    }
  }
}

ExecutionVisualizer.prototype.showVizHeaderEditMode = function() {
  this.domRoot.find('#vizHeader').show();

  this.domRoot.find('#vizTitleViewer,#vizDescriptionViewer').hide();
  this.domRoot.find('#vizTitleEditor,#vizDescriptionEditor').show();
}


ExecutionVisualizer.prototype.destroyAllAnnotationBubbles = function() {
  var myViz = this;

  // hopefully destroys all old bubbles and reclaims their memory
  if (myViz.allAnnotationBubbles) {
    $.each(myViz.allAnnotationBubbles, function(i, e) {
      e.destroyQTip();
    });
  }

  // remove this handler as well!
  this.domRoot.find('#pyCodeOutputDiv').unbind('scroll');

  myViz.allAnnotationBubbles = null;
}

ExecutionVisualizer.prototype.initStepAnnotation = function() {
  var curEntry = this.curTrace[this.curInstr];
  if (curEntry.stepAnnotation) {
    this.domRoot.find("#stepAnnotationViewer").html(htmlsanitize(curEntry.stepAnnotation)); // help prevent HTML/JS injection attacks
    this.domRoot.find("#stepAnnotationEditor").val(curEntry.stepAnnotation);
  }
  else {
    this.domRoot.find("#stepAnnotationViewer").html('');
    this.domRoot.find("#stepAnnotationEditor").val('');
  }
}

ExecutionVisualizer.prototype.initAllAnnotationBubbles = function() {
  var myViz = this;

  // TODO: check for memory leaks
  //console.log('initAllAnnotationBubbles');

  myViz.destroyAllAnnotationBubbles();

  var codelineIDs = [];
  $.each(this.domRoot.find('#pyCodeOutput .cod'), function(i, e) {
    codelineIDs.push($(e).attr('id'));
  });

  var heapObjectIDs = [];
  $.each(this.domRoot.find('.heapObject'), function(i, e) {
    heapObjectIDs.push($(e).attr('id'));
  });

  var variableIDs = [];
  $.each(this.domRoot.find('.variableTr'), function(i, e) {
    variableIDs.push($(e).attr('id'));
  });

  var frameIDs = [];
  $.each(this.domRoot.find('.stackFrame'), function(i, e) {
    frameIDs.push($(e).attr('id'));
  });

  myViz.allAnnotationBubbles = [];

  $.each(codelineIDs, function(i,e) {myViz.allAnnotationBubbles.push(new AnnotationBubble(myViz, 'codeline', e));});
  $.each(heapObjectIDs, function(i,e) {myViz.allAnnotationBubbles.push(new AnnotationBubble(myViz, 'object', e));});
  $.each(variableIDs, function(i,e) {myViz.allAnnotationBubbles.push(new AnnotationBubble(myViz, 'variable', e));});
  $.each(frameIDs, function(i,e) {myViz.allAnnotationBubbles.push(new AnnotationBubble(myViz, 'frame', e));});


  this.domRoot.find('#pyCodeOutputDiv').scroll(function() {
    $.each(myViz.allAnnotationBubbles, function(i, e) {
      if (e.type == 'codeline') {
        e.redrawCodelineBubble();
      }
    });
  });

  //console.log('initAllAnnotationBubbles', myViz.allAnnotationBubbles.length);
}


ExecutionVisualizer.prototype.enterViewAnnotationsMode = function() {
  this.editAnnotationMode = false;
  var curEntry = this.curTrace[this.curInstr];

  // TODO: check for memory leaks!!!
  var myViz = this;

  if (!myViz.allAnnotationBubbles) {
    if (curEntry.bubbleAnnotations) {
      // If there is an existing annotations object, then initiate all annotations bubbles
      // and display them in 'View' mode
      myViz.initAllAnnotationBubbles();

      $.each(myViz.allAnnotationBubbles, function(i, e) {
        var txt = curEntry.bubbleAnnotations[e.domID];
        if (txt) {
          e.preseedText(txt);
        }
      });
    }
  }


  if (myViz.allAnnotationBubbles) {
    var curAnnotations = {};

    $.each(myViz.allAnnotationBubbles, function(i, e) {
      e.enterViewMode();

      if (e.text) {
        curAnnotations[e.domID] = e.text;
      }
    });

    // Save annotations directly into the current trace entry as an 'annotations' object
    // directly mapping domID -> text.
    //
    // NB: This scheme can break if the functions for generating domIDs are altered.
    curEntry.bubbleAnnotations = curAnnotations;
  }

  var stepAnnotationEditorVal = myViz.domRoot.find("#stepAnnotationEditor").val().trim();
  if (stepAnnotationEditorVal) {
    curEntry.stepAnnotation = stepAnnotationEditorVal;
  }
  else {
    delete curEntry.stepAnnotation; // go as far as to DELETE this field entirely
  }

  myViz.initStepAnnotation();

  myViz.showVizHeaderViewMode();

  // redraw all connectors and bubbles in new vertical position ..
  myViz.redrawConnectors();
  myViz.redrawAllAnnotationBubbles();
}

ExecutionVisualizer.prototype.enterEditAnnotationsMode = function() {
  this.editAnnotationMode = true;

  // TODO: check for memory leaks!!!
  var myViz = this;

  var curEntry = this.curTrace[this.curInstr];

  if (!myViz.allAnnotationBubbles) {
    myViz.initAllAnnotationBubbles();
  }

  $.each(myViz.allAnnotationBubbles, function(i, e) {
    e.enterEditMode();
  });


  if (curEntry.stepAnnotation) {
    myViz.domRoot.find("#stepAnnotationEditor").val(curEntry.stepAnnotation);
  }
  else {
    myViz.domRoot.find("#stepAnnotationEditor").val('');
  }


  myViz.showVizHeaderEditMode();

  // redraw all connectors and bubbles in new vertical position ..
  myViz.redrawConnectors();
  myViz.redrawAllAnnotationBubbles();
}


ExecutionVisualizer.prototype.redrawAllAnnotationBubbles = function() {
  if (this.allAnnotationBubbles) {
    $.each(this.allAnnotationBubbles, function(i, e) {
      e.redrawBubble();
    });
  }
}


// find the previous/next breakpoint to c or return -1 if it doesn't exist
ExecutionVisualizer.prototype.findPrevBreakpoint = function() {
  var myViz = this;
  var c = myViz.curInstr;

  if (myViz.sortedBreakpointsList.length == 0) {
    return -1;
  }
  else {
    for (var i = 1; i < myViz.sortedBreakpointsList.length; i++) {
      var prev = myViz.sortedBreakpointsList[i-1];
      var cur = myViz.sortedBreakpointsList[i];
      if (c <= prev)
        return -1;
      if (cur >= c)
        return prev;
    }

    // final edge case:
    var lastElt = myViz.sortedBreakpointsList[myViz.sortedBreakpointsList.length - 1];
    return (lastElt < c) ? lastElt : -1;
  }
}

ExecutionVisualizer.prototype.findNextBreakpoint = function() {
  var myViz = this;
  var c = myViz.curInstr;

  if (myViz.sortedBreakpointsList.length == 0) {
    return -1;
  }
  // usability hack: if you're currently on a breakpoint, then
  // single-step forward to the next execution point, NOT the next
  // breakpoint. it's often useful to see what happens when the line
  // at a breakpoint executes.
  else if ($.inArray(c, myViz.sortedBreakpointsList) >= 0) {
    return c + 1;
  }
  else {
    for (var i = 0; i < myViz.sortedBreakpointsList.length - 1; i++) {
      var cur = myViz.sortedBreakpointsList[i];
      var next = myViz.sortedBreakpointsList[i+1];
      if (c < cur)
        return cur;
      if (cur <= c && c < next) // subtle
        return next;
    }

    // final edge case:
    var lastElt = myViz.sortedBreakpointsList[myViz.sortedBreakpointsList.length - 1];
    return (lastElt > c) ? lastElt : -1;
  }
}


// returns true if action successfully taken
ExecutionVisualizer.prototype.stepForward = function() {
  var myViz = this;

  if (myViz.editAnnotationMode) {
    return;
  }

  if (myViz.curInstr < myViz.curTrace.length - 1) {
    // if there is a next breakpoint, then jump to it ...
    if (myViz.sortedBreakpointsList.length > 0) {
      var nextBreakpoint = myViz.findNextBreakpoint();
      if (nextBreakpoint != -1)
        myViz.curInstr = nextBreakpoint;
      else
        myViz.curInstr += 1; // prevent "getting stuck" on a solitary breakpoint
    }
    else {
      myViz.curInstr += 1;
    }
    myViz.updateOutput(true);
    return true;
  }

  return false;
}

// returns true if action successfully taken
ExecutionVisualizer.prototype.stepBack = function() {
  var myViz = this;

  if (myViz.editAnnotationMode) {
    return;
  }

  if (myViz.curInstr > 0) {
    // if there is a prev breakpoint, then jump to it ...
    if (myViz.sortedBreakpointsList.length > 0) {
      var prevBreakpoint = myViz.findPrevBreakpoint();
      if (prevBreakpoint != -1)
        myViz.curInstr = prevBreakpoint;
      else
        myViz.curInstr -= 1; // prevent "getting stuck" on a solitary breakpoint
    }
    else {
      myViz.curInstr -= 1;
    }
    myViz.updateOutput();
    return true;
  }

  return false;
}


ExecutionVisualizer.prototype.renderPyCodeOutput = function() {
  var myViz = this; // to prevent confusion of 'this' inside of nested functions


  // initialize!
  this.breakpoints = d3.map();
  this.sortedBreakpointsList = [];
  this.hoverBreakpoints = d3.map();

  // an array of objects with the following fields:
  //   'text' - the text of the line of code
  //   'lineNumber' - one-indexed (always the array index + 1)
  //   'executionPoints' - an ordered array of zero-indexed execution points where this line was executed
  //   'breakpointHere' - has a breakpoint been set here?
  this.codeOutputLines = [];


  function renderSliderBreakpoints() {
    myViz.domRoot.find("#executionSliderFooter").empty();

    // I originally didn't want to delete and re-create this overlay every time,
    // but if I don't do so, there are weird flickering artifacts with clearing
    // the SVG container; so it's best to just delete and re-create the container each time
    var sliderOverlay = myViz.domRootD3.select('#executionSliderFooter')
      .append('svg')
      .attr('id', 'sliderOverlay')
      .attr('width', myViz.domRoot.find('#executionSlider').width())
      .attr('height', 12);

    var xrange = d3.scale.linear()
      .domain([0, myViz.curTrace.length - 1])
      .range([0, myViz.domRoot.find('#executionSlider').width()]);

    sliderOverlay.selectAll('rect')
      .data(myViz.sortedBreakpointsList)
      .enter().append('rect')
      .attr('x', function(d, i) {
        // make the edge cases look decent
        if (d == 0) {
          return 0;
        }
        else {
          return xrange(d) - 3;
        }
      })
      .attr('y', 0)
      .attr('width', 2)
      .attr('height', 12)
      .style('fill', function(d) {
         if (myViz.hoverBreakpoints.has(d)) {
           return hoverBreakpointColor;
         }
         else {
           return breakpointColor;
         }
      });
  }

  function _getSortedBreakpointsList() {
    var ret = [];
    myViz.breakpoints.forEach(function(k, v) {
      ret.push(Number(k)); // these should be NUMBERS, not strings
    });
    ret.sort(function(x,y){return x-y}); // WTF, javascript sort is lexicographic by default!
    return ret;
  }

  function addToBreakpoints(executionPoints) {
    $.each(executionPoints, function(i, ep) {
      myViz.breakpoints.set(ep, 1);
    });
    myViz.sortedBreakpointsList = _getSortedBreakpointsList();
  }

  function removeFromBreakpoints(executionPoints) {
    $.each(executionPoints, function(i, ep) {
      myViz.breakpoints.remove(ep);
    });
    myViz.sortedBreakpointsList = _getSortedBreakpointsList();
  }


  function setHoverBreakpoint(t) {
    var exePts = d3.select(t).datum().executionPoints;

    // don't do anything if exePts is empty
    // (i.e., this line was never executed)
    if (!exePts || exePts.length == 0) {
      return;
    }

    myViz.hoverBreakpoints = d3.map();
    $.each(exePts, function(i, ep) {
      // don't add redundant entries
      if (!myViz.breakpoints.has(ep)) {
        myViz.hoverBreakpoints.set(ep, 1);
      }
    });

    addToBreakpoints(exePts);
    renderSliderBreakpoints();
  }


  function setBreakpoint(t) {
    var exePts = d3.select(t).datum().executionPoints;

    // don't do anything if exePts is empty
    // (i.e., this line was never executed)
    if (!exePts || exePts.length == 0) {
      return;
    }

    addToBreakpoints(exePts);

    // remove from hoverBreakpoints so that slider display immediately changes color
    $.each(exePts, function(i, ep) {
      myViz.hoverBreakpoints.remove(ep);
    });

    d3.select(t.parentNode).select('td.lineNo').style('color', breakpointColor);
    d3.select(t.parentNode).select('td.lineNo').style('font-weight', 'bold');

    renderSliderBreakpoints();
  }

  function unsetBreakpoint(t) {
    var exePts = d3.select(t).datum().executionPoints;

    // don't do anything if exePts is empty
    // (i.e., this line was never executed)
    if (!exePts || exePts.length == 0) {
      return;
    }

    removeFromBreakpoints(exePts);

    var lineNo = d3.select(t).datum().lineNumber;

    renderSliderBreakpoints();
  }

  var lines = this.curInputCode.split('\n');

  for (var i = 0; i < lines.length; i++) {
    var cod = lines[i];

    var n = {};
    n.text = cod;
    n.lineNumber = i + 1;
    n.executionPoints = [];
    n.breakpointHere = false;

    $.each(this.curTrace, function(j, elt) {
      if (elt.line == n.lineNumber) {
        n.executionPoints.push(j);
      }
    });

 
    // if there is a comment containing 'breakpoint' and this line was actually executed,
    // then set a breakpoint on this line
    var breakpointInComment = false;
    var toks = cod.split('#');
    for (var j = 1 /* start at index 1, not 0 */; j < toks.length; j++) {
      if (toks[j].indexOf('breakpoint') != -1) {
        breakpointInComment = true;
      }
    }

    if (breakpointInComment && n.executionPoints.length > 0) {
      n.breakpointHere = true;
      addToBreakpoints(n.executionPoints);
    }

    this.codeOutputLines.push(n);
  }


  myViz.domRoot.find('#pyCodeOutputDiv').empty();

  // maps this.codeOutputLines to both table columns
  var codeOutputD3 = this.domRootD3.select('#pyCodeOutputDiv')
    .append('table')
    .attr('id', 'pyCodeOutput')
    .selectAll('tr')
    .data(this.codeOutputLines)
    .enter().append('tr')
    .selectAll('td')
    .data(function(d, i){return [d, d] /* map full data item down both columns */;})
    .enter().append('td')
    .attr('class', function(d, i) {
      if (i == 0) {
        return 'lineNo';
      }
      else {
        return 'cod';
      }
    })
    .attr('id', function(d, i) {
      if (i == 0) {
        return 'lineNo' + d.lineNumber;
      }
      else {
        return myViz.generateID('cod' + d.lineNumber); // make globally unique (within the page)
      }
    })
    .html(function(d, i) {
      if (i == 0) {
        return d.lineNumber;
      }
      else {
        return htmlspecialchars(d.text);
      }
    });

  // create a left-most gutter td that spans ALL rows ...
  // (NB: valign="top" is CRUCIAL for this to work in IE)
  if (myViz.params.arrowLines) {
      myViz.domRoot.find('#pyCodeOutput tr:first')
          .prepend('<td id="gutterTD" valign="top" rowspan="' + this.codeOutputLines.length + '"><svg id="leftCodeGutterSVG"/></td>');
      
      // create prevLineArrow and curLineArrow
      myViz.domRootD3.select('svg#leftCodeGutterSVG')
          .append('polygon')
          .attr('id', 'prevLineArrow')
          .attr('points', SVG_ARROW_POLYGON)
          .attr('fill', lightArrowColor);
      
      myViz.domRootD3.select('svg#leftCodeGutterSVG')
          .append('polygon')
          .attr('id', 'curLineArrow')
          .attr('points', SVG_ARROW_POLYGON)
          .attr('fill', darkArrowColor);
  }

  // 2012-09-05: Disable breakpoints for now to simplify UX
  /*
  if (!this.params.embeddedMode) {
    codeOutputD3.style('cursor', function(d, i) {return 'pointer'})
    .on('mouseover', function() {
      setHoverBreakpoint(this);
    })
    .on('mouseout', function() {
      myViz.hoverBreakpoints = d3.map();

      var breakpointHere = d3.select(this).datum().breakpointHere;

      if (!breakpointHere) {
        unsetBreakpoint(this);
      }

      renderSliderBreakpoints(); // get rid of hover breakpoint colors
    })
    .on('mousedown', function() {
      // don't do anything if exePts is empty
      // (i.e., this line was never executed)
      var exePts = d3.select(this).datum().executionPoints;
      if (!exePts || exePts.length == 0) {
        return;
      }

      // toggle breakpoint
      d3.select(this).datum().breakpointHere = !d3.select(this).datum().breakpointHere;

      var breakpointHere = d3.select(this).datum().breakpointHere;
      if (breakpointHere) {
        setBreakpoint(this);
      }
      else {
        unsetBreakpoint(this);
      }
    });

    renderSliderBreakpoints(); // renders breakpoints written in as code comments
  }
  */

}


// takes a string inputStr and returns an HTML version with
// the characters from [highlightIndex, highlightIndex+extent) highlighted with
// a span of class highlightCssClass
function htmlWithHighlight(inputStr, highlightInd, extent, highlightCssClass) {
  var prefix = '';
  if (highlightInd > 0) {
    prefix = inputStr.slice(0, highlightInd);
  }

  var highlightedChars = inputStr.slice(highlightInd, highlightInd + extent);

  var suffix = '';
  if (highlightInd + extent < inputStr.length) {
    suffix = inputStr.slice(highlightInd + extent, inputStr.length);
  }

  // ... then set the current line to lineHTML
  var lineHTML = htmlspecialchars(prefix) +
      '<span class="' + highlightCssClass + '">' +
      htmlspecialchars(highlightedChars) +
      '</span>' +
      htmlspecialchars(suffix);
  return lineHTML;
}


// This function is called every time the display needs to be updated
// smoothTransition is OPTIONAL!
ExecutionVisualizer.prototype.updateOutput = function(smoothTransition) {
  assert(this.curTrace);

  var myViz = this; // to prevent confusion of 'this' inside of nested functions

  // there's no point in re-rendering if this pane isn't even visible in the first place!
  if (!myViz.domRoot.is(':visible')) {
    return;
  }


  // really nitpicky!!! gets the difference in width between the code display
  // and the maximum width of its enclosing div
  myViz.codeHorizontalOverflow = myViz.domRoot.find('#pyCodeOutput').width() - myViz.domRoot.find('#pyCodeOutputDiv').width();
  // should always be positive
  if (myViz.codeHorizontalOverflow < 0) {
    myViz.codeHorizontalOverflow = 0;
  }


  // crucial resets for annotations (TODO: kludgy)
  myViz.destroyAllAnnotationBubbles();
  myViz.initStepAnnotation();


  var prevDataVizHeight = myViz.domRoot.find('#dataViz').height();


  var gutterSVG = myViz.domRoot.find('svg#leftCodeGutterSVG');

  // one-time initialization of the left gutter
  // (we often can't do this earlier since the entire pane
  //  might be invisible and hence returns a height of zero or NaN
  //  -- the exact format depends on browser)
  if (!myViz.leftGutterSvgInitialized && myViz.params.arrowLines) {
    // set the gutter's height to match that of its parent
    gutterSVG.height(gutterSVG.parent().height());

    var firstRowOffsetY = myViz.domRoot.find('table#pyCodeOutput tr:first').offset().top;

    // first take care of edge case when there's only one line ...
    myViz.codeRowHeight = myViz.domRoot.find('table#pyCodeOutput td.cod:first').height();

    // ... then handle the (much more common) multi-line case ...
    // this weird contortion is necessary to get the accurate row height on Internet Explorer
    // (simpler methods work on all other major browsers, erghhhhhh!!!)
    if (this.codeOutputLines && this.codeOutputLines.length > 1) {
      var secondRowOffsetY = myViz.domRoot.find('table#pyCodeOutput tr:nth-child(2)').offset().top;
      myViz.codeRowHeight = secondRowOffsetY - firstRowOffsetY;
    }

    assert(myViz.codeRowHeight > 0);

    var gutterOffsetY = gutterSVG.offset().top;
    var teenyAdjustment = gutterOffsetY - firstRowOffsetY;

    // super-picky detail to adjust the vertical alignment of arrows so that they line up
    // well with the pointed-to code text ...
    // (if you want to manually adjust tableTop, then ~5 is a reasonable number)
    myViz.arrowOffsetY = Math.floor((myViz.codeRowHeight / 2) - (SVG_ARROW_HEIGHT / 2)) - teenyAdjustment;

    myViz.leftGutterSvgInitialized = true;
  }

  if (myViz.params.arrowLines) {
      assert(myViz.arrowOffsetY !== undefined);
      assert(myViz.codeRowHeight !== undefined);
      assert(0 <= myViz.arrowOffsetY && myViz.arrowOffsetY <= myViz.codeRowHeight);
  }

  // call the callback if necessary (BEFORE rendering)
  if (this.params.updateOutputCallback) {
    this.params.updateOutputCallback(this);
  }


  var curEntry = this.curTrace[this.curInstr];
  var hasError = false;
  // bnm  Render a question
  if (curEntry.question) {
      //alert(curEntry.question.text);
      
      $('#'+curEntry.question.div).modal({position:["25%","50%"]});
  }

  // render VCR controls:
  var totalInstrs = this.curTrace.length;

  var isLastInstr = (this.curInstr == (totalInstrs-1));

  var vcrControls = myViz.domRoot.find("#vcrControls");

  if (isLastInstr) {
    if (this.promptForUserInput || this.promptForMouseInput) {
      vcrControls.find("#curInstr").html('<b><font color="' + brightRed + '">' + this.userInputPromptStr + '</font></b>');

      // don't do smooth transition since prompt() is modal so it doesn't
      // give the animation background thread time to run
      smoothTransition = false;
    }
    else if (this.instrLimitReached) {
      vcrControls.find("#curInstr").html("Instruction limit reached");
    }
    else {
      vcrControls.find("#curInstr").html("Program terminated");
    }
  }
  else {
    vcrControls.find("#curInstr").html("Step " +
                                       String(this.curInstr + 1) +
                                       " of " + String(totalInstrs-1));
  }


  vcrControls.find("#jmpFirstInstr").attr("disabled", false);
  vcrControls.find("#jmpStepBack").attr("disabled", false);
  vcrControls.find("#jmpStepFwd").attr("disabled", false);
  vcrControls.find("#jmpLastInstr").attr("disabled", false);

  if (this.curInstr == 0) {
    vcrControls.find("#jmpFirstInstr").attr("disabled", true);
    vcrControls.find("#jmpStepBack").attr("disabled", true);
  }
  if (isLastInstr) {
    vcrControls.find("#jmpLastInstr").attr("disabled", true);
    vcrControls.find("#jmpStepFwd").attr("disabled", true);
  }


  // PROGRAMMATICALLY change the value, so evt.originalEvent should be undefined
  myViz.domRoot.find('#executionSlider').slider('value', this.curInstr);


  // render error (if applicable):
  if (curEntry.event == 'exception' ||
      curEntry.event == 'uncaught_exception') {
    assert(curEntry.exception_msg);

    if (curEntry.exception_msg == "Unknown error") {
      myViz.domRoot.find("#errorOutput").html('Unknown error: Please email a bug report to philip@pgbovine.net');
    }
    else {
      myViz.domRoot.find("#errorOutput").html(htmlspecialchars(curEntry.exception_msg));
    }

    myViz.domRoot.find("#errorOutput").show();

    hasError = true;
  }
  else {
    if (!this.instrLimitReached) { // ugly, I know :/
      myViz.domRoot.find("#errorOutput").hide();
    }
  }


  function highlightCodeLine() {
    /* if instrLimitReached, then treat like a normal non-terminating line */
    var isTerminated = (!myViz.instrLimitReached && isLastInstr);

    var pcod = myViz.domRoot.find('#pyCodeOutputDiv');

    var curLineNumber = null;
    var prevLineNumber = null;

    // only relevant if in myViz.pyCrazyMode
    var prevColumn = undefined;
    var prevExprStartCol = undefined;
    var prevExprWidth = undefined;

    var curIsReturn = (curEntry.event == 'return');
    var prevIsReturn = false;


    if (myViz.curInstr > 0) {
      prevLineNumber = myViz.curTrace[myViz.curInstr - 1].line;
      prevIsReturn = (myViz.curTrace[myViz.curInstr - 1].event == 'return');

      if (myViz.pyCrazyMode) {
        var p = myViz.curTrace[myViz.curInstr - 1];
        prevColumn = p.column;
        // if these don't exist, set reasonable defaults
        prevExprStartCol = (p.expr_start_col !== undefined) ? p.expr_start_col : p.column;
        prevExprWidth = (p.expr_width !== undefined) ? p.expr_width : 1;
      }
    }

    curLineNumber = curEntry.line;

    if (myViz.pyCrazyMode) {
      var curColumn = curEntry.column;

      // if these don't exist, set reasonable defaults
      var curExprStartCol = (curEntry.expr_start_col !== undefined) ? curEntry.expr_start_col : curColumn;
      var curExprWidth = (curEntry.expr_width !== undefined) ? curEntry.expr_width : 1;

      var curLineInfo = myViz.codeOutputLines[curLineNumber - 1];
      assert(curLineInfo.lineNumber == curLineNumber);
      var codeAtLine = curLineInfo.text;

      // shotgun approach: reset ALL lines to their natural (unbolded) state
      $.each(myViz.codeOutputLines, function(i, e) {
        var d = myViz.generateID('cod' + e.lineNumber);
        myViz.domRoot.find('#' + d).html(htmlspecialchars(e.text));
      });


      // Three possible cases:
      // 1. previous and current trace entries are on the SAME LINE
      // 2. previous and current trace entries are on different lines
      // 3. there is no previous trace entry

      if (prevLineNumber == curLineNumber) {
        var curLineHTML = '';

        // tricky tricky!
        // generate a combined line with both previous and current
        // columns highlighted

        for (var i = 0; i < codeAtLine.length; i++) {
          var isCur = (curExprStartCol <= i) && (i < curExprStartCol + curExprWidth);
          var isPrev = (prevExprStartCol <= i) && (i < prevExprStartCol + prevExprWidth);

          var htmlEscapedChar = htmlspecialchars(codeAtLine[i]);

          if (isCur && isPrev) {
            curLineHTML += '<span class="pycrazy-highlight-prev-and-cur">' + htmlEscapedChar + '</span>';
          }
          else if (isPrev) {
            curLineHTML += '<span class="pycrazy-highlight-prev">' + htmlEscapedChar + '</span>';
          }
          else if (isCur) {
            curLineHTML += '<span class="pycrazy-highlight-cur">' + htmlEscapedChar + '</span>';
          }
          else {
            curLineHTML += htmlEscapedChar;
          }
        }

        assert(curLineHTML);
        myViz.domRoot.find('#' + myViz.generateID('cod' + curLineNumber)).html(curLineHTML);
      }
      else {
        if (prevLineNumber) {
          var prevLineInfo = myViz.codeOutputLines[prevLineNumber - 1];
          var prevLineHTML = htmlWithHighlight(prevLineInfo.text, prevExprStartCol, prevExprWidth, 'pycrazy-highlight-prev');
          myViz.domRoot.find('#' + myViz.generateID('cod' + prevLineNumber)).html(prevLineHTML);
        }
        var curLineHTML = htmlWithHighlight(codeAtLine, curExprStartCol, curExprWidth, 'pycrazy-highlight-cur');
        myViz.domRoot.find('#' + myViz.generateID('cod' + curLineNumber)).html(curLineHTML);
      }
    }

    // on 'return' events, give a bit more of a vertical nudge to show that
    // the arrow is aligned with the 'bottom' of the line ...
    var prevVerticalNudge = prevIsReturn ? Math.floor(myViz.codeRowHeight / 2) : 0;
    var curVerticalNudge  = curIsReturn  ? Math.floor(myViz.codeRowHeight / 2) : 0;


    // edge case for the final instruction :0
    if (isTerminated && !hasError) {
      // don't show redundant arrows on the same line when terminated ...
      if (prevLineNumber == curLineNumber) {
        curLineNumber = null;
      }
      // otherwise have a smaller vertical nudge (to fit at bottom of display table)
      else {
        curVerticalNudge = curVerticalNudge - 2;
      }
    }

    if (myViz.params.arrowLines) {
        if (prevLineNumber) {
            var pla = myViz.domRootD3.select('#prevLineArrow');
            var translatePrevCmd = 'translate(0, ' + (((prevLineNumber - 1) * myViz.codeRowHeight) + myViz.arrowOffsetY + prevVerticalNudge) + ')';
            
            if (smoothTransition) {
                pla 
                    .transition()
                    .duration(200)
                    .attr('fill', 'white')
                    .each('end', function() {
                        pla
                            .attr('transform', translatePrevCmd)
                            .attr('fill', lightArrowColor);
                        
                        gutterSVG.find('#prevLineArrow').show(); // show at the end to avoid flickering
                    });
            }
            else {
                pla.attr('transform', translatePrevCmd)
                gutterSVG.find('#prevLineArrow').show();
            }
            
        }
        else {
            gutterSVG.find('#prevLineArrow').hide();
        }
        
        if (curLineNumber) {
            var cla = myViz.domRootD3.select('#curLineArrow');
            var translateCurCmd = 'translate(0, ' + (((curLineNumber - 1) * myViz.codeRowHeight) + myViz.arrowOffsetY + curVerticalNudge) + ')';
            
            if (smoothTransition) {
                cla 
                    .transition()
                    .delay(200)
                    .duration(250)
                    .attr('transform', translateCurCmd);
            }
            else {
                cla.attr('transform', translateCurCmd);
            }
            
            gutterSVG.find('#curLineArrow').show();
        }
        else {
            gutterSVG.find('#curLineArrow').hide();
        }
    }

    myViz.domRootD3.selectAll('#pyCodeOutputDiv td.cod')
      .style('border-top', function(d) {
        if (hasError && (d.lineNumber == curEntry.line)) {
          return '1px solid ' + errorColor;
        }
        else {
          return '';
        }
      })
      .style('border-bottom', function(d) {
        // COPY AND PASTE ALERT!
        if (hasError && (d.lineNumber == curEntry.line)) {
          return '1px solid ' + errorColor;
        }
        else {
          return '';
        }
      });

    // returns True iff lineNo is visible in pyCodeOutputDiv
    function isOutputLineVisible(lineNo) {
      var lineNoTd = myViz.domRoot.find('#lineNo' + lineNo);
      var LO = lineNoTd.offset().top;

      var PO = pcod.offset().top;
      var ST = pcod.scrollTop();
      var H = pcod.height();

      // add a few pixels of fudge factor on the bottom end due to bottom scrollbar
      return (PO <= LO) && (LO < (PO + H - 30));
    }


    // smoothly scroll pyCodeOutputDiv so that the given line is at the center
    function scrollCodeOutputToLine(lineNo) {
      var lineNoTd = myViz.domRoot.find('#lineNo' + lineNo);
      var LO = lineNoTd.offset().top;

      var PO = pcod.offset().top;
      var ST = pcod.scrollTop();
      var H = pcod.height();

      pcod.stop(); // first stop all previously-queued animations
      pcod.animate({scrollTop: (ST + (LO - PO - (Math.round(H / 2))))}, 300);
    }

    if (myViz.params.highlightLines) {
        myViz.domRoot.find('#pyCodeOutputDiv td.cod').removeClass('highlight-prev');
        myViz.domRoot.find('#pyCodeOutputDiv td.cod').removeClass('highlight-cur');
        if (curLineNumber)
            myViz.domRoot.find('#'+myViz.generateID('cod'+curLineNumber)).addClass('highlight-cur');        
        if (prevLineNumber)
            myViz.domRoot.find('#'+myViz.generateID('cod'+prevLineNumber)).addClass('highlight-prev');      
    }


    // smoothly scroll code display
    if (!isOutputLineVisible(curEntry.line)) {
      scrollCodeOutputToLine(curEntry.line);
    }

  } // end of highlightCodeLine


  // render code output:
  if (curEntry.line) {
    highlightCodeLine();
  }

  // render stdout:

  // if there isn't anything in curEntry.stdout, don't even bother
  // displaying the pane
  if (curEntry.stdout) {
    this.domRoot.find('#progOutputs').show();

    // keep original horizontal scroll level:
    var oldLeft = myViz.domRoot.find("#pyStdout").scrollLeft();
    myViz.domRoot.find("#pyStdout").val(curEntry.stdout);

    myViz.domRoot.find("#pyStdout").scrollLeft(oldLeft);
    // scroll to bottom, though:
    myViz.domRoot.find("#pyStdout").scrollTop(myViz.domRoot.find("#pyStdout")[0].scrollHeight);
  }
  else {
    this.domRoot.find('#progOutputs').hide();
  }


  // inject user-specified HTML/CSS/JS output:
  // YIKES -- HUGE CODE INJECTION VULNERABILITIES :O
  myViz.domRoot.find("#htmlOutputDiv").empty();
  if (curEntry.html_output) {
    if (curEntry.css_output) {
      myViz.domRoot.find("#htmlOutputDiv").append('<style type="text/css">' + curEntry.css_output + '</style>');
    }
    myViz.domRoot.find("#htmlOutputDiv").append(curEntry.html_output);

    // inject and run JS *after* injecting HTML and CSS
    if (curEntry.js_output) {
      // NB: when jQuery injects JS, it executes the code immediately
      // and then removes the entire <script> block from the DOM
      // http://stackoverflow.com/questions/610995/jquery-cant-append-script-element
      myViz.domRoot.find("#htmlOutputDiv").append('<script type="text/javascript">' + curEntry.js_output + '</script>');
    }
  }


  // finally, render all of the data structures
  this.renderDataStructures();

  this.enterViewAnnotationsMode(); // ... and render optional annotations (if any exist)


  // call the callback if necessary (BEFORE rendering)
  if (myViz.domRoot.find('#dataViz').height() != prevDataVizHeight) {
    if (this.params.heightChangeCallback) {
      this.params.heightChangeCallback(this);
    }
  }


  if (isLastInstr && this.executeCodeWithRawInputFunc) {
    if (this.promptForUserInput) {
      // blocking prompt dialog!
      // put a default string of '' or else it looks ugly in IE
      var userInput = prompt(this.userInputPromptStr, '');

      // if you hit 'Cancel' in prompt(), it returns null
      if (userInput !== null) {
        // after executing, jump back to this.curInstr to give the
        // illusion of continuity
        this.executeCodeWithRawInputFunc(userInput, this.curInstr);
      }
    }
  }

} // end of updateOutput


// Pre-compute the layout of top-level heap objects for ALL execution
// points as soon as a trace is first loaded. The reason why we want to
// do this is so that when the user steps through execution points, the
// heap objects don't "jiggle around" (i.e., preserving positional
// invariance). Also, if we set up the layout objects properly, then we
// can take full advantage of d3 to perform rendering and transitions.

ExecutionVisualizer.prototype.precomputeCurTraceLayouts = function() {

  // curTraceLayouts is a list of top-level heap layout "objects" with the
  // same length as curTrace after it's been fully initialized. Each
  // element of curTraceLayouts is computed from the contents of its
  // immediate predecessor, thus ensuring that objects don't "jiggle
  // around" between consecutive execution points.
  //
  // Each top-level heap layout "object" is itself a LIST of LISTS of
  // object IDs, where each element of the outer list represents a row,
  // and each element of the inner list represents columns within a
  // particular row. Each row can have a different number of columns. Most
  // rows have exactly ONE column (representing ONE object ID), but rows
  // containing 1-D linked data structures have multiple columns. Each
  // inner list element looks something like ['row1', 3, 2, 1] where the
  // first element is a unique row ID tag, which is used as a key for d3 to
  // preserve "object constancy" for updates, transitions, etc. The row ID
  // is derived from the FIRST object ID inserted into the row. Since all
  // object IDs are unique, all row IDs will also be unique.

  /* This is a good, simple example to test whether objects "jiggle"

  x = [1, [2, [3, None]]]
  y = [4, [5, [6, None]]]

  x[1][1] = y[1]

  */
  this.curTraceLayouts = [];
  this.curTraceLayouts.push([]); // pre-seed with an empty sentinel to simplify the code

  assert(this.curTrace.length > 0);

  var myViz = this; // to prevent confusion of 'this' inside of nested functions


  $.each(this.curTrace, function(i, curEntry) {
    var prevLayout = myViz.curTraceLayouts[myViz.curTraceLayouts.length - 1];

    // make a DEEP COPY of prevLayout to use as the basis for curLine
    var curLayout = $.extend(true /* deep copy */ , [], prevLayout);

    // initialize with all IDs from curLayout
    var idsToRemove = d3.map();
    $.each(curLayout, function(i, row) {
      for (var j = 1 /* ignore row ID tag */; j < row.length; j++) {
        idsToRemove.set(row[j], 1);
      }
    });

    var idsAlreadyLaidOut = d3.map(); // to prevent infinite recursion


    function curLayoutIndexOf(id) {
      for (var i = 0; i < curLayout.length; i++) {
        var row = curLayout[i];
        var index = row.indexOf(id);
        if (index > 0) { // index of 0 is impossible since it's the row ID tag
          return {row: row, index: index}
        }
      }
      return null;
    }


    function recurseIntoObject(id, curRow, newRow) {
      //console.log('recurseIntoObject', id,
      //            $.extend(true /* make a deep copy */ , [], curRow),
      //            $.extend(true /* make a deep copy */ , [], newRow));

      // heuristic for laying out 1-D linked data structures: check for enclosing elements that are
      // structurally identical and then lay them out as siblings in the same "row"
      var heapObj = curEntry.heap[id];
      assert(heapObj);

      if (heapObj[0] == 'LIST' || heapObj[0] == 'TUPLE' || heapObj[0] == 'SET') {
        $.each(heapObj, function(ind, child) {
          if (ind < 1) return; // skip type tag

          if (!isPrimitiveType(child)) {
            var childID = getRefID(child);
            if (structurallyEquivalent(heapObj, curEntry.heap[childID])) {
              updateCurLayout(childID, curRow, newRow);
            }
            else if (myViz.disableHeapNesting) {
              updateCurLayout(childID, [], []);
            }
          }
        });
      }
      else if (heapObj[0] == 'DICT') {
        $.each(heapObj, function(ind, child) {
          if (ind < 1) return; // skip type tag

          if (myViz.disableHeapNesting) {
            var dictKey = child[0];
            if (!isPrimitiveType(dictKey)) {
              var keyChildID = getRefID(dictKey);
              updateCurLayout(keyChildID, [], []);
            }
          }

          var dictVal = child[1];
          if (!isPrimitiveType(dictVal)) {
            var childID = getRefID(dictVal);
            if (structurallyEquivalent(heapObj, curEntry.heap[childID])) {
              updateCurLayout(childID, curRow, newRow);
            }
            else if (myViz.disableHeapNesting) {
              updateCurLayout(childID, [], []);
            }
          }
        });
      }
      else if (heapObj[0] == 'INSTANCE' || heapObj[0] == 'CLASS') {
        jQuery.each(heapObj, function(ind, child) {
          var headerLength = (heapObj[0] == 'INSTANCE') ? 2 : 3;
          if (ind < headerLength) return;

          if (myViz.disableHeapNesting) {
            var instKey = child[0];
            if (!isPrimitiveType(instKey)) {
              var keyChildID = getRefID(instKey);
              updateCurLayout(keyChildID, [], []);
            }
          }

          var instVal = child[1];
          if (!isPrimitiveType(instVal)) {
            var childID = getRefID(instVal);
            if (structurallyEquivalent(heapObj, curEntry.heap[childID])) {
              updateCurLayout(childID, curRow, newRow);
            }
            else if (myViz.disableHeapNesting) {
              updateCurLayout(childID, [], []);
            }
          }
        });
      }
    }


    // a krazy function!
    // id     - the new object ID to be inserted somewhere in curLayout
    //          (if it's not already in there)
    // curRow - a row within curLayout where new linked list
    //          elements can be appended onto (might be null)
    // newRow - a new row that might be spliced into curRow or appended
    //          as a new row in curLayout
    function updateCurLayout(id, curRow, newRow) {
      if (idsAlreadyLaidOut.has(id)) {
        return; // PUNT!
      }

      var curLayoutLoc = curLayoutIndexOf(id);

      var alreadyLaidOut = idsAlreadyLaidOut.has(id);
      idsAlreadyLaidOut.set(id, 1); // unconditionally set now

      // if id is already in curLayout ...
      if (curLayoutLoc) {
        var foundRow = curLayoutLoc.row;
        var foundIndex = curLayoutLoc.index;

        idsToRemove.remove(id); // this id is already accounted for!

        // very subtle ... if id hasn't already been handled in
        // this iteration, then splice newRow into foundRow. otherwise
        // (later) append newRow onto curLayout as a truly new row
        if (!alreadyLaidOut) {
          // splice the contents of newRow right BEFORE foundIndex.
          // (Think about when you're trying to insert in id=3 into ['row1', 2, 1]
          //  to represent a linked list 3->2->1. You want to splice the 3
          //  entry right before the 2 to form ['row1', 3, 2, 1])
          if (newRow.length > 1) {
            var args = [foundIndex, 0];
            for (var i = 1; i < newRow.length; i++) { // ignore row ID tag
              args.push(newRow[i]);
              idsToRemove.remove(newRow[i]);
            }
            foundRow.splice.apply(foundRow, args);

            // remove ALL elements from newRow since they've all been accounted for
            // (but don't reassign it away to an empty list, since the
            // CALLER checks its value. TODO: how to get rid of this gross hack?!?)
            newRow.splice(0, newRow.length);
          }
        }

        // recurse to find more top-level linked entries to append onto foundRow
        recurseIntoObject(id, foundRow, []);
      }
      else {
        // push id into newRow ...
        if (newRow.length == 0) {
          newRow.push('row' + id); // unique row ID (since IDs are unique)
        }
        newRow.push(id);

        // recurse to find more top-level linked entries ...
        recurseIntoObject(id, curRow, newRow);


        // if newRow hasn't been spliced into an existing row yet during
        // a child recursive call ...
        if (newRow.length > 0) {
          if (curRow && curRow.length > 0) {
            // append onto the END of curRow if it exists
            for (var i = 1; i < newRow.length; i++) { // ignore row ID tag
              curRow.push(newRow[i]);
            }
          }
          else {
            // otherwise push to curLayout as a new row
            //
            // TODO: this might not always look the best, since we might
            // sometimes want to splice newRow in the MIDDLE of
            // curLayout. Consider this example:
            //
            // x = [1,2,3]
            // y = [4,5,6]
            // x = [7,8,9]
            //
            // when the third line is executed, the arrows for x and y
            // will be crossed (ugly!) since the new row for the [7,8,9]
            // object is pushed to the end (bottom) of curLayout. The
            // proper behavior is to push it to the beginning of
            // curLayout where the old row for 'x' used to be.
            curLayout.push($.extend(true /* make a deep copy */ , [], newRow));
          }

          // regardless, newRow is now accounted for, so clear it
          for (var i = 1; i < newRow.length; i++) { // ignore row ID tag
            idsToRemove.remove(newRow[i]);
          }
          newRow.splice(0, newRow.length); // kill it!
        }

      }
    }


    // iterate through all globals and ordered stack frames and call updateCurLayout
    $.each(curEntry.ordered_globals, function(i, varname) {
      var val = curEntry.globals[varname];
      if (val !== undefined) { // might not be defined at this line, which is OKAY!
        if (!isPrimitiveType(val)) {
          var id = getRefID(val);
          updateCurLayout(id, null, []);
        }
      }
    });

    $.each(curEntry.stack_to_render, function(i, frame) {
      $.each(frame.ordered_varnames, function(xxx, varname) {
        var val = frame.encoded_locals[varname];

        if (!isPrimitiveType(val)) {
          var id = getRefID(val);
          updateCurLayout(id, null, []);
        }
      });
    });


    // iterate through remaining elements of idsToRemove and REMOVE them from curLayout
    idsToRemove.forEach(function(id, xxx) {
      id = Number(id); // keys are stored as strings, so convert!!!
      $.each(curLayout, function(rownum, row) {
        var ind = row.indexOf(id);
        if (ind > 0) { // remember that index 0 of the row is the row ID tag
          row.splice(ind, 1);
        }
      });
    });

    // now remove empty rows (i.e., those with only a row ID tag) from curLayout
    curLayout = curLayout.filter(function(row) {return row.length > 1});

    myViz.curTraceLayouts.push(curLayout);
  });

  this.curTraceLayouts.splice(0, 1); // remove seeded empty sentinel element
  assert (this.curTrace.length == this.curTraceLayouts.length);
}


var heapPtrSrcRE = /__heap_pointer_src_/;

// The "3.0" version of renderDataStructures renders variables in
// a stack, values in a separate heap, and draws line connectors
// to represent both stack->heap object references and, more importantly,
// heap->heap references. This version was created in August 2012.
//
// The "2.0" version of renderDataStructures renders variables in
// a stack and values in a separate heap, with data structure aliasing
// explicitly represented via line connectors (thanks to jsPlumb lib).
// This version was created in September 2011.
//
// The ORIGINAL "1.0" version of renderDataStructures
// was created in January 2010 and rendered variables and values
// INLINE within each stack frame without any explicit representation
// of data structure aliasing. That is, aliased objects were rendered
// multiple times, and a unique ID label was used to identify aliases.
ExecutionVisualizer.prototype.renderDataStructures = function() {

  var myViz = this; // to prevent confusion of 'this' inside of nested functions

  var curEntry = this.curTrace[this.curInstr];
  var curToplevelLayout = this.curTraceLayouts[this.curInstr];

  // for simplicity (but sacrificing some performance), delete all
  // connectors and redraw them from scratch. doing so avoids mysterious
  // jsPlumb connector alignment issues when the visualizer's enclosing
  // div contains, say, a "position: relative;" CSS tag
  // (which happens in the IPython Notebook)
  var existingConnectionEndpointIDs = d3.map();
  myViz.jsPlumbInstance.select({scope: 'varValuePointer'}).each(function(c) {
    // This is VERY crude, but to prevent multiple redundant HEAP->HEAP
    // connectors from being drawn with the same source and origin, we need to first
    // DELETE ALL existing HEAP->HEAP connections, and then re-render all of
    // them in each call to this function. The reason why we can't safely
    // hold onto them is because there's no way to guarantee that the
    // *__heap_pointer_src_<src id> IDs are consistent across execution points.
    //
    // thus, only add to existingConnectionEndpointIDs if this is NOT heap->heap
    if (!c.sourceId.match(heapPtrSrcRE)) {
      existingConnectionEndpointIDs.set(c.sourceId, c.targetId);
    }
  });

  var existingParentPointerConnectionEndpointIDs = d3.map();
  myViz.jsPlumbInstance.select({scope: 'frameParentPointer'}).each(function(c) {
    existingParentPointerConnectionEndpointIDs.set(c.sourceId, c.targetId);
  });


  // Heap object rendering phase:


  // Key:   CSS ID of the div element representing the stack frame variable
  //        (for stack->heap connections) or heap object (for heap->heap connections)
  //        the format is: '<this.visualizerID>__heap_pointer_src_<src id>'
  // Value: CSS ID of the div element representing the value rendered in the heap
  //        (the format is: '<this.visualizerID>__heap_object_<id>')
  //
  // The reason we need to prepend this.visualizerID is because jsPlumb needs
  // GLOBALLY UNIQUE IDs for use as connector endpoints.

  // the only elements in these sets are NEW elements to be rendered in this
  // particular call to renderDataStructures.
  var connectionEndpointIDs = d3.map();
  var heapConnectionEndpointIDs = d3.map(); // subset of connectionEndpointIDs for heap->heap connections

  // analogous to connectionEndpointIDs, except for environment parent pointers
  var parentPointerConnectionEndpointIDs = d3.map();

  var heap_pointer_src_id = 1; // increment this to be unique for each heap_pointer_src_*


  var renderedObjectIDs = d3.map();

  // count everything in curToplevelLayout as already rendered since we will render them
  // in d3 .each() statements
  $.each(curToplevelLayout, function(xxx, row) {
    for (var i = 0; i < row.length; i++) {
      renderedObjectIDs.set(row[i], 1);
    }
  });



  // use d3 to render the heap by mapping curToplevelLayout into <table class="heapRow">
  // and <td class="toplevelHeapObject"> elements

  var heapRows = myViz.domRootD3.select('#heap')
    .selectAll('table.heapRow')
    .data(curToplevelLayout, function(objLst) {
      return objLst[0]; // return first element, which is the row ID tag
  });


  // insert new heap rows
  heapRows.enter().append('table')
    //.each(function(objLst, i) {console.log('NEW ROW:', objLst, i);})
    .attr('class', 'heapRow');

  // delete a heap row
  var hrExit = heapRows.exit();

  if (myViz.enableTransitions) {
    hrExit
      .style('opacity', '1')
      .transition()
      .style('opacity', '0')
      .duration(500)
      .each('end', function() {
        hrExit
          .each(function(d, idx) {
            $(this).empty(); // crucial for garbage collecting jsPlumb connectors!
          })
          .remove();
        myViz.redrawConnectors();
      });
  }
  else {
    hrExit
      .each(function(d, idx) {
        $(this).empty(); // crucial for garbage collecting jsPlumb connectors!
      })
      .remove();
  }


  // update an existing heap row
  var toplevelHeapObjects = heapRows
    //.each(function(objLst, i) { console.log('UPDATE ROW:', objLst, i); })
    .selectAll('td.toplevelHeapObject')
    .data(function(d, i) {return d.slice(1, d.length);}, /* map over each row, skipping row ID tag */
          function(objID) {return objID;} /* each object ID is unique for constancy */);

  // insert a new toplevelHeapObject
  var tlhEnter = toplevelHeapObjects.enter().append('td')
    .attr('class', 'toplevelHeapObject')
    .attr('id', function(d, i) {return 'toplevel_heap_object_' + d;});

  if (myViz.enableTransitions) {
    tlhEnter
      .style('opacity', '0')
      .style('border-color', 'red')
      .transition()
      .style('opacity', '1') /* fade in */
      .duration(700)
      .each('end', function() {
        tlhEnter.transition()
          .style('border-color', 'white') /* kill border */
          .duration(300)
        });
  }

  // remember that the enter selection is added to the update
  // selection so that we can process it later ...

  // update a toplevelHeapObject
  toplevelHeapObjects
    .order() // VERY IMPORTANT to put in the order corresponding to data elements
    .each(function(objID, i) {
      //console.log('NEW/UPDATE ELT', objID);

      // TODO: add a smoother transition in the future
      // Right now, just delete the old element and render a new one in its place
      $(this).empty();
      renderCompoundObject(objID, $(this), true);
    });

  // delete a toplevelHeapObject
  var tlhExit = toplevelHeapObjects.exit();

  if (myViz.enableTransitions) {
    tlhExit.transition()
      .style('opacity', '0') /* fade out */
      .duration(500)
      .each('end', function() {
        tlhExit
          .each(function(d, idx) {
            $(this).empty(); // crucial for garbage collecting jsPlumb connectors!
          })
          .remove();
        myViz.redrawConnectors();
      });
  }
  else {
    tlhExit
      .each(function(d, idx) {
        $(this).empty(); // crucial for garbage collecting jsPlumb connectors!
      })
      .remove();
  }


  function renderNestedObject(obj, d3DomElement) {
    if (isPrimitiveType(obj)) {
      renderPrimitiveObject(obj, d3DomElement);
    }
    else {
      renderCompoundObject(getRefID(obj), d3DomElement, false);
    }
  }


  function renderPrimitiveObject(obj, d3DomElement) {
    var typ = typeof obj;

    if (obj == null) {
      d3DomElement.append('<span class="nullObj">None</span>');
    }
    else if (typ == "number") {
      d3DomElement.append('<span class="numberObj">' + obj + '</span>');
    }
    else if (typ == "boolean") {
      if (obj) {
        d3DomElement.append('<span class="boolObj">True</span>');
      }
      else {
        d3DomElement.append('<span class="boolObj">False</span>');
      }
    }
    else if (typ == "string") {
      // escape using htmlspecialchars to prevent HTML/script injection
      var literalStr = htmlspecialchars(obj);

      // print as a double-quoted string literal
      literalStr = literalStr.replace(new RegExp('\"', 'g'), '\\"'); // replace ALL
      literalStr = '"' + literalStr + '"';

      d3DomElement.append('<span class="stringObj">' + literalStr + '</span>');
    }
    else {
      assert(false);
    }
  }


  function renderCompoundObject(objID, d3DomElement, isTopLevel) {
    if (!isTopLevel && renderedObjectIDs.has(objID)) {
      var srcDivID = myViz.generateID('heap_pointer_src_' + heap_pointer_src_id);
      heap_pointer_src_id++; // just make sure each source has a UNIQUE ID

      var dstDivID = myViz.generateID('heap_object_' + objID);

      if (myViz.textualMemoryLabels) {
        var labelID = srcDivID + '_text_label';
        d3DomElement.append('<div class="objectIdLabel" id="' + labelID + '">id' + objID + '</div>');

        myViz.domRoot.find('div#' + labelID).hover(
          function() {
            myViz.jsPlumbInstance.connect({source: labelID, target: dstDivID,
                                           scope: 'varValuePointer'});
          },
          function() {
            myViz.jsPlumbInstance.select({source: labelID}).detach();
          });
      }
      else {
        // render jsPlumb arrow source since this heap object has already been rendered
        // (or will be rendered soon)

        // add a stub so that we can connect it with a connector later.
        // IE needs this div to be NON-EMPTY in order to properly
        // render jsPlumb endpoints, so that's why we add an "&nbsp;"!
        d3DomElement.append('<div id="' + srcDivID + '">&nbsp;</div>');

        assert(!connectionEndpointIDs.has(srcDivID));
        connectionEndpointIDs.set(srcDivID, dstDivID);
        //console.log('HEAP->HEAP', srcDivID, dstDivID);

        assert(!heapConnectionEndpointIDs.has(srcDivID));
        heapConnectionEndpointIDs.set(srcDivID, dstDivID);
      }

      return; // early return!
    }


    var heapObjID = myViz.generateID('heap_object_' + objID);


    // wrap ALL compound objects in a heapObject div so that jsPlumb
    // connectors can point to it:
    d3DomElement.append('<div class="heapObject" id="' + heapObjID + '"></div>');
    d3DomElement = myViz.domRoot.find('#' + heapObjID);

    renderedObjectIDs.set(objID, 1);

    var obj = curEntry.heap[objID];
    assert($.isArray(obj));

    // prepend the type label with a memory address label
    var typeLabelPrefix = '';
    if (myViz.textualMemoryLabels) {
      typeLabelPrefix = 'id' + objID + ':';
    }

    if (obj[0] == 'LIST' || obj[0] == 'TUPLE' || obj[0] == 'SET' || obj[0] == 'DICT') {
      var label = obj[0].toLowerCase();

      assert(obj.length >= 1);
      if (obj.length == 1) {
        d3DomElement.append('<div class="typeLabel">' + typeLabelPrefix + 'empty ' + label + '</div>');
      }
      else {
        d3DomElement.append('<div class="typeLabel">' + typeLabelPrefix + label + '</div>');
        d3DomElement.append('<table class="' + label + 'Tbl"></table>');
        var tbl = d3DomElement.children('table');

        if (obj[0] == 'LIST' || obj[0] == 'TUPLE') {
          tbl.append('<tr></tr><tr></tr>');
          var headerTr = tbl.find('tr:first');
          var contentTr = tbl.find('tr:last');
          $.each(obj, function(ind, val) {
            if (ind < 1) return; // skip type tag and ID entry

            // add a new column and then pass in that newly-added column
            // as d3DomElement to the recursive call to child:
            headerTr.append('<td class="' + label + 'Header"></td>');
            headerTr.find('td:last').append(ind - 1);

            contentTr.append('<td class="'+ label + 'Elt"></td>');
            renderNestedObject(val, contentTr.find('td:last'));
          });
        }
        else if (obj[0] == 'SET') {
          // create an R x C matrix:
          var numElts = obj.length - 1;

          // gives roughly a 3x5 rectangular ratio, square is too, err,
          // 'square' and boring
          var numRows = Math.round(Math.sqrt(numElts));
          if (numRows > 3) {
            numRows -= 1;
          }

          var numCols = Math.round(numElts / numRows);
          // round up if not a perfect multiple:
          if (numElts % numRows) {
            numCols += 1;
          }

          jQuery.each(obj, function(ind, val) {
            if (ind < 1) return; // skip 'SET' tag

            if (((ind - 1) % numCols) == 0) {
              tbl.append('<tr></tr>');
            }

            var curTr = tbl.find('tr:last');
            curTr.append('<td class="setElt"></td>');
            renderNestedObject(val, curTr.find('td:last'));
          });
        }
        else if (obj[0] == 'DICT') {
          $.each(obj, function(ind, kvPair) {
            if (ind < 1) return; // skip 'DICT' tag

            tbl.append('<tr class="dictEntry"><td class="dictKey"></td><td class="dictVal"></td></tr>');
            var newRow = tbl.find('tr:last');
            var keyTd = newRow.find('td:first');
            var valTd = newRow.find('td:last');

            var key = kvPair[0];
            var val = kvPair[1];

            renderNestedObject(key, keyTd);
            renderNestedObject(val, valTd);
          });
        }
      }
    }
    else if (obj[0] == 'INSTANCE' || obj[0] == 'CLASS') {
      var isInstance = (obj[0] == 'INSTANCE');
      var headerLength = isInstance ? 2 : 3;

      assert(obj.length >= headerLength);

      if (isInstance) {
        d3DomElement.append('<div class="typeLabel">' + typeLabelPrefix + obj[1] + ' instance</div>');
      }
      else {
        var superclassStr = '';
        if (obj[2].length > 0) {
          superclassStr += ('[extends ' + obj[2].join(', ') + '] ');
        }
        d3DomElement.append('<div class="typeLabel">' + typeLabelPrefix + obj[1] + ' class ' + superclassStr + '</div>');
      }

      // right now, let's NOT display class members, since that clutters
      // up the display too much. in the future, consider displaying
      // class members in a pop-up pane on mouseover or mouseclick
      // actually nix what i just said above ...
      //if (!isInstance) return;

      if (obj.length > headerLength) {
        var lab = isInstance ? 'inst' : 'class';
        d3DomElement.append('<table class="' + lab + 'Tbl"></table>');

        var tbl = d3DomElement.children('table');

        $.each(obj, function(ind, kvPair) {
          if (ind < headerLength) return; // skip header tags

          tbl.append('<tr class="' + lab + 'Entry"><td class="' + lab + 'Key"></td><td class="' + lab + 'Val"></td></tr>');

          var newRow = tbl.find('tr:last');
          var keyTd = newRow.find('td:first');
          var valTd = newRow.find('td:last');

          // the keys should always be strings, so render them directly (and without quotes):
          // (actually this isn't the case when strings are rendered on the heap)
          if (typeof kvPair[0] == "string") {
            // common case ...
            var attrnameStr = htmlspecialchars(kvPair[0]);
            keyTd.append('<span class="keyObj">' + attrnameStr + '</span>');
          }
          else {
            // when strings are rendered as heap objects ...
            renderNestedObject(kvPair[0], keyTd);
          }

          // values can be arbitrary objects, so recurse:
          renderNestedObject(kvPair[1], valTd);
        });
      }
    }
    else if (obj[0] == 'INSTANCE_PPRINT') {
      d3DomElement.append('<div class="typeLabel">' + typeLabelPrefix + obj[1] + ' instance</div>');

      strRepr = htmlspecialchars(obj[2]); // escape strings!
      d3DomElement.append('<table class="customObjTbl"><tr><td class="customObjElt">' + strRepr + '</td></tr></table>');
    }
    else if (obj[0] == 'FUNCTION') {
      assert(obj.length == 3);

      // pretty-print lambdas and display other weird characters:
      var funcName = htmlspecialchars(obj[1]).replace('&lt;lambda&gt;', '\u03bb');
      var parentFrameID = obj[2]; // optional

      d3DomElement.append('<div class="typeLabel">' + typeLabelPrefix + 'function</div>');

      if (parentFrameID) {
        d3DomElement.append('<div class="funcObj">' + funcName + ' [parent=f'+ parentFrameID + ']</div>');
      }
      else {
        d3DomElement.append('<div class="funcObj">' + funcName + '</div>');
      }
    }
    else if (obj[0] == 'HEAP_PRIMITIVE') {
      assert(obj.length == 3);

      var typeName = obj[1];
      var primitiveVal = obj[2];

      // add a bit of padding to heap primitives, for aesthetics
      d3DomElement.append('<div class="heapPrimitive"></div>');
      d3DomElement.find('div.heapPrimitive').append('<div class="typeLabel">' + typeLabelPrefix + typeName + '</div>');
      renderPrimitiveObject(primitiveVal, d3DomElement.find('div.heapPrimitive'));
    }
    else {
      // render custom data type
      assert(obj.length == 2);

      var typeName = obj[0];
      var strRepr = obj[1];

      strRepr = htmlspecialchars(strRepr); // escape strings!

      d3DomElement.append('<div class="typeLabel">' + typeLabelPrefix + typeName + '</div>');
      d3DomElement.append('<table class="customObjTbl"><tr><td class="customObjElt">' + strRepr + '</td></tr></table>');
    }
  }


  // Render globals and then stack frames using d3:


  // TODO: this sometimes seems buggy on Safari, so nix it for now:
  function highlightAliasedConnectors(d, i) {
    // if this row contains a stack pointer, then highlight its arrow and
    // ALL aliases that also point to the same heap object
    var stackPtrId = $(this).find('div.stack_pointer').attr('id');
    if (stackPtrId) {
      var foundTargetId = null;
      myViz.jsPlumbInstance.select({source: stackPtrId}).each(function(c) {foundTargetId = c.targetId;});

      // use foundTargetId to highlight ALL ALIASES
      myViz.jsPlumbInstance.select().each(function(c) {
        if (c.targetId == foundTargetId) {
          c.setHover(true);
          $(c.canvas).css("z-index", 2000); // ... and move it to the VERY FRONT
        }
        else {
          c.setHover(false);
        }
      });
    }
  }

  function unhighlightAllConnectors(d, i) {
    myViz.jsPlumbInstance.select().each(function(c) {
      c.setHover(false);
    });
  }



  // TODO: coalesce code for rendering globals and stack frames,
  // since there's so much copy-and-paste grossness right now

  // render all global variables IN THE ORDER they were created by the program,
  // in order to ensure continuity:

  // Derive a list where each element contains varname
  // as long as value is NOT undefined.
  // (Sometimes entries in curEntry.ordered_globals are undefined,
  // so filter those out.)
  var realGlobalsLst = [];
  $.each(curEntry.ordered_globals, function(i, varname) {
    var val = curEntry.globals[varname];

    // (use '!==' to do an EXACT match against undefined)
    if (val !== undefined) { // might not be defined at this line, which is OKAY!
      realGlobalsLst.push(varname);
    }
  });

  var globalsID = myViz.generateID('globals');
  var globalTblID = myViz.generateID('global_table');

  var globalVarTable = myViz.domRootD3.select('#' + globalTblID)
    .selectAll('tr')
    .data(realGlobalsLst,
          function(d) {return d;} // use variable name as key
    );

  globalVarTable
    .enter()
    .append('tr')
    .attr('class', 'variableTr')
    .attr('id', function(d, i) {
        return myViz.generateID(varnameToCssID('global__' + d + '_tr')); // make globally unique (within the page)
    });


  var globalVarTableCells = globalVarTable
    .selectAll('td.stackFrameVar,td.stackFrameValue')
    .data(function(d, i){return [d, d];}) /* map varname down both columns */

  globalVarTableCells.enter()
    .append('td')
    .attr('class', function(d, i) {return (i == 0) ? 'stackFrameVar' : 'stackFrameValue';});

  // remember that the enter selection is added to the update
  // selection so that we can process it later ...

  // UPDATE
  globalVarTableCells
    .order() // VERY IMPORTANT to put in the order corresponding to data elements
    .each(function(varname, i) {
      if (i == 0) {
        $(this).html(varname);
      }
      else {
        // always delete and re-render the global var ...
        // NB: trying to cache and compare the old value using,
        // say -- $(this).attr('data-curvalue', valStringRepr) -- leads to
        // a mysterious and killer memory leak that I can't figure out yet
        $(this).empty();

        // make sure varname doesn't contain any weird
        // characters that are illegal for CSS ID's ...
        var varDivID = myViz.generateID('global__' + varnameToCssID(varname));

        // need to get rid of the old connector in preparation for rendering a new one:
        existingConnectionEndpointIDs.remove(varDivID);

        var val = curEntry.globals[varname];
        if (isPrimitiveType(val)) {
          renderPrimitiveObject(val, $(this));
        }
        else {
          var heapObjID = myViz.generateID('heap_object_' + getRefID(val));

          if (myViz.textualMemoryLabels) {
            var labelID = varDivID + '_text_label';
            $(this).append('<div class="objectIdLabel" id="' + labelID + '">id' + getRefID(val) + '</div>');
            $(this).find('div#' + labelID).hover(
              function() {
                myViz.jsPlumbInstance.connect({source: labelID, target: heapObjID,
                                               scope: 'varValuePointer'});
              },
              function() {
                myViz.jsPlumbInstance.select({source: labelID}).detach();
              });
          }
          else {
            // add a stub so that we can connect it with a connector later.
            // IE needs this div to be NON-EMPTY in order to properly
            // render jsPlumb endpoints, so that's why we add an "&nbsp;"!
            $(this).append('<div class="stack_pointer" id="' + varDivID + '">&nbsp;</div>');

            assert(!connectionEndpointIDs.has(varDivID));
            connectionEndpointIDs.set(varDivID, heapObjID);
            //console.log('STACK->HEAP', varDivID, heapObjID);
          }
        }
      }
    });



  globalVarTableCells.exit()
    .each(function(d, idx) {
      $(this).empty(); // crucial for garbage collecting jsPlumb connectors!
    })
    .remove();

  globalVarTable.exit()
    .each(function(d, i) {
      // detach all stack_pointer connectors for divs that are being removed
      $(this).find('.stack_pointer').each(function(i, sp) {
        existingConnectionEndpointIDs.remove($(sp).attr('id'));
      });

      $(this).empty(); // crucial for garbage collecting jsPlumb connectors!
    })
    .remove();


  // for aesthetics, hide globals if there aren't any globals to display
  if (curEntry.ordered_globals.length == 0) {
    this.domRoot.find('#' + globalsID).hide();
  }
  else {
    this.domRoot.find('#' + globalsID).show();
  }


  // holy cow, the d3 code for stack rendering is ABSOLUTELY NUTS!

  var stackDiv = myViz.domRootD3.select('#stack');

  // VERY IMPORTANT for selectAll selector to be SUPER specific here!
  var stackFrameDiv = stackDiv.selectAll('div.stackFrame,div.zombieStackFrame')
    .data(curEntry.stack_to_render, function(frame) {
      // VERY VERY VERY IMPORTANT for properly handling closures and nested functions
      // (see the backend code for more details)
      return frame.unique_hash;
    });

  var sfdEnter = stackFrameDiv.enter()
    .append('div')
    .attr('class', function(d, i) {return d.is_zombie ? 'zombieStackFrame' : 'stackFrame';})
    .attr('id', function(d, i) {return d.is_zombie ? myViz.generateID("zombie_stack" + i)
                                                   : myViz.generateID("stack" + i);
    })
    // HTML5 custom data attributes
    .attr('data-frame_id', function(frame, i) {return frame.frame_id;})
    .attr('data-parent_frame_id', function(frame, i) {
      return (frame.parent_frame_id_list.length > 0) ? frame.parent_frame_id_list[0] : null;
    })
    .each(function(frame, i) {
      if (!myViz.drawParentPointers) {
        return;
      }
      // only run if myViz.drawParentPointers is true ...

      var my_CSS_id = $(this).attr('id');

      //console.log(my_CSS_id, 'ENTER');

      // render a parent pointer whose SOURCE node is this frame
      // i.e., connect this frame to p, where this.parent_frame_id == p.frame_id
      // (if this.parent_frame_id is null, then p is the global frame)
      if (frame.parent_frame_id_list.length > 0) {
        var parent_frame_id = frame.parent_frame_id_list[0];
        // tricky turkey!
        // ok this hack just HAPPENS to work by luck ... usually there will only be ONE frame
        // that matches this selector, but sometimes multiple frames match, in which case the
        // FINAL frame wins out (since parentPointerConnectionEndpointIDs is a map where each
        // key can be mapped to only ONE value). it so happens that the final frame winning
        // out looks "desirable" for some of the closure test cases that I've tried. but
        // this code is quite brittle :(
        myViz.domRoot.find('div#stack [data-frame_id=' + parent_frame_id + ']').each(function(i, e) {
          var parent_CSS_id = $(this).attr('id');
          //console.log('connect', my_CSS_id, parent_CSS_id);
          parentPointerConnectionEndpointIDs.set(my_CSS_id, parent_CSS_id);
        });
      }
      else {
        // render a parent pointer to the global frame
        //console.log('connect', my_CSS_id, globalsID);
        // only do this if there are actually some global variables to display ...
        if (curEntry.ordered_globals.length > 0) {
          parentPointerConnectionEndpointIDs.set(my_CSS_id, globalsID);
        }
      }

      // tricky turkey: render parent pointers whose TARGET node is this frame.
      // i.e., for all frames f such that f.parent_frame_id == my_frame_id,
      // connect f to this frame.
      // (make sure not to confuse frame IDs with CSS IDs!!!)
      var my_frame_id = frame.frame_id;
      myViz.domRoot.find('div#stack [data-parent_frame_id=' + my_frame_id + ']').each(function(i, e) {
        var child_CSS_id = $(this).attr('id');
        //console.log('connect', child_CSS_id, my_CSS_id);
        parentPointerConnectionEndpointIDs.set(child_CSS_id, my_CSS_id);
      });
    });

  sfdEnter
    .append('div')
    .attr('class', 'stackFrameHeader')
    .html(function(frame, i) {

      // pretty-print lambdas and display other weird characters
      // (might contain '<' or '>' for weird names like <genexpr>)
      var funcName = htmlspecialchars(frame.func_name).replace('&lt;lambda&gt;', '\u03bb')
            .replace('\n', '<br/>');

      var headerLabel = funcName;

      // only display if you're someone's parent
      if (frame.is_parent) {
        headerLabel = 'f' + frame.frame_id + ': ' + headerLabel;
      }

      // optional (btw, this isn't a CSS id)
      if (frame.parent_frame_id_list.length > 0) {
        var parentFrameID = frame.parent_frame_id_list[0];
        headerLabel = headerLabel + ' [parent=f' + parentFrameID + ']';
      }

      return headerLabel;
    });

  sfdEnter
    .append('table')
    .attr('class', 'stackFrameVarTable');


  var stackVarTable = stackFrameDiv
    .order() // VERY IMPORTANT to put in the order corresponding to data elements
    .select('table').selectAll('tr')
    .data(function(frame) {
        // each list element contains a reference to the entire frame
        // object as well as the variable name
        // TODO: look into whether we can use d3 parent nodes to avoid
        // this hack ... http://bost.ocks.org/mike/nest/
        return frame.ordered_varnames.map(function(varname) {return {varname:varname, frame:frame};});
      },
      function(d) {return d.varname;} // use variable name as key
    );

  stackVarTable
    .enter()
    .append('tr')
    .attr('class', 'variableTr')
    .attr('id', function(d, i) {
        return myViz.generateID(varnameToCssID(d.frame.unique_hash + '__' + d.varname + '_tr')); // make globally unique (within the page)
    });


  var stackVarTableCells = stackVarTable
    .selectAll('td.stackFrameVar,td.stackFrameValue')
    .data(function(d, i) {return [d, d] /* map identical data down both columns */;});

  stackVarTableCells.enter()
    .append('td')
    .attr('class', function(d, i) {return (i == 0) ? 'stackFrameVar' : 'stackFrameValue';});

  stackVarTableCells
    .order() // VERY IMPORTANT to put in the order corresponding to data elements
    .each(function(d, i) {
      var varname = d.varname;
      var frame = d.frame;

      if (i == 0) {
        if (varname == '__return__')
          $(this).html('<span class="retval">Return<br/>value</span>');
        else
          $(this).html(varname);
      }
      else {
        // always delete and re-render the stack var ...
        // NB: trying to cache and compare the old value using,
        // say -- $(this).attr('data-curvalue', valStringRepr) -- leads to
        // a mysterious and killer memory leak that I can't figure out yet
        $(this).empty();

        // make sure varname and frame.unique_hash don't contain any weird
        // characters that are illegal for CSS ID's ...
        var varDivID = myViz.generateID(varnameToCssID(frame.unique_hash + '__' + varname));

        // need to get rid of the old connector in preparation for rendering a new one:
        existingConnectionEndpointIDs.remove(varDivID);

        var val = frame.encoded_locals[varname];
        if (isPrimitiveType(val)) {
          renderPrimitiveObject(val, $(this));
        }
        else {
          var heapObjID = myViz.generateID('heap_object_' + getRefID(val));
          if (myViz.textualMemoryLabels) {
            var labelID = varDivID + '_text_label';
            $(this).append('<div class="objectIdLabel" id="' + labelID + '">id' + getRefID(val) + '</div>');
            $(this).find('div#' + labelID).hover(
              function() {
                myViz.jsPlumbInstance.connect({source: labelID, target: heapObjID,
                                               scope: 'varValuePointer'});
              },
              function() {
                myViz.jsPlumbInstance.select({source: labelID}).detach();
              });
          }
          else {
            // add a stub so that we can connect it with a connector later.
            // IE needs this div to be NON-EMPTY in order to properly
            // render jsPlumb endpoints, so that's why we add an "&nbsp;"!
            $(this).append('<div class="stack_pointer" id="' + varDivID + '">&nbsp;</div>');

            assert(!connectionEndpointIDs.has(varDivID));
            connectionEndpointIDs.set(varDivID, heapObjID);
            //console.log('STACK->HEAP', varDivID, heapObjID);
          }
        }
      }
    });


  stackVarTableCells.exit()
    .each(function(d, idx) {
      $(this).empty(); // crucial for garbage collecting jsPlumb connectors!
    })
   .remove();

  stackVarTable.exit()
    .each(function(d, i) {
      $(this).find('.stack_pointer').each(function(i, sp) {
        // detach all stack_pointer connectors for divs that are being removed
        existingConnectionEndpointIDs.remove($(sp).attr('id'));
      });

      $(this).empty(); // crucial for garbage collecting jsPlumb connectors!
    })
    .remove();

  stackFrameDiv.exit()
    .each(function(frame, i) {
      $(this).find('.stack_pointer').each(function(i, sp) {
        // detach all stack_pointer connectors for divs that are being removed
        existingConnectionEndpointIDs.remove($(sp).attr('id'));
      });

      var my_CSS_id = $(this).attr('id');

      //console.log(my_CSS_id, 'EXIT');

      // Remove all pointers where either the source or destination end is my_CSS_id
      existingParentPointerConnectionEndpointIDs.forEach(function(k, v) {
        if (k == my_CSS_id || v == my_CSS_id) {
          //console.log('remove EPP', k, v);
          existingParentPointerConnectionEndpointIDs.remove(k);
        }
      });

      $(this).empty(); // crucial for garbage collecting jsPlumb connectors!
    })
    .remove();


  // NB: ugh, I'm not very happy about this hack, but it seems necessary
  // for embedding within sophisticated webpages such as IPython Notebook

  // delete all connectors. do this AS LATE AS POSSIBLE so that
  // (presumably) the calls to $(this).empty() earlier in this function
  // will properly garbage collect the connectors
  //
  // WARNING: for environment parent pointers, garbage collection doesn't seem to
  // be working as intended :(
  //
  // I suspect that this is due to the fact that parent pointers are SIBLINGS
  // of stackFrame divs and not children, so when stackFrame divs get destroyed,
  // their associated parent pointers do NOT.)
  myViz.jsPlumbInstance.reset();


  // use jsPlumb scopes to keep the different kinds of pointers separated
  function renderVarValueConnector(varID, valueID) {
    myViz.jsPlumbInstance.connect({source: varID, target: valueID, scope: 'varValuePointer'});
  }


  var totalParentPointersRendered = 0;

  function renderParentPointerConnector(srcID, dstID) {
    // SUPER-DUPER-ugly hack since I can't figure out a cleaner solution for now:
    // if either srcID or dstID no longer exists, then SKIP rendering ...
    if ((myViz.domRoot.find('#' + srcID).length == 0) ||
        (myViz.domRoot.find('#' + dstID).length == 0)) {
      return;
    }

    //console.log('renderParentPointerConnector:', srcID, dstID);

    myViz.jsPlumbInstance.connect({source: srcID, target: dstID,
                                   anchors: ["LeftMiddle", "LeftMiddle"],

                                   // 'horizontally offset' the parent pointers up so that they don't look as ugly ...
                                   //connector: ["Flowchart", { stub: 9 + (6 * (totalParentPointersRendered + 1)) }],

                                   // actually let's try a bezier curve ...
                                   connector: [ "Bezier", { curviness: 45 }],

                                   endpoint: ["Dot", {radius: 4}],
                                   //hoverPaintStyle: {lineWidth: 1, strokeStyle: connectorInactiveColor}, // no hover colors
                                   scope: 'frameParentPointer'});
    totalParentPointersRendered++;
  }

  if (!myViz.textualMemoryLabels) {
    // re-render existing connectors and then ...
    existingConnectionEndpointIDs.forEach(renderVarValueConnector);
    // add all the NEW connectors that have arisen in this call to renderDataStructures
    connectionEndpointIDs.forEach(renderVarValueConnector);
  }
  // do the same for environment parent pointers
  if (myViz.drawParentPointers) {
    existingParentPointerConnectionEndpointIDs.forEach(renderParentPointerConnector);
    parentPointerConnectionEndpointIDs.forEach(renderParentPointerConnector);
  }

  /*
  myViz.jsPlumbInstance.select().each(function(c) {
    console.log('CONN:', c.sourceId, c.targetId);
  });
  */
  //console.log('---', myViz.jsPlumbInstance.select().length, '---');


  function highlight_frame(frameID) {
    myViz.jsPlumbInstance.select().each(function(c) {
      // this is VERY VERY fragile code, since it assumes that going up
      // FOUR layers of parent() calls will get you from the source end
      // of the connector to the enclosing stack frame
      var stackFrameDiv = c.source.parent().parent().parent().parent();

      // if this connector starts in the selected stack frame ...
      if (stackFrameDiv.attr('id') == frameID) {
        // then HIGHLIGHT IT!
        c.setPaintStyle({lineWidth:1, strokeStyle: connectorBaseColor});
        c.endpoints[0].setPaintStyle({fillStyle: connectorBaseColor});
        //c.endpoints[1].setVisible(false, true, true); // JUST set right endpoint to be invisible

        $(c.canvas).css("z-index", 1000); // ... and move it to the VERY FRONT
      }
      // for heap->heap connectors
      else if (heapConnectionEndpointIDs.has(c.endpoints[0].elementId)) {
        // NOP since it's already the color and style we set by default
      }
      else {
        // else unhighlight it
        c.setPaintStyle({lineWidth:1, strokeStyle: connectorInactiveColor});
        c.endpoints[0].setPaintStyle({fillStyle: connectorInactiveColor});
        //c.endpoints[1].setVisible(false, true, true); // JUST set right endpoint to be invisible

        $(c.canvas).css("z-index", 0);
      }
    });


    // clear everything, then just activate this one ...
    myViz.domRoot.find(".stackFrame").removeClass("highlightedStackFrame");
    myViz.domRoot.find('#' + frameID).addClass("highlightedStackFrame");
  }


  // highlight the top-most non-zombie stack frame or, if not available, globals
  var frame_already_highlighted = false;
  $.each(curEntry.stack_to_render, function(i, e) {
    if (e.is_highlighted) {
      highlight_frame(myViz.generateID('stack' + i));
      frame_already_highlighted = true;
    }
  });

  if (!frame_already_highlighted) {
    highlight_frame(myViz.generateID('globals'));
  }

}



ExecutionVisualizer.prototype.redrawConnectors = function() {
  this.jsPlumbInstance.repaintEverything();
}


// Utilities


/* colors - see pytutor.css for more colors */

var highlightedLineColor = '#e4faeb';
var highlightedLineBorderColor = '#005583';

var highlightedLineLighterColor = '#e8fff0';

var funcCallLineColor = '#a2eebd';

var brightRed = '#e93f34';

var connectorBaseColor = '#005583';
var connectorHighlightColor = brightRed;
var connectorInactiveColor = '#cccccc';

var errorColor = brightRed;

var breakpointColor = brightRed;
var hoverBreakpointColor = connectorBaseColor;


// Unicode arrow types: '\u21d2', '\u21f0', '\u2907'
var darkArrowColor = brightRed;
var lightArrowColor = '#c9e6ca';


function assert(cond) {
  if (!cond) {
    alert("Assertion Failure (see console log for backtrace)");
    throw 'Assertion Failure';
  }
}

// taken from http://www.toao.net/32-my-htmlspecialchars-function-for-javascript
function htmlspecialchars(str) {
  if (typeof(str) == "string") {
    str = str.replace(/&/g, "&amp;"); /* must do &amp; first */

    // ignore these for now ...
    //str = str.replace(/"/g, "&quot;");
    //str = str.replace(/'/g, "&#039;");

    str = str.replace(/</g, "&lt;");
    str = str.replace(/>/g, "&gt;");

    // replace spaces:
    str = str.replace(/ /g, "&nbsp;");

    // replace tab as four spaces:
    str = str.replace(/\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;");
  }
  return str;
}


// same as htmlspecialchars except don't worry about expanding spaces or
// tabs since we want proper word wrapping in divs.
function htmlsanitize(str) {
  if (typeof(str) == "string") {
    str = str.replace(/&/g, "&amp;"); /* must do &amp; first */

    str = str.replace(/</g, "&lt;");
    str = str.replace(/>/g, "&gt;");
  }
  return str;
}


String.prototype.rtrim = function() {
  return this.replace(/\s*$/g, "");
}


// make sure varname doesn't contain any weird
// characters that are illegal for CSS ID's ...
//
// I know for a fact that iterator tmp variables named '_[1]'
// are NOT legal names for CSS ID's.
// I also threw in '{', '}', '(', ')', '<', '>' as illegal characters.
//
// also some variable names are like '.0' (for generator expressions),
// and '.' seems to be illegal.
// TODO: what other characters are illegal???
var lbRE = new RegExp('\\[|{|\\(|<', 'g');
var rbRE = new RegExp('\\]|}|\\)|>', 'g');
function varnameToCssID(varname) {
  return varname.replace(lbRE, 'LeftB_').replace(rbRE, '_RightB').replace('.', '_DOT_');
}


// compare two JSON-encoded compound objects for structural equivalence:
function structurallyEquivalent(obj1, obj2) {
  // punt if either isn't a compound type
  if (isPrimitiveType(obj1) || isPrimitiveType(obj2)) {
    return false;
  }

  // must be the same compound type
  if (obj1[0] != obj2[0]) {
    return false;
  }

  // must have the same number of elements or fields
  if (obj1.length != obj2.length) {
    return false;
  }

  // for a list or tuple, same size (e.g., a cons cell is a list/tuple of size 2)
  if (obj1[0] == 'LIST' || obj1[0] == 'TUPLE') {
    return true;
  }
  else {
    var startingInd = -1;

    if (obj1[0] == 'DICT') {
      startingInd = 2;
    }
    else if (obj1[0] == 'INSTANCE') {
      startingInd = 3;
    }
    else {
      return false; // punt on all other types
    }

    var obj1fields = d3.map();

    // for a dict or object instance, same names of fields (ordering doesn't matter)
    for (var i = startingInd; i < obj1.length; i++) {
      obj1fields.set(obj1[i][0], 1); // use as a set
    }

    for (var i = startingInd; i < obj2.length; i++) {
      if (!obj1fields.has(obj2[i][0])) {
        return false;
      }
    }

    return true;
  }
}


function isPrimitiveType(obj) {
  var typ = typeof obj;
  return ((obj == null) || (typ != "object"));
}

function getRefID(obj) {
  assert(obj[0] == 'REF');
  return obj[1];
}


// Annotation bubbles

var qtipShared = {
  show: {
    ready: true, // show on document.ready instead of on mouseenter
    delay: 0,
    event: null,
    effect: function() {$(this).show();}, // don't do any fancy fading because it screws up with scrolling
  },
  hide: {
    fixed: true,
    event: null,
    effect: function() {$(this).hide();}, // don't do any fancy fading because it screws up with scrolling
  },
  style: {
    classes: 'ui-tooltip-pgbootstrap', // my own customized version of the bootstrap style
  },
};


// a speech bubble annotation to attach to:
//   'codeline' - a line of code
//   'frame'    - a stack frame
//   'variable' - a variable within a stack frame
//   'object'   - an object on the heap
// (as determined by the 'type' param)
//
// domID is the ID of the element to attach to (without the leading '#' sign)
function AnnotationBubble(parentViz, type, domID) {
  this.parentViz = parentViz;

  this.domID = domID;
  this.hashID = '#' + domID;

  this.type = type;

  if (type == 'codeline') {
    this.my = 'left center';
    this.at = 'right center';
  }
  else if (type == 'frame') {
    this.my = 'right center';
    this.at = 'left center';
  }
  else if (type == 'variable') {
    this.my = 'right center';
    this.at = 'left center';
  }
  else if (type == 'object') {
    this.my = 'bottom left';
    this.at = 'top center';
  }
  else {
    assert(false);
  }

  // possible states:
  //   'invisible'
  //   'edit'
  //   'view'
  //   'minimized'
  //   'stub'
  this.state = 'invisible';

  this.text = ''; // the actual contents of the annotation bubble

  this.qtipHidden = false; // is there a qtip object present but hidden? (TODO: kinda confusing)
}

AnnotationBubble.prototype.showStub = function() {
  assert(this.state == 'invisible' || this.state == 'edit');
  assert(this.text == '');

  var myBubble = this; // to avoid name clashes with 'this' in inner scopes

  // destroy then create a new tip:
  this.destroyQTip();
  $(this.hashID).qtip($.extend({}, qtipShared, {
    content: ' ',
    id: this.domID,
    position: {
      my: this.my,
      at: this.at,
      adjust: {
        x: (myBubble.type == 'codeline' ? -6 : 0), // shift codeline tips over a bit for aesthetics
      },
      effect: null, // disable all cutesy animations
    },
    style: {
      classes: 'ui-tooltip-pgbootstrap ui-tooltip-pgbootstrap-stub'
    }
  }));


  $(this.qTipID())
    .unbind('click') // unbind all old handlers
    .click(function() {
      myBubble.showEditor();
    });

  this.state = 'stub';
}

AnnotationBubble.prototype.showEditor = function() {
  assert(this.state == 'stub' || this.state == 'view' || this.state == 'minimized');

  var myBubble = this; // to avoid name clashes with 'this' in inner scopes

  var ta = '<textarea class="bubbleInputText">' + this.text + '</textarea>';

  // destroy then create a new tip:
  this.destroyQTip();
  $(this.hashID).qtip($.extend({}, qtipShared, {
    content: ta,
    id: this.domID,
    position: {
      my: this.my,
      at: this.at,
      adjust: {
        x: (myBubble.type == 'codeline' ? -6 : 0), // shift codeline tips over a bit for aesthetics
      },
      effect: null, // disable all cutesy animations
    }
  }));

  
  $(this.qTipContentID()).find('textarea.bubbleInputText')
    // set handler when the textarea loses focus
    .blur(function() {
      myBubble.text = $(this).val().trim(); // strip all leading and trailing spaces

      if (myBubble.text) {
        myBubble.showViewer();
      }
      else {
        myBubble.showStub();
      }
    })
    .focus(); // grab focus so that the user can start typing right away!

  this.state = 'edit';
}


AnnotationBubble.prototype.bindViewerClickHandler = function() {
  var myBubble = this;

  $(this.qTipID())
    .unbind('click') // unbind all old handlers
    .click(function() {
      if (myBubble.parentViz.editAnnotationMode) {
        myBubble.showEditor();
      }
      else {
        myBubble.minimizeViewer();
      }
    });
}

AnnotationBubble.prototype.showViewer = function() {
  assert(this.state == 'edit' || this.state == 'invisible');
  assert(this.text); // must be non-empty!

  var myBubble = this;
  // destroy then create a new tip:
  this.destroyQTip();
  $(this.hashID).qtip($.extend({}, qtipShared, {
    content: htmlsanitize(this.text), // help prevent HTML/JS injection attacks
    id: this.domID,
    position: {
      my: this.my,
      at: this.at,
      adjust: {
        x: (myBubble.type == 'codeline' ? -6 : 0), // shift codeline tips over a bit for aesthetics
      },
      effect: null, // disable all cutesy animations
    }
  }));

  this.bindViewerClickHandler();
  this.state = 'view';
}


AnnotationBubble.prototype.minimizeViewer = function() {
  assert(this.state == 'view');

  var myBubble = this;

  $(this.hashID).qtip('option', 'content.text', ' '); //hack to "minimize" its size

  $(this.qTipID())
    .unbind('click') // unbind all old handlers
    .click(function() {
      if (myBubble.parentViz.editAnnotationMode) {
        myBubble.showEditor();
      }
      else {
        myBubble.restoreViewer();
      }
    });

  this.state = 'minimized';
}

AnnotationBubble.prototype.restoreViewer = function() {
  assert(this.state == 'minimized');
  $(this.hashID).qtip('option', 'content.text', htmlsanitize(this.text)); // help prevent HTML/JS injection attacks
  this.bindViewerClickHandler();
  this.state = 'view';
}

// NB: actually DESTROYS the QTip object
AnnotationBubble.prototype.makeInvisible = function() {
  assert(this.state == 'stub' || this.state == 'edit');
  this.destroyQTip();
  this.state = 'invisible';
}


AnnotationBubble.prototype.destroyQTip = function() {
  $(this.hashID).qtip('destroy');
}

AnnotationBubble.prototype.qTipContentID = function() {
  return '#ui-tooltip-' + this.domID + '-content';
}

AnnotationBubble.prototype.qTipID = function() {
  return '#ui-tooltip-' + this.domID;
}


AnnotationBubble.prototype.enterEditMode = function() {
  assert(this.parentViz.editAnnotationMode);
  if (this.state == 'invisible') {
    this.showStub();

    if (this.type == 'codeline') {
      this.redrawCodelineBubble();
    }
  }
}

AnnotationBubble.prototype.enterViewMode = function() {
  assert(!this.parentViz.editAnnotationMode);
  if (this.state == 'stub') {
    this.makeInvisible();
  }
  else if (this.state == 'edit') {
    this.text = $(this.qTipContentID()).find('textarea.bubbleInputText').val().trim(); // strip all leading and trailing spaces

    if (this.text) {
      this.showViewer();

      if (this.type == 'codeline') {
        this.redrawCodelineBubble();
      }
    }
    else {
      this.makeInvisible();
    }
  }
  else if (this.state == 'invisible') {
    // this happens when, say, you first enter View Mode
    if (this.text) {
      this.showViewer();

      if (this.type == 'codeline') {
        this.redrawCodelineBubble();
      }
    }
  }
}

AnnotationBubble.prototype.preseedText = function(txt) {
  assert(this.state == 'invisible');
  this.text = txt;
}

AnnotationBubble.prototype.redrawCodelineBubble = function() {
  assert(this.type == 'codeline');

  if (isOutputLineVisibleForBubbles(this.domID)) {
    if (this.qtipHidden) {
      $(this.hashID).qtip('show');
    }
    else {
      $(this.hashID).qtip('reposition');
    }

    this.qtipHidden = false;
  }
  else {
    $(this.hashID).qtip('hide');
    this.qtipHidden = true;
  }
}

AnnotationBubble.prototype.redrawBubble = function() {
  $(this.hashID).qtip('reposition');
}


// NB: copy-and-paste from isOutputLineVisible with some minor tweaks
function isOutputLineVisibleForBubbles(lineDivID) {
  var pcod = $('#pyCodeOutputDiv');

  var lineNoTd = $('#' + lineDivID);
  var LO = lineNoTd.offset().top;

  var PO = pcod.offset().top;
  var ST = pcod.scrollTop();
  var H = pcod.height();

  // add a few pixels of fudge factor on the bottom end due to bottom scrollbar
  return (PO <= LO) && (LO < (PO + H - 25));
}


// popup question dialog code from Brad Miller

// inputId is the ID of the input element
// divId is the div that containsthe visualizer
// answer is a dotted form of an attribute that lives in the curEntry of the trace
// So if we want to ask for the value of a global variable we would say 'globals.a'
// this allows us do do curTrace[i].globals.a  But we do it in the loop below using the
// [] operator.
function traceQCheckMe(inputId, divId, answer) {
   var vis = $("#"+divId).data("vis")
   var i = vis.curInstr
   var curEntry = vis.curTrace[i+1];
   var ans = $('#'+inputId).val()
   var attrs = answer.split(".")
   var correctAns = curEntry;
   for (j in attrs) {
       correctAns = correctAns[attrs[j]]
   }
   feedbackElement = $("#" + divId + "_feedbacktext")
   if (ans.length > 0 && ans == correctAns) {
       feedbackElement.html('Correct')
   } else {
       feedbackElement.html(vis.curTrace[i].question.feedback)
   }

}

function closeModal(divId) {
    $.modal.close()
    $("#"+divId).data("vis").stepForward();
}
