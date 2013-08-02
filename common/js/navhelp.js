/**
 * Created by isaacdontjelindell on 8/2/13.
 */

/* Sets up the interactive navhelp using intro.js */

var is_setup;

function setup() {
    var ac_block = $("#codeexample1");
    ac_block.attr('data-intro', 'ActiveCode blocks allow you to run Python programs right in the textbook');
    ac_block.attr('data-step', '1');

    var ac_code = $("codeexample1_code_div");
    ac_code.attr('data-intro', 'Write and edit code here');
    ac_code.attr('data-step', '2');


    var ac_run = $("codeexample1_runb");
    ac_run.attr('data-intro', 'Click here to execute the code');
    ac_run.attr('data-step', '3');
}


setup();
