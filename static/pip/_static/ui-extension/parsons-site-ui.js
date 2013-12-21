(function() {
  var ANIMATION_DURATION = 200,
      touch = ( 'ontouchstart' in document.documentElement ) ? true : false,
      clickEvent = touch?"touchstart":"click",
      FEEDBACK_WINDOWS = [5000, 20000, 45000],
      FEEDBACK_PENALTIES = [15000, 15000, 15000],
      COLLECT_ANONYMOUS_DATA = false,
      previousFeedbackState,
      exercise,
      parson,
      feedbackTimeHistory;

  // object to handle the assignment tab
  var AssignmentTab = {
    toggle: function() {
      var $ass = $(".assignment");
      if ($ass.hasClass("hidden")) { // hidden, so we'll show it
        $ass.animate({"left": "0"}, ANIMATION_DURATION);
      } else {
        $ass.animate({"left": "-" + $ass.find(".assignmentText").outerWidth() + "px"}, ANIMATION_DURATION);
      }
      $ass.toggleClass("hidden ontop");
      $("#modality").toggleClass("visible");
    },
    init: function() {
      // handle assignment show/hide
      $(".content").off(clickEvent).on(clickEvent, ".assignment .tabRight, #hideAssignment", function(e) {
        e.stopPropagation();
        e.preventDefault();
        AssignmentTab.toggle();
      });
      // update assignment text and make sure it is visible
      $(".assignmentText").html("<h2>" + exercise.name + "</h2>" + exercise.assignment +
                  "<div class='buttonContainer'><button id='hideAssignment'>OK</button></div>");
      $(".assignment").css({"left": 0}).removeClass("hidden").addClass("ontop");

      // expose by adding to the parson object
      parson.AssignmentTab = AssignmentTab;
    }
  };



  // object to handle the revisit feedback tab
  var RevisitFeedback = {
    _available: false,
    _element: undefined,
    init: function() {
      this._element = $(".previously");
      var that = this;
      $(".content").on(clickEvent, ".previously .tabLeft", function(e) {
        if (!that.isVisible()) {
          that.show();
        } else {
          that.hide();
        }
      });
      return this;
    },
    isVisible: function() {
      return this._element.hasClass("visible");
    },
    show: function() {
      if (this._element) {
        this._element.toggleClass("ontop visible").find(".prevContent").css({width: "100%"});
        $("#modality").addClass("visible");
        this._element.css({ right: "-" + this._element.outerWidth() + "px"}).animate({right: "40px"}, ANIMATION_DURATION);
      }
      return this;
    },
    hide: function() {
      if (this._element) {
        this._element.toggleClass("ontop visible").css({right: 0}).find(".prevContent").animate({width: 0}, ANIMATION_DURATION);
        $("#modality").removeClass("visible");
      }
      return this;
    },
    available: function(newVal) {
      if (typeof newVal === "undefined") {
        return this._available;
      } else {
        this._available = newVal;
        if (newVal) {
          this._element.addClass("available");
        } else {
          this._element.removeClass("available");
        }
        return this;
      }
    },
    html: function(val) {
      if (!this._element) {
        this.init();
      }
      this._element.find(".prevContent").html(val);
      return this;
    },
    label: function(label) {
      if (!this._element) { this.init(); }
      if (typeof label === "undefined") {
        return this._element.find(".tabLeft").text();
      } else {
        this._element.find(".tabLeft").text(label);
        return this;
      }
    },
    highlightLine: function(lineid) {
      this._element.find("#" + lineid).addClass("changed");
      return this;
    }
  };

  var createParsonFeedbackForElement = function(elemId, parsonStateHash) {
    var otherParson = new ParsonsWidget({
        'sortableId': elemId,
        'max_wrong_lines': 100
    });
    otherParson.init(exercise.code);
    otherParson.createHTMLFromHashes(parsonStateHash, "");
    otherParson.getFeedback();
    return otherParson;
  };

  var setLastFeedback = function() {
    if (!RevisitFeedback.available() || RevisitFeedback.label() !== "Hint") {
      var html = "<p>This is the feedback you were shown when you requested it the last time.</p>" +
                 "<div class='sortable-code' id='prevFeedback'></div>";
      if ('feedback' in previousFeedbackState.feedback) {
        html += "<h2 style='clear:both;'>Test Results</h2>" + previousFeedbackState.feedback.feedback;
      }
      RevisitFeedback.html(html).label("Last Feedback").available(true);
      createParsonFeedbackForElement("prevFeedback", previousFeedbackState.state);
    }
  };
  // callback function called when user action is done on codelines
  var actionCallback = function(newAction) {
    // ignore init and feedback actions
    if (newAction.type === "init" || newAction.type === "feedback") { return; }
    var action = parson.whatWeDidPreviously();
    // if we have been here before (action not undefined) and more than one line in solution...
    if (action && action.output && newAction.output.split('-').length > 1 && action.output.split('-').length > 1 && action.stepsToLast > 2) {
      var html = "<div class='currentState'><p>Your current code is identical to one you had " +
                 "previously. You might want to stop going in circles and think carefully about " +
                 "the feedback shown here.</p>" +
                 "<div class='sortable-code' id='currFeedback'></div>";
      html += "</div><div class='prevAction'><p>Last time you went on to move the line " +
              "highlighted with a blue right margin. Think carefully about the feedback for " +
              "this code and your current code.</p>" +
              "<div class='sortable-code' id='prevFeedback'></div>";
      html += "</div>";

      // .. set the content of the tab ...
      RevisitFeedback.html(html)
                     .label("Hint")
                     .available(true); // .. and make the "feedback" available
      // create the parsons feedback
      createParsonFeedbackForElement("currFeedback", newAction.output);
      createParsonFeedbackForElement("prevFeedback", action.output);
      // .. and higlight modified lines
      RevisitFeedback.highlightLine("currFeedbackcodeline" + action.target)
                     .highlightLine("prevFeedbackcodeline" + action.target);
    } else if (previousFeedbackState) {
      RevisitFeedback.available(false);
      setLastFeedback();
    } else {
      RevisitFeedback.available(false); // make the feedback unavailable
    }
  };

  // function used to show a UI message dialog
  var showDialog = function(title, message, callback, options) {
    var buttons = {};
    buttons[options?(options.buttonTitle || "OK"):"OK"] = function() {
      $(this).dialog( "close" );
    };
    var opts = $.extend(true,
                        { buttons: buttons,
                          modal: true,
                          title: title,
                          draggable: false,
                          close: function() {
                            // if there is a callback, call it
                            if ($.isFunction(callback)) {
                              callback();
                            }
                            return true;
                          }
                        },
                        options);
    $("#feedbackDialog") // find the dialog element
          .find("p") // find the p element inside
              .text(message) // set the feedback text
          .end() // go back to the #feedbackDialog element
          .dialog(opts);
  };

  // function to disable feedback for duration milliseconds
  var disableFeedback = function(duration) {
    $("#header").addClass("timer");
    $("#timer").show().animate({width: "100%"}, duration, function() {
      $("#header").removeClass("timer");
      $("#timer").hide().css({width: "0"});
    });
  };


  // default feedback callback handler
  var feedbackHandler = function(feedback) {
    var isCorrect = ($.isArray(feedback) && feedback.length === 0) ||
                    ('feedback' in feedback && feedback.success);

    // correctly solved but collection has more exercises
    if (isCorrect && $.isFunction(PARSONS_SETTINGS.next)) {
      $("#ul-sortable").sortable("destroy");
      $("#ul-sortableTrash").sortable("destroy");
      showDialog("Good Job!", "Click OK to go to the next question.", function() {
        PARSONS_SETTINGS.next();
      });
    } else if (isCorrect) { // correct and last question
      showDialog("Good Job!", "That was the last question. Click OK to go back to main page.", function() {
        window.location = "./index.html";
      });
    } else { // not correct, show feedback
      var now = new Date(),
          penaltyTime = 0,
          feedbackText;
      if ($.isArray(feedback)) { // line-based feedback
        feedbackText = feedback.join('\n');
      } else if ('feedback' in feedback) { // execution based feedback
        feedbackText = "Some tests failed for your solution. See the Last Feedback tab for details.";
      }
      if (feedbackTimeHistory.length > 1) { // 1st and 2nd feedback can't be too fast
        // we'll go through all the times in the feedback time history
        for (var i = 0; i < feedbackTimeHistory.length; i++) {
          // check if the corresponding feedbackwindow is bigger than time between now
          // and the i:th feedback time
          if (FEEDBACK_WINDOWS[i] > now - feedbackTimeHistory[i]) {
            penaltyTime += FEEDBACK_PENALTIES[i]; // add to penalty time
          }
        }
        // if there is penalty time, disable feedback and show a message to student
        if (penaltyTime > 0) {
          disableFeedback(penaltyTime);
          feedbackText += "\n\nDue to frequent use, feedback has been disabled for a while. It will be" +
                        "available once the button turns orange again. You can still continue solving the problem.";
        }
      }
      // add the current time to the feedbak history
      feedbackTimeHistory.unshift(now);
      // make sure we have at most as many feedback times in history as we have windows
      feedbackTimeHistory = feedbackTimeHistory.slice(0, FEEDBACK_WINDOWS.length);
      showDialog("Feedback", feedbackText);
    }
  };


  // function for doing some repositioning/sizing when orientation changes or window resizes
  var handleOrientationChange = function() {
    $("body").css({width: $(window).width(), minHeight: $(window).height() });
    var $ass = $(".assignment");
    // reposition the assignment tab
    if ($ass.hasClass("hidden")) { // assignment tab hidden, need to reposition
      $ass.css({left: "-" + $ass.find(".assignmentText").outerWidth() + "px"});
    }
    // position the timer bar
    $("#timer").css({top: $("#header").innerHeight()});
  };
  // register a listener for the orientation change event and resize
  $(window).on("orientationchange resize", _.throttle(handleOrientationChange, 50));


  // Helper function for initializing a ParsonsWidget for the given exercise.
  // Parameter exer should be an object describing a Parsons exercise with the
  // following properties:
  //   - code: contains the initial codelines for the exercise in the same format as the
  //           widget wants them (that is, one long string with \n characters) [REQUIRED]
  //   - assignment: the assignment text for the exercise [REQUIRED]
  //   - name: the name of the exercise [REQUIRED]
  //   - unit_tests: unit tests used in assessing a solution [optional]
  //
  // The function uses a global PARSONS_SETTINGS to configure the behavior. Possible properties:
  //   - widget_options: An objects with properties that will be passed to ParsonsWidget
  //   - submit_url: A url where the log and student solution is POSTed when feedback is requested.
  //   - submit_data: Additional data that is POSTed on feedback request. The log data and student
  //                  solution will automatically be added to this data.
  //   - submit_callback: A function which is called whenever a user requests feedback. The function
  //                      is passed feedback as a first parameter, and, if submit_url is specified,
  //                      also data, textStatus, and jqXhr parameters (see jQuery Ajax docs for details).
  //   - next: A function which is called when a user correctly solves an exercise. This is useful for
  //           collection of exercises.
  function initParsons(exer) {
    exercise = exer;
    feedbackTimeHistory = [];

    if (!PARSONS_SETTINGS) {
      PARSONS_SETTINGS = {};
    }

    var widget_options = $.extend({
                  'sortableId': 'sortable', 'trashId': 'sortableTrash',
                  'max_wrong_lines': 100,
                  'action_cb': actionCallback
                  }, PARSONS_SETTINGS.widget_options);
    if (exercise.unit_tests) {
      widget_options.unittests = $.parseJSON(exercise.unit_tests);
    }

    // initialize the widget
    parson = new ParsonsWidget(widget_options);
    parson.init(exercise.code);
    parson.shuffleLines();
    parson.showDialog = showDialog;

    // initialize UI
    AssignmentTab.init();
    // update, clear, and position the previously visited feedback tab
    RevisitFeedback.init().html("").available(false);
    previousFeedbackState = undefined;

    // add modality panel
    $("#modality").addClass("visible");


    $(".output").css({minHeight: $(".output").height() + "px" });

    $("#submitLink").off("click").click(function(event) {
      event.preventDefault();
      // if feedback is disabled (timer available), don't give feedback
      if ($("#header").hasClass("timer")) { return; }
      var feedback = parson.getFeedback(),
          callbackHandler = function(data, textStatus, jqXhr) {
            if ($.isFunction(PARSONS_SETTINGS.submit_callback)) {
              PARSONS_SETTINGS.submit_callback(feedback, data, textStatus, jqXhr);
            } else {
              feedbackHandler(feedback);
            }
          };
      previousFeedbackState = {
        state: parson.user_actions[parson.user_actions.length - 1].output,
        feedback: feedback
      };
      setLastFeedback(feedback); // update the Last feedback tab


      if (PARSONS_SETTINGS.submit_url) {
        var post_data = $.extend({'submission': JSON.stringify({'actions': parson.user_actions }),
                                  'feedback': $.isArray(feedback)?feedback.length:(feedback.success?0:1)},
                                PARSONS_SETTINGS.submit_data);
        $.post(PARSONS_SETTINGS.submit_url, post_data, function(data, textStatus, jqXhr) {
          callbackHandler(data, textStatus, jqXhr);
        });
      } else {
        callbackHandler();
      }
    });

    handleOrientationChange(); // size things up properly

    // return the widget
    return parson;
  }

  // expose the initParsons function
  window.initParsons = initParsons;
})();
