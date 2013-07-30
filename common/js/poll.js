// Javascript needed for the poll Sphinx directive type


function submitPoll(div_id) {
    var form = $("#"+div_id+"_poll");
    var poll_val = form.find("input:radio[name="+div_id +"_opt]:checked").val();
    if(poll_val === undefined)
        return;

    var poll_comment = form.find("input:text[name="+div_id+"_comment]").val();

    var act = '';
    if((poll_comment === undefined) || (poll_comment[0] !== undefined))
        act = poll_val + ":" + poll_comment;
    else
        act = poll_val;

    var eventInfo = {'event':'poll', 'act':act, 'div_id':div_id};

    // log the response to the database
    logBookEvent(eventInfo); // in bookfuncs.js

    // log the fact that the user has answered the poll to local storage
    localStorage.setItem(div_id, "true");

    // hide the poll inputs
    $("#"+div_id+"_poll_input").hide();

    // show the results of the poll
    var data = {};
    data.div_id = div_id;
    data.course = eBookConfig.course;
    jQuery.get(eBookConfig.ajaxURL+'getpollresults', data, showPollResults);
}

function showPollResults(data) {
    // create the display of the poll results

    results = eval(data);
    var total = results[0];
    var opt_list = results[1];
    var count_list = results[2];
    var div_id = results[3];

    var result_div = $("#"+div_id+"_results");
    result_div.html("<b>Results:</b><br><br>");
    result_div.show();

    var list = $(document.createElement("ol"));
    for(var i=0; i<opt_list.length; i++) {
        var count = count_list[i];
        var percent = (count / total) * 100;
        var text = Math.round(10*percent)/10 + "%";   // round percent to 10ths

        var html = "<li value='"+opt_list[i]+"'><div class='progress'><div class='progress-bar progress-bar-success' style='width:"+percent+"%;'><span class='poll-text'>"+text+"</span></div></div></li>";
        var el = $(html);
        list.append(el);
    }
    result_div.append(list);
}

