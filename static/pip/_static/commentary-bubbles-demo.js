// Run:
//   python generate_json_trace.py --create_jsvar=listSumTrace tests/backend-tests/list_sum.txt
// and copy-and-paste the output line into here:
var listSumTrace = {"code": "def listSum(numbers):\n  if not numbers:\n    return 0\n  else:\n    (f, rest) = numbers\n    return f + listSum(rest)\n\nmyList = (1, (2, (3, None)))\ntotal = listSum(myList)\n", "trace": [{"ordered_globals": [], "stdout": "", "func_name": "<module>", "stack_to_render": [], "globals": {}, "heap": {}, "line": 1, "event": "step_line"}, {"ordered_globals": ["listSum"], "stdout": "", "func_name": "<module>", "stack_to_render": [], "globals": {"listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null]}, "line": 8, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "<module>", "stack_to_render": [], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 9, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2]}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 1, "event": "call"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2]}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 2, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2]}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 5, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 6, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3]}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 1, "event": "call"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3]}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 2, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3]}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 5, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3], "rest": ["REF", 4], "f": 2}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers", "f", "rest"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 6, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3], "rest": ["REF", 4], "f": 2}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 3, "encoded_locals": {"numbers": ["REF", 4]}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f3", "ordered_varnames": ["numbers"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 1, "event": "call"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3], "rest": ["REF", 4], "f": 2}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 3, "encoded_locals": {"numbers": ["REF", 4]}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f3", "ordered_varnames": ["numbers"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 2, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3], "rest": ["REF", 4], "f": 2}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 3, "encoded_locals": {"numbers": ["REF", 4]}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f3", "ordered_varnames": ["numbers"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 5, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3], "rest": ["REF", 4], "f": 2}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 3, "encoded_locals": {"numbers": ["REF", 4], "rest": null, "f": 3}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f3", "ordered_varnames": ["numbers", "f", "rest"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 6, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3], "rest": ["REF", 4], "f": 2}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 3, "encoded_locals": {"numbers": ["REF", 4], "rest": null, "f": 3}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f3", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 4, "encoded_locals": {"numbers": null}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f4", "ordered_varnames": ["numbers"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 1, "event": "call"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3], "rest": ["REF", 4], "f": 2}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 3, "encoded_locals": {"numbers": ["REF", 4], "rest": null, "f": 3}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f3", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 4, "encoded_locals": {"numbers": null}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f4", "ordered_varnames": ["numbers"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 2, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3], "rest": ["REF", 4], "f": 2}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 3, "encoded_locals": {"numbers": ["REF", 4], "rest": null, "f": 3}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f3", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 4, "encoded_locals": {"numbers": null}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f4", "ordered_varnames": ["numbers"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 3, "event": "step_line"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3], "rest": ["REF", 4], "f": 2}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 3, "encoded_locals": {"numbers": ["REF", 4], "rest": null, "f": 3}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f3", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 4, "encoded_locals": {"__return__": 0, "numbers": null}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f4", "ordered_varnames": ["numbers", "__return__"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 3, "event": "return"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"numbers": ["REF", 3], "rest": ["REF", 4], "f": 2}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 3, "encoded_locals": {"__return__": 3, "numbers": ["REF", 4], "rest": null, "f": 3}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f3", "ordered_varnames": ["numbers", "f", "rest", "__return__"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 6, "event": "return"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": false, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest"]}, {"frame_id": 2, "encoded_locals": {"__return__": 5, "numbers": ["REF", 3], "rest": ["REF", 4], "f": 2}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f2", "ordered_varnames": ["numbers", "f", "rest", "__return__"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 6, "event": "return"}, {"ordered_globals": ["listSum", "myList"], "stdout": "", "func_name": "listSum", "stack_to_render": [{"frame_id": 1, "encoded_locals": {"__return__": 6, "numbers": ["REF", 2], "rest": ["REF", 3], "f": 1}, "is_highlighted": true, "is_parent": false, "func_name": "listSum", "is_zombie": false, "parent_frame_id_list": [], "unique_hash": "listSum_f1", "ordered_varnames": ["numbers", "f", "rest", "__return__"]}], "globals": {"myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 6, "event": "return"}, {"ordered_globals": ["listSum", "myList", "total"], "stdout": "", "func_name": "<module>", "stack_to_render": [], "globals": {"total": 6, "myList": ["REF", 2], "listSum": ["REF", 1]}, "heap": {"1": ["FUNCTION", "listSum(numbers)", null], "2": ["TUPLE", 1, ["REF", 3]], "3": ["TUPLE", 2, ["REF", 4]], "4": ["TUPLE", 3, null]}, "line": 9, "event": "return"}]};


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


function createSpeechBubble(domID, my, at, htmlContent, isInput) {
  var hashID = '#' + domID;
  $(hashID).qtip($.extend({}, qtipShared, {
    content: htmlContent,
    id: domID,
    position: {
      my: my,
      at: at,
      effect: null, // disable all cutesy animations
    },
  }));


  if (isInput) {

  }
  else {
    $('#ui-tooltip-' + domID + '-content').click(function() {
      if (!$(hashID).data('qtip-minimized')) {
        $(hashID)
          .data('qtip-minimized', true)
          .qtip('option', 'content.text', ' ');
      }
      else {
        $(hashID)
          .data('qtip-minimized', false)
          .qtip('option', 'content.text', htmlContent);
      }
    });
  }
}


// a speech bubble annotation to attach to:
//   'codeline' - a line of code
//   'frame'    - a stack frame
//   'variable' - a variable within a stack frame
//   'object'   - an object on the heap
// (as determined by the 'type' param)
//
// domID is the ID of the element to attach to (without the leading '#' sign)
function AnnotationBubble(type, domID) {
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
      if (globalAnnotationMode == 'edit') {
        myBubble.showEditor();
      }
      else if (globalAnnotationMode == 'view') {
        myBubble.minimizeViewer();
      }
      else {
        assert(false);
      }
    });
}

AnnotationBubble.prototype.showViewer = function() {
  assert(this.state == 'edit');
  assert(this.text); // must be non-empty!

  // destroy then create a new tip:
  this.destroyQTip();
  $(this.hashID).qtip($.extend({}, qtipShared, {
    content: this.text,
    id: this.domID,
    position: {
      my: this.my,
      at: this.at,
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
      if (globalAnnotationMode == 'edit') {
        myBubble.showEditor();
      }
      else if (globalAnnotationMode == 'view') {
        myBubble.restoreViewer();
      }
      else {
        assert(false);
      }
    });

  this.state = 'minimized';
}

AnnotationBubble.prototype.restoreViewer = function() {
  assert(this.state == 'minimized');
  $(this.hashID).qtip('option', 'content.text', this.text);
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
  assert(globalAnnotationMode == 'edit');
  if (this.state == 'invisible') {
    this.showStub();

    if (this.type == 'codeline') {
      this.redrawCodelineBubble();
    }
  }
}

AnnotationBubble.prototype.enterViewMode = function() {
  assert(globalAnnotationMode == 'view');
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
}

AnnotationBubble.prototype.redrawCodelineBubble = function() {
  assert(this.type == 'codeline');

  if (isOutputLineVisible(this.domID)) {
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


globalAnnotationMode = 'view';
allBubbles = [];


// returns True iff lineNo is visible in pyCodeOutputDiv
// NB: copied, pasted, and modified from isOutputLineVisible in js/pytutor.js
function isOutputLineVisible(lineDivID) {
  var pcod = $('#pyCodeOutputDiv');

  var lineNoTd = $('#' + lineDivID);
  var LO = lineNoTd.offset().top;

  var PO = pcod.offset().top;
  var ST = pcod.scrollTop();
  var H = pcod.height();

  // add a few pixels of fudge factor on the bottom end due to bottom scrollbar
  return (PO <= LO) && (LO < (PO + H - 25));
}


$(document).ready(function() {
  /*
  var listSumVisualizer = new ExecutionVisualizer('listSumDiv', listSumTrace,
                                                  {embeddedMode: false,
                                                   editCodeBaseURL: 'http://pythontutor.com/visualize.html'});

  return;
  */

  // force vertical code scrolling
  $('#pyCodeOutputDiv').css('max-height', '120px');

  allBubbles.push(new AnnotationBubble('frame', 'v1__globals'));
  allBubbles.push(new AnnotationBubble('frame', 'v1__stack0'));
  allBubbles.push(new AnnotationBubble('frame', 'v1__stack1'));
  allBubbles.push(new AnnotationBubble('frame', 'v1__stack2'));
  allBubbles.push(new AnnotationBubble('frame', 'v1__stack3'));

  allBubbles.push(new AnnotationBubble('object', 'v1__heap_object_1'));
  allBubbles.push(new AnnotationBubble('object', 'v1__heap_object_2'));
  allBubbles.push(new AnnotationBubble('object', 'v1__heap_object_3'));
  allBubbles.push(new AnnotationBubble('object', 'v1__heap_object_4'));

  allBubbles.push(new AnnotationBubble('codeline', 'v1__cod1'));
  allBubbles.push(new AnnotationBubble('codeline', 'v1__cod2'));
  allBubbles.push(new AnnotationBubble('codeline', 'v1__cod3'));
  allBubbles.push(new AnnotationBubble('codeline', 'v1__cod4'));
  allBubbles.push(new AnnotationBubble('codeline', 'v1__cod5'));
  allBubbles.push(new AnnotationBubble('codeline', 'v1__cod6'));
  allBubbles.push(new AnnotationBubble('codeline', 'v1__cod7'));
  allBubbles.push(new AnnotationBubble('codeline', 'v1__cod8'));
  allBubbles.push(new AnnotationBubble('codeline', 'v1__cod9'));

  allBubbles.push(new AnnotationBubble('variable', 'v1__global__listSum_tr'));
  allBubbles.push(new AnnotationBubble('variable', 'v1__global__myList_tr'));

  allBubbles.push(new AnnotationBubble('variable', 'v1__listSum_f1__numbers_tr'));
  allBubbles.push(new AnnotationBubble('variable', 'v1__listSum_f1__f_tr'));
  allBubbles.push(new AnnotationBubble('variable', 'v1__listSum_f1__rest_tr'));

  allBubbles.push(new AnnotationBubble('variable', 'v1__listSum_f2__numbers_tr'));
  allBubbles.push(new AnnotationBubble('variable', 'v1__listSum_f2__f_tr'));
  allBubbles.push(new AnnotationBubble('variable', 'v1__listSum_f2__rest_tr'));

  allBubbles.push(new AnnotationBubble('variable', 'v1__listSum_f3__numbers_tr'));
  allBubbles.push(new AnnotationBubble('variable', 'v1__listSum_f3__f_tr'));
  allBubbles.push(new AnnotationBubble('variable', 'v1__listSum_f3__rest_tr'));

  allBubbles.push(new AnnotationBubble('variable', 'v1__listSum_f4__numbers_tr'));
  allBubbles.push(new AnnotationBubble('variable', 'v1__listSum_f4____return___tr'));


  $('#pyCodeOutputDiv').scroll(function() {
    $.each(allBubbles, function(i, e) {
      if (e.type == 'codeline') {
        e.redrawCodelineBubble();
      }
    });
  });


  $('#modeToggleBtn').click(function() {
    if (globalAnnotationMode == 'view') {
      $('#modeToggleBtn').html('View Annotations');
      globalAnnotationMode = 'edit';
      $.each(allBubbles, function(i, e) {
        e.enterEditMode();
      });
    }
    else if (globalAnnotationMode == 'edit') {
      $('#modeToggleBtn').html('Add/Edit Annotations');
      globalAnnotationMode = 'view';
      $.each(allBubbles, function(i, e) {
        e.enterViewMode();
      });
    }
    else {
      assert(false);
    }
  });
});
