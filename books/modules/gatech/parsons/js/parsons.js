(function($, _) { // wrap in anonymous function to not show some helper variables

   // regexp used for trimming
   var trimRegexp = /^\s*(.*?)\s*$/;
   var translations = {
     fi: {
       trash_label: 'Raahaa rivit ohjelmaasi tästä',
       solution_label: 'Muodosta ratkaisusi tähän',
       order: function() {
         return "Ohjelma sisältää vääriä palasia tai palasten järjestys on väärä. Tämä on mahdollista korjata siirtämällä, poistamalla tai vaihtamalla korostettuja palasia.";},
       lines_missing: function() {
         return "Ohjelmassasi on liian vähän palasia, jotta se toimisi oikein.";},
       no_matching: function(lineNro) {
         return "Korostettu palanen (" + lineNro + ") on sisennetty Pythonin kieliopin vastaisesti."; },
       block_structure: function(lineNro) {
         return "Korostettu palanen (" + lineNro + ") on sisennetty väärään koodilohkoon."; },
       unittest_error: function(errormsg) {
         return "<span class='msg'>Virhe ohjelman jäsentämisessä/suorituksessa</span><br/> <span class='errormsg'>" + errormsg + "</span>";
       },
       unittest_output_assertion: function(expected, actual) {
        return "Odotettu tulostus: <span class='expected output'>" + expected + "</span>" +
              "Ohjelmasi tulostus: <span class='actual output'>" + actual + "</span>";
       },
       unittest_assertion: function(expected, actual) {
        return "Odotettu arvo: <span class='expected'>" + expected + "</span><br>" +
              "Ohjelmasi antama arvo: <span class='actual'>" + actual + "</span>";
       },
       variabletest_assertion: function(varname, expected, actual) {
        return "Muuttujan " + varname + " odotettu arvo: <span class='expected'>" + expected + "</span> " +
              "Ohjelmasi antama arvo: <span class='actual'>" + actual + "</span>";
       }
     },
     en: {
       trash_label: 'Drag from here',
       solution_label: 'Construct your solution here',
       order: function() {
         return "Code fragments in your program are wrong, or in wrong order. This can be fixed by moving, removing, or replacing highlighted fragments.";},
       lines_missing: function() {
         return "Your program has too few code fragments.";},
       no_matching: function(lineNro) {
         return "Based on python syntax, the highlighted fragment (" + lineNro + ") is not correctly indented."; },
       block_structure: function(lineNro) { return "The highlighted fragment " + lineNro + " belongs to a wrong block (i.e. indentation)."; },
       unittest_error: function(errormsg) {
         return "<span class='msg'>Error in parsing/executing your program</span><br/> <span class='errormsg'>" + errormsg + "</span>";
       },
       unittest_output_assertion: function(expected, actual) {
        return "Expected output: <span class='expected output'>" + expected + "</span>" +
              "Output of your program: <span class='actual output'>" + actual + "</span>";
       },
       unittest_assertion: function(expected, actual) {
        return "Expected value: <span class='expected'>" + expected + "</span><br>" +
              "Actual value: <span class='actual'>" + actual + "</span>";
       },
       variabletest_assertion: function(varname, expected, actual) {
        return "Expected value of variable " + varname + ": <span class='expected'>" + expected + "</span><br>" +
              "Actual value: <span class='actual'>" + actual + "</span>";
       }
     }
   };

  // Different graders


  // Grader that will execute the code and check variable values after that
  // Expected and supported options:
  //  - vartests (required): array of variable test objects
  // Each variable test object can/must have the following properties:
  //  - initcode: code that will be prepended before the learner solution code
  //  - code: code that will be appended after the learner solution code
  //  - message (required): a textual description of the test, shown to learner
  // Properties specifying what is tested:
  //  - variables: an object with properties for each variable name to
  //                          be tested; the value of the property is the expected
  //                          value
  // or
  //  - variable: a variable name to be tested
  //  - expected: expected value of the variable after code execution
  var VariableCheckGrader = function(parson) {
    this.parson = parson;
  };
  // Executes the given code using Skulpt and returns an object with variable
  // values of the variables given in the variables array.
  // Possible errors will be in the _error property of the returned object.
  // Output of the code will be in _output property of the result.
  // Example: this._python_exec("x=0\ny=2\nprint x", ["x", "y"])
  //    will return object {"x": 0, "y": 2, "_output": "0"}
  VariableCheckGrader.prototype._python_exec = function(code, variables) {
      var output = "",
          mainmod,
          result = {'variables': {}},
          varname;
      // configure Skulpt
      Sk.execLimit = this.parson.options.exec_limit || 2500; // time limit for the code to run
      Sk.configure( { output: function(str) { output += str; },
          python3: this.parson.options.python3 || false
      } );
      try {
        mainmod = Sk.importMainWithBody("<stdin>", false, code);
      } catch (e) {
        return {"_output": output, "_error": "" + e};
      }
      for (var i = 0; i < variables.length; i++) {
        varname = variables[i];
        result.variables[varname] = mainmod.tp$getattr(varname);
      }
      result._output = output;
      return result;
  };
  VariableCheckGrader.prototype.formatVariableValue = function(varValue) {
    var varType = typeof varValue;
    if (varType === "undefined" || varValue === null) {
      return "None";
    } else if (varType === "string") { // show strings in quotes
      return '"' + varValue + '"';
    } else if (varType === "boolean") { // Python booleans with capital first letter
      return varValue?"True":"False";
    } else if ($.isArray(varValue)) { // JavaScript arrays
      return '[' + varValue.join(', ') + ']';
    } else if (varType === "object" && varValue.tp$name === "str") { // Python strings
      return '"' + varValue.v + '"';
    } else if (varType === "object" && varValue.tp$name === "list") { // Python lists
      return '[' + varValue.v.join(', ') + ']';
    } else {
      return varValue;
    }
  };
  // Fix or strip line numbers in the (error) message
  // Basically removes the number of lines in prependCode from the line number shown.
  VariableCheckGrader.prototype.stripLinenumberIfNeeded = function(msg, prependCode, studentCode) {
    var lineNbrRegexp = /.*on line ([0-9]+).*/;
    // function that fixes the line numbers in student feedback
    var match = msg.match(lineNbrRegexp);
    if (match) {
      var lineNo = parseInt(match[1], 10),
          lowerLimit = prependCode?
                          prependCode.split('\n').length
                          :0,
          upperLimit = lowerLimit + studentCode.split('\n').length - 1;
      // if error in prepended code or tests, remove the line number
      if (lineNo <= lowerLimit || lineNo > upperLimit) {
        return msg.replace(' on line ' + lineNo, '');
      } else if (lowerLimit > 0) {
        // if error in student code, make sure the line number matches student lines
        return msg.replace(' on line ' + lineNo, ' on line ' + (lineNo - lowerLimit));
      }
    }
    return msg;
  };
  VariableCheckGrader.prototype.grade = function() {
    var parson = this.parson,
        that = this,
        feedback = "",
        log_errors = [],
        all_passed = true;
    $.each(parson.options.vartests, function(index, testdata) {
      var $lines = $("#sortable li");
      var student_code = parson._codelinesAsString();
      var executableCode = (testdata.initcode || "") + "\n" + student_code + "\n" + (testdata.code || "");
      var variables, expectedVals;
      if ('variables' in testdata) {
        variables = _.keys(testdata.variables);
        expectedVals = testdata.variables;
      } else {
        variables = [testdata.variable];
        expectedVals = {};
        expectedVals[testdata.variable] = testdata.expected;
      }
      var res = that._python_exec(executableCode, variables);
      var testcaseFeedback = "",
          success = true,
          log_entry = {'code': testdata.code, 'msg': testdata.message},
          expected_value,
          actual_value;
      if ("_error" in res) {
        testcaseFeedback += parson.translations.unittest_error(that.stripLinenumberIfNeeded(res._error,
                                                                                      testdata.initcode,
                                                                                      student_code));
        success = false;
        log_entry.type = "error";
        log_entry.errormsg = res._error;
      } else {
        log_entry.type = "assertion";
        log_entry.variables = {};
        for (var j = 0; j < variables.length; j++) {
          var variable = variables[j];
          if (variable === "__output") { // checking output of the program
            expected_value = testdata.expected;
            actual_value = res._output;
            testcaseFeedback += parson.translations.unittest_output_assertion(expected_value, actual_value);
          } else {
            expected_value = that.formatVariableValue(expectedVals[variable]);
            actual_value = that.formatVariableValue(res.variables[variable].v);
            testcaseFeedback += parson.translations.variabletest_assertion(variable, expected_value, actual_value) + "<br/>";
          }
          log_entry.variables[variable] = {expected: expected_value, actual: actual_value};
          if (actual_value != expected_value) { // should we do a strict test??
            success = false;
          }
        }
      }
      all_passed = all_passed && success;
      log_entry.success = success;
      log_errors.push(log_entry);
      feedback += "<div class='testcase " + (success?"pass":"fail") +
                  "'><span class='msg'>" + testdata.message + "</span><br>" +
                  testcaseFeedback + "</div>";
    });
    return { html: feedback, "log_errors": log_errors, success: all_passed };
  };

  // Grader that will execute student code and Skulpt unittests
  var UnitTestGrader = function(parson) {
    this.parson = parson;
  };
  // copy the line number fixer from VariableCheckGrader
  UnitTestGrader.prototype.stripLinenumberIfNeeded = VariableCheckGrader.prototype.stripLinenumberIfNeeded;
  // do the grading
  UnitTestGrader.prototype.grade = function() {
    var success = true,
        parson = this.parson,
        unittests = parson.options.unittests,
        studentCode = parson._codelinesAsString(),
        feedbackHtml = "", // HTML to be returned as feedback
        result, mainmod;

    var executableCode = studentCode + "\n" + unittests;

    // if there is code to add before student code, add it
    if (parson.options.unittest_code_prepend) {
      executableCode = parson.options.unittest_code_prepend + "\n" + executableCode;
    }

    function builtinRead(x) {
      if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
          throw "File not found: '" + x + "'";
      return Sk.builtinFiles["files"][x];
    }

    // configuration for Skulpt
    Sk.execLimit = parson.options.exec_limit || 2500; // time limit for the code to run
    Sk.configure({output: console?console.log:function() {},
                  read: builtinRead,
                  python3: parson.options.python3 || false
                 });
    try {
      mainmod = Sk.importMainWithBody("<stdin>", false, executableCode);
      result = JSON.parse(mainmod.tp$getattr("_test_result").v);
    } catch (e) {
      result = [{status: "error", _error: e.toString() }];
    }

    // go through the results and generate HTML feedback
    for (var i = 0, l = result.length; i < l; i++) {
      var res = result[i];
      feedbackHtml += '<div class="testcase ' + res.status + '">';
      if (res.status === "error") { // errors in execution
        feedbackHtml += parson.translations.unittest_error(this.stripLinenumberIfNeeded(res._error,
                                                                    parson.options.unittest_code_prepend,
                                                                    studentCode));
        success = false;
      } else { // passed or failed tests
        feedbackHtml += '<span class="msg">' + this.stripLinenumberIfNeeded(res.feedback) + '</span><br />';
        feedbackHtml += 'Expected <span class="expected">' + res.expected +
                  '</span>' + res.test + '<span class="actual">' + res.actual +
                  '</span>';
        if (res.status === "fail") {
          success = false;
        }
      }
      feedbackHtml += '</div>';
    }

    return { html: feedbackHtml, result: result, success: success };
  };

  // The "original" grader for giving line based feedback.
  var LineBasedGrader = function(parson) {
    this.parson = parson;
  };
  LineBasedGrader.prototype.grade = function(elementId) {
    var parson = this.parson;
    var elemId = elementId || parson.options.sortableId;
    var student_code = parson.normalizeIndents(parson.getModifiedCode("#ul-" + elemId));
    var lines_to_check = Math.min(student_code.length, parson.model_solution.length);
    var errors = [], log_errors = [];
    var incorrectLines = [], lines = [];
    var id, line, i;
    var wrong_order = false;

    //remove distractors from lines and add all those to the set of misplaced lines
    for (i=0; i<student_code.length; i++) {
      id = parseInt(student_code[i].id.replace(parson.id_prefix, ""), 10);
      line = parson.getLineById(parson.id_prefix + id);
      if (line.distractor) {
        incorrectLines.push(id);
        wrong_order = true;
        $("#" + parson.id_prefix + id).addClass("incorrectPosition");
      } else {
        lines.push(id);
      }
    }

    var inv = LIS.best_lise_inverse(lines);
    _.each(inv, function(itemId) {
            $("#" + parson.id_prefix + itemId).addClass("incorrectPosition");
            incorrectLines.push(itemId);
          });
    if (inv.length > 0 || errors.length > 0) {
      wrong_order = true;
      log_errors.push({type: "incorrectPosition", lines: incorrectLines});
    }

    if (wrong_order) {
      errors.push(parson.translations.order());
    }

    // Always show this feedback
    if (parson.model_solution.length < student_code.length) {
      //$("#ul-" + elemId).addClass("incorrect");
      //errors.push("Too many lines in your solution.");
      log_errors.push({type: "tooManyLines", lines: student_code.length});
    } else if (parson.model_solution.length > student_code.length){
      $("#ul-" + elemId).addClass("incorrect");
      errors.push(parson.translations.lines_missing());
      log_errors.push({type: "tooFewLines", lines: student_code.length});
    }

    if (errors.length === 0) { // check indent if no other errors
      for (i = 0; i < lines_to_check; i++) {
        var code_line = student_code[i];
        var model_line = parson.model_solution[i];
        if (code_line.indent !== model_line.indent &&
             ((!parson.options.first_error_only) || errors.length === 0)) {
          $("#" + code_line.id).addClass("incorrectIndent");
          errors.push(parson.translations.block_structure(i+1));
          log_errors.push({type: "incorrectIndent", line: (i+1)});
        }
        if (code_line.code == model_line.code &&
             code_line.indent == model_line.indent &&
             errors.length === 0) {
          $("#" + code_line.id).addClass("correctPosition");
        }
      }
    }

    return {errors: errors, log_errors: log_errors, success: (errors.length === 0)};
  };


   var python_indents = [],
        spaces = "";
   for (var counter = 0; counter < 20; counter++) {
    python_indents[counter] = spaces;
    spaces += "  ";
   }

   var defaultToggleTypeHandlers = {
      boolean: ["True", "False"],
      compop: ["<", ">", "<=", ">=", "==", "!="],
      mathop: ["+", "-", "*", "/"],
      boolop: ["and", "or"],
      range: function($item) {
         var min = parseFloat($item.data("min") || "0", 10),
             max = parseFloat($item.data("max") || "10", 10),
             step = parseFloat($item.data("step") || "1", 10),
             opts = [],
             curr = min;
         while (curr <= max) {
            opts.push("" + curr);
            curr += step;
         }
         return opts;
      }
   };
   var addToggleableElements = function(widget) {
      // toggleable elements are only enabled for unit tests
      if (!widget.options.unittests && !widget.options.vartests) { return; }
      var handlers = $.extend(defaultToggleTypeHandlers, widget.options.toggleTypeHandlers),
          context = $("#" + widget.options.sortableId + ", #" + widget.options.trashId);
      $(".jsparson-toggle", context).each(function(index, item) {
         var type = $(item).data("type");
         if (!type) { return; }
         var handler = handlers[type],
             jspOptions;
         if ($.isFunction(handler)) {
            jspOptions = handler($(item));
         } else {
            jspOptions = handler;
         }
         if (jspOptions && $.isArray(jspOptions)) {
            $(item).attr("data-jsp-options", JSON.stringify(jspOptions));
         }
      });
      // register a click handler for all the toggleable elements (and unregister existing)
      context.off("click", ".jsparson-toggle").on("click", ".jsparson-toggle", function() {
         var $this = $(this),
             curVal = $this.text(),
             choices = $this.data("jsp-options"),
             newVal = choices[(choices.indexOf(curVal) + 1)%choices.length],
             $parent = $this.parent("li");
         // change the shown toggle element
         $this.text(newVal);
         // log the event
         widget.addLogEntry({type: "toggle", oldvalue: curVal, newvalue: newVal,
                           target: $parent[0].id,
                           toggleindex: $parent.find(".jsparson-toggle").index($this)});
      });
   };

   var ParsonsWidget = function(options) {
     this.modified_lines = [];
     this.extra_lines = [];
     this.model_solution = [];
     
     //To collect statistics, feedback should not be based on this
     this.user_actions = [];
     
     //State history for feedback purposes
     this.state_path = [];
     this.states = {};
     
     var defaults = {
       'incorrectSound': false,
       'x_indent': 50,
       'feedback_cb': false,
       'first_error_only': true,
       'max_wrong_lines': 10,
       'lang': 'en'
     };
     
     this.options = jQuery.extend({}, defaults, options);
     this.feedback_exists = false;
     this.id_prefix = options['sortableId'] + 'codeline';
     if (translations.hasOwnProperty(this.options.lang)) {
       this.translations = translations[this.options.lang];
     } else {
       this.translations = translations['en'];
     }

     // translate trash_label and solution_label
     if (!this.options.hasOwnProperty("trash_label")) {
         this.options.trash_label = this.translations.trash_label;
     }
     if (!this.options.hasOwnProperty("solution_label")) {
         this.options.solution_label = this.translations.solution_label;
     }
     this.FEEDBACK_STYLES = { 'correctPosition' : 'correctPosition',
                              'incorrectPosition' : 'incorrectPosition',
                              'correctIndent' : 'correctIndent',
                              'incorrectIndent' : 'incorrectIndent'};

    // initialize the grader
    if (typeof(this.options.unittests) !== "undefined") { /// unittests are specified
      this.grader = new UnitTestGrader(this);
    } else if (typeof(this.options.vartests) !== "undefined") { /// tests for variable values
      this.grader = new VariableCheckGrader(this);
    } else { // "traditional" parson feedback
      this.grader = new LineBasedGrader(this);
    }
   };
      
   //Public methods
   ParsonsWidget.prototype.parseLine = function(spacePrefixedLine) {
     return {
       code: spacePrefixedLine.replace(trimRegexp, "$1").replace(/\\n/g,"\n"),
       indent: spacePrefixedLine.length - spacePrefixedLine.replace(/^\s+/,"").length
     };
   };
   
   ParsonsWidget.prototype.parseCode = function(lines, max_distractors) {
     var distractors = [],
     indented = [],
     widgetData = [],
     lineObject,
     errors = [],
     that = this;
     $.each(lines, function(index, item) {
              if (item.search(/#distractor\s*$/) >= 0) {
                lineObject = {
                  code: item.replace(/#distractor\s*$/,"").replace(trimRegexp, "$1").replace(/\\n/,"\n"),
                  indent: -1,
                  distractor: true,
                  orig: index
                };
                if (lineObject.code.length > 0) {
                  distractors.push(lineObject);
                }
              } else {
                lineObject = that.parseLine(item);
                if (lineObject.code.length > 0) {
                  lineObject.distractor = false;
                  lineObject.orig = index;
                  indented.push(lineObject);
                }
              }
            });
     
     // Normalize indents and make sure indentation is valid
     var normalized = this.normalizeIndents(indented);
     
     $.each(normalized, function(index, item) {
              if (item.indent < 0) {
                errors.push(this.translations.no_matching(normalized.orig));
              }
              widgetData.push(item);
            });
     
     // Remove extra distractors
     var permutation = this.getRandomPermutation(distractors.length);
     var selected_distractors = [];
     for (var i = 0; i < max_distractors; i++) {
       selected_distractors.push(distractors[permutation[i]]);
       widgetData.push(distractors[permutation[i]]);
     }
     
     return {
       solution:  $.extend(true, [], normalized),
       distractors: $.extend(true, [], selected_distractors),
       widgetInitial: $.extend(true, [], widgetData),
       errors: errors};
   };

   ParsonsWidget.prototype.init = function(text) {
     var initial_structures = this.parseCode(text.split("\n"), this.options.max_wrong_lines);
     this.model_solution = initial_structures.solution;
     this.extra_lines = initial_structures.distractors;
     this.modified_lines = initial_structures.widgetInitial;
     this.alternatives = {};
     var that = this;

     $.each(this.modified_lines, function(index, item) {
              item.id = that.id_prefix + index;
              item.indent = 0;
              if (that.alternatives.hasOwnProperty(item.code)) {
                that.alternatives[item.code].push(index);
              } else {
                that.alternatives[item.code] = [index];
              }
     });

   };

   ParsonsWidget.prototype.getHash = function(searchString) {
     var ids = [];
     var hash = [];
     ids = $(searchString).sortable('toArray');
     for (var i = 0; i < ids.length; i++) {
       hash.push(ids[i].replace(this.id_prefix, "") + "_" + this.getLineById(ids[i]).indent);
     }
     //prefix with something to handle empty output situations
     if (hash.length === 0) {
       return "-";
     } else {
       return hash.join("-");
     }
   };
   
   ParsonsWidget.prototype.solutionHash = function() {
       return this.getHash("#ul-" + this.options.sortableId);
   };

   ParsonsWidget.prototype.trashHash = function() {
       return this.getHash("#ul-" + this.options.trashId);
   };

   ParsonsWidget.prototype.whatWeDidPreviously = function() {
     var hash = this.solutionHash();
     var previously = this.states[hash];
     if (!previously) { return undefined; }
     var visits = _.filter(this.state_path, function(state) {
                             return state == hash;
                           }).length - 1;
     var i, stepsToLast = 0, s,
        outputStepTypes = ['removeOutput', 'addOutput', 'moveOutput'];
     for (i = this.state_path.length - 2; i > 0; i--) {
       s = this.states[this.state_path[i]];
       if (s && outputStepTypes.indexOf(s.type) != -1) {
         stepsToLast++;
       }
       if (hash === this.state_path[i]) { break; }
     }
     return $.extend(false, {'visits': visits, stepsToLast: stepsToLast}, previously);
   };
   
  /**
    * Returns states of the toggles for logging purposes
    */
  ParsonsWidget.prototype._getToggleStates = function() {
    var context = $("#" + this.options.sortableId + ", #" + this.options.trashId),
        toggles = $(".jsparson-toggle", context),
        toggleStates = {};
    $("#" + this.options.sortableId + " .jsparson-toggle").each(function() {
      if (!toggleStates.output) {
        toggleStates.output = [];
      }
      toggleStates.output.push($(this).text());
    });
    if (this.options.trashId) {
      toggleStates.input = [];
      $("#" + this.options.trashId + " .jsparson-toggle").each(function() {
        toggleStates.input.push($(this).text());
      });
    }
    if ((toggleStates.output && toggleStates.output.length > 0) ||
                  (toggleStates.input && toggleStates.input.length > 0)) {
      return toggleStates;
    } else {
      return undefined;
    }
  };

   ParsonsWidget.prototype.addLogEntry = function(entry) {
     var state, previousState;
     var logData = {
       time: new Date(),
       output: this.solutionHash(),
       type: "action"
     };

     if (this.options.trashId) {
       logData.input = this.trashHash();
     }

     if (entry.target) {
       entry.target = entry.target.replace(this.id_prefix, "");
     }

     // add toggle states to log data if there are toggles
     var toggles = this._getToggleStates();
     if (toggles) {
       logData.toggleStates = toggles;
     }

     state = logData.output;

     jQuery.extend(logData, entry);
     this.user_actions.push(logData);

     //Updating the state history
     if(this.state_path.length > 0) {
       previousState = this.state_path[this.state_path.length - 1];
       this.states[previousState] = logData;
     }

     //Add new item to the state path only if new and previous states are not equal
     if (this.state_path[this.state_path.length - 1] !== state) {
       this.state_path.push(state);
     }
     // callback for reacting to actions
     if ($.isFunction(this.options.action_cb)) {
       this.options.action_cb.call(this, logData);
     }
   };

   /**
    * Update indentation of a line based on new coordinates
    * leftDiff horizontal difference from (before and after drag) in px
    ***/
   ParsonsWidget.prototype.updateIndent = function(leftDiff, id) {

     var code_line = this.getLineById(id);
     var new_indent = code_line.indent + Math.floor(leftDiff / this.options.x_indent);
     new_indent = Math.max(0, new_indent);
     code_line.indent = new_indent;

     return new_indent;
   };

   /**
    *
    * @param id
    * @return
    */
   ParsonsWidget.prototype.getLineById = function(id) {
     var index = -1;
     for (var i = 0; i < this.modified_lines.length; i++) {
       if (this.modified_lines[i].id == id) {
         index = i;
         break;
       }
     }
     return this.modified_lines[index];
   };

   /** Does not use the current object - only the argument */
   ParsonsWidget.prototype.normalizeIndents = function(lines) {

     var normalized = [];
     var new_line;
     var match_indent = function(index) {
       //return line index from the previous lines with matching indentation
       for (var i = index-1; i >= 0; i--) {
         if (lines[i].indent == lines[index].indent) {
           return normalized[i].indent;
         }
       }
       return -1;
     };
     for ( var i = 0; i < lines.length; i++ ) {
       //create shallow copy from the line object
       new_line = jQuery.extend({}, lines[i]);
       if (i === 0) {
         new_line.indent = 0;
         if (lines[i].indent !== 0) {
           new_line.indent = -1;
         }
       } else if (lines[i].indent == lines[i-1].indent) {
         new_line.indent = normalized[i-1].indent;
       } else if (lines[i].indent > lines[i-1].indent) {
         new_line.indent = normalized[i-1].indent + 1;
       } else {
         // indentation can be -1 if no matching indentation exists, i.e. IndentationError in Python
         new_line.indent = match_indent(i);
       }
       normalized[i] = new_line;
     }
     return normalized;
   };

   /**
    * Retrieve the code lines based on what is in the DOM
    *
    * TODO(petri) refactor to UI
    * */
   ParsonsWidget.prototype.getModifiedCode = function(search_string) {
     //ids of the the modified code
     var lines_to_return = [],
          that = this;
     $(search_string).find("li").each(function(index, item) {
       lines_to_return.push({id: $(item).attr("id"),
                      indent: parseInt($(item).css("margin-left"), 10)/that.options.x_indent});
     });
     return lines_to_return;
   };

   ParsonsWidget.prototype.hashToIDList = function(hash) {
     var lines = [];
     var lineValues;
     var lineObject;
     var h;

     if (hash === "-" || hash === "" || hash === null) {
       h = [];
     } else {
       h = hash.split("-");
     }
     
     var ids = [];
     for (var i = 0; i < h.length; i++) {
       lineValues = h[i].split("_");
       ids.push(this.modified_lines[lineValues[0]].id);
     }
     return ids;
   };

   ParsonsWidget.prototype.updateIndentsFromHash = function(hash) {
     var lines = [];
     var lineValues;
     var lineObject;
     var h;

     if (hash === "-" || hash === "" || hash === null) {
       h = [];
     } else {
       h = hash.split("-");
     }
     
     var ids = [];
     for (var i = 0; i < h.length; i++) {
         lineValues = h[i].split("_");
         this.modified_lines[lineValues[0]].indent = Number(lineValues[1]);
         this.updateHTMLIndent(this.modified_lines[lineValues[0]].id);
     }
     return ids;
   };


   /**
    * TODO(petri) refoctor to UI
    */
   ParsonsWidget.prototype.displayError = function(message) {
     if (this.options.incorrectSound && $.sound) {
       $.sound.play(this.options.incorrectSound);
     }
     alert(message);
   };

   ParsonsWidget.prototype.colorFeedback = function(elemId) {
     return new LineBasedGrader(this).grade(elemId);
   };


  ParsonsWidget.prototype._codelinesAsString = function() {
    var $lines = $("#" + this.options.sortableId + " li");
    var student_code = this.normalizeIndents(this.getModifiedCode("#ul-" + this.options.sortableId));
    var executableCode = "";
    $.each(student_code, function(index, item) {
      // split codeblocks on br elements
      var lines = $("#" + item.id).html().split(/<br\s*\/?>/);
      // go through all the lines
      for (var i = 0; i < lines.length; i++) {
        // add indents and get the text for the line (to remove the syntax highlight html elements)
        executableCode += python_indents[item.indent] + $("<span>" + lines[i] + "</span>").text() + "\n";
      }
    });
    return executableCode;
  };

   /**
    * @return
    * TODO(petri): Separate UI from here
    */
   ParsonsWidget.prototype.getFeedback = function() {
     this.feedback_exists = true;
     var fb = this.grader.grade();
     if (this.options.feedback_cb) {
       this.options.feedback_cb(fb); //TODO(petri): what is needed?
     }
     // if answer is correct, mark it in the UI
     if (fb.success) {
       $("#ul-" + this.options.sortableId).addClass("correct");
     }
     // log the feedback and return; based on the type of grader
     if ('html' in fb) { // unittest/vartests type feedback
       this.addLogEntry({type: "feedback", errors: fb.result, success: fb.success, toggles: this._getToggleStates()});
       return { feedback: fb.html, success: fb.success };
     } else {
       this.addLogEntry({type: "feedback", errors: fb.log_errors, success: fb.success});
       return fb.errors;
     }
   };

   ParsonsWidget.prototype.clearFeedback = function() {
     if (this.feedback_exists) {
       $("#ul-" + this.options.sortableId).removeClass("incorrect correct");
       var li_elements = $("#ul-" + this.options.sortableId + " li");
       $.each(this.FEEDBACK_STYLES, function(index, value) {
                li_elements.removeClass(value);
              });
     }
     this.feedback_exists = false;
   };


   ParsonsWidget.prototype.getRandomPermutation = function(n) {
     var permutation = [];
     var i;
     for (i = 0; i < n; i++) {
       permutation.push(i);
     }
     var swap1, swap2, tmp;
     for (i = 0; i < n; i++) {
       swap1 = Math.floor(Math.random() * n);
       swap2 = Math.floor(Math.random() * n);
       tmp = permutation[swap1];
       permutation[swap1] = permutation[swap2];
       permutation[swap2] = tmp;
     }
     return permutation;
   };


   ParsonsWidget.prototype.shuffleLines = function() {
       var permutation = this.getRandomPermutation(this.modified_lines.length);
       var idlist = [];
       for(var i in permutation) {
           idlist.push(this.modified_lines[permutation[i]].id);
       }
       if (this.options.trashId) {
           this.createHTMLFromLists([],idlist);
       } else {
           this.createHTMLFromLists(idlist,[]);
       }
       addToggleableElements(this);
   };

   ParsonsWidget.prototype.createHTMLFromHashes = function(solutionHash, trashHash) {
       var solution = this.hashToIDList(solutionHash);
       var trash = this.hashToIDList(trashHash);
       this.createHTMLFromLists(solution,trash);
       this.updateIndentsFromHash(solutionHash);
   };

    ParsonsWidget.prototype.updateHTMLIndent = function(codelineID) {
        var line = this.getLineById(codelineID);
        $('#' + codelineID).css("margin-left", this.options.x_indent * line.indent + "px");
    };


    ParsonsWidget.prototype.codeLineToHTML = function(codeline) {
        return '<li id="' + codeline.id + '" class="prettyprint lang-py">' + codeline.code + '<\/li>';
    };

    ParsonsWidget.prototype.codeLinesToHTML = function(codelineIDs, destinationID) {
        var lineHTML = [];
        for(var id in codelineIDs) {
            var line = this.getLineById(codelineIDs[id]);
            lineHTML.push(this.codeLineToHTML(line));
        }
        return '<ul id="ul-' + destinationID + '">'+lineHTML.join('')+'</ul>';
    };

   /** modifies the DOM by inserting exercise elements into it */
   ParsonsWidget.prototype.createHTMLFromLists = function(solutionIDs, trashIDs) {
     var html;
     if (this.options.trashId) {
       html = (this.options.trash_label?'<p>'+this.options.trash_label+'</p>':'') +
         this.codeLinesToHTML(trashIDs, this.options.trashId);
       $("#" + this.options.trashId).html(html);
       html = (this.options.solution_label?'<p>'+this.options.solution_label+'</p>':'') +
         this.codeLinesToHTML(solutionIDs, this.options.sortableId);
       $("#" + this.options.sortableId).html(html);
     } else {
       html = this.codeLinesToHTML(solutionIDs, this.options.sortableId);
       $("#" + this.options.sortableId).html(html);
     }

     if (window.prettyPrint && (typeof(this.options.prettyPrint) === "undefined" || this.options.prettyPrint)) {
       prettyPrint();
     }

     var that = this;
     var sortable = $("#ul-" + this.options.sortableId).sortable(
       {
         start : function() { that.clearFeedback(); },
         stop : function(event, ui) {
           if ($(event.target)[0] != ui.item.parent()[0]) {
             return;
           }
           that.updateIndent(ui.position.left - ui.item.parent().offset().left,
                                       ui.item[0].id);
           that.updateHTMLIndent(ui.item[0].id);
           that.addLogEntry({type: "moveOutput", target: ui.item[0].id}, true);
         },
         receive : function(event, ui) {
           var ind = that.updateIndent(ui.position.left - ui.item.parent().offset().left,
                                       ui.item[0].id);
           that.updateHTMLIndent(ui.item[0].id);
           that.addLogEntry({type: "addOutput", target: ui.item[0].id}, true);
         },
         grid : [that.options.x_indent, 1 ]
       });
     sortable.addClass("output");
     if (this.options.trashId) {
       var trash = $("#ul-" + this.options.trashId).sortable(
         {
           connectWith: sortable,
           start: function() { that.clearFeedback(); },
           receive: function(event, ui) {
             that.getLineById(ui.item[0].id).indent = 0;
             that.updateHTMLIndent(ui.item[0].id);
             that.addLogEntry({type: "removeOutput", target: ui.item[0].id}, true);
           },
           stop: function(event, ui) {
             if ($(event.target)[0] != ui.item.parent()[0]) {
               // line moved to output and logged there
               return;
             }
             that.addLogEntry({type: "moveInput", target: ui.item[0].id}, true);
           }
         });
       sortable.sortable('option', 'connectWith', trash);
     }
     this.addLogEntry({type: 'init', time: new Date(), bindings: this.modified_lines});
   };


     window['ParsonsWidget'] = ParsonsWidget;
 }
// allows _ and $ to be modified with noconflict without changing the globals
// that parsons uses
)($,_);
