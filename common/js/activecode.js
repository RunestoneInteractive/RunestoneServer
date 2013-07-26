var elem; // current audio element playing
var dur=0; // the time that the current audio file takes to play in seconds
var interval=0; // curent timer (used to play the next audio file)
var currIndex; // current index
var len; // current length of audio files for tour
var buttonCount; // number of audio tour buttons
var aname; // the audio file name
var ahash; // hash of the audio file name to the lines to highlight
var theDivid; // div id 

String.prototype.replaceAll = function(target, replacement)
{
  return this.split(target).join(replacement);
};

// function to display the audio tours
var createAudioTourHTML = function(divid,code,bnum,audio_text)
{
    
    // Replacing has been done here to make sure special characters in the code are displayed correctly
    code=code.replaceAll("*doubleq*","\"");
    code=code.replaceAll("*singleq*","'");
    code=code.replaceAll("*open*","(");
    code=code.replaceAll("*close*",")");
    code=code.replaceAll("*nline*","<br/>");
    var codeArray=code.split("<br/>");

    var audio_hash=new Array();
    var bval=new Array();
    var atype=audio_text.replaceAll("*doubleq*","\"");
    var audio_type=atype.split("*atype*");
    for(var i=0;i<audio_type.length-1;i++)
    {
        audio_hash[i]=audio_type[i];
        var aword=audio_type[i].split(";");
        bval.push(aword[0]);
    }   

    var first="<pre><div id='"+divid+"_l1'>"+"1.  "+codeArray[0]+"</div>";
    num_lines=codeArray.length;
    for(var i=1;i<num_lines;i++)
    {
        var sec="<div id='"+divid+"_l"+ (i+1) +"'>"+(i+1)+".  "+codeArray[i]+"</div>";
        var next=first.concat(sec);
        first=next;
    }
    first = first + "</pre>"
    
    //laying out the HTML content
    
    var bcount=0;
    var html_string="<div class='modal-lightsout'></div><div class='modal-profile'><h2>Take an audio tour through the code!</h2><div class='modal-close-profile'></div><p id='windowcode'></p><p id='"+divid+"_audiocode'></p>";
    html_string+="<input type='image' src='../_static/first.png' width='25' id='first_audio' name='first_audio' title='Play first audio in tour' alt='Play first audio in tour' disabled/>"+"<input type='image' src='../_static/prev.png' width='25' id='prev_audio' name='prev_audio' title='Play previous audio in tour' alt='Play previous audio in tour' disabled/>" + "<input type='image' src='../_static/pause.png' width='25' id='pause_audio' name='pause_audio' title='Pause current audio' alt='Pause current audio' disabled/><input type='image' src='../_static/next.png' width ='25' id='next_audio' name='next_audio' title='Play next audio in tour' alt='Play next audio in tour' disabled/><input type='image' src='../_static/last.png' width ='25' id='last_audio' name='last_audio' title='Play last audio in tour' alt='Play last audio in tour' disabled/><br/>";
    for(var i=0;i<audio_type.length-1;i++)
    {
        html_string+="<input type='button' id='button_audio_"+i+"' name='button_audio_"+i+"' value="+bval[i]+" />";
        bcount++;
    }
    html_string+="<p id='status'></p><p id='hightest'></p><p id='hightest1'></p><br/><br/><p id='test'></p><br/><p id='audi'></p></div>"

    $('#cont').html(html_string);
    $('#windowcode').html(first);

    // Position modal box in the center of the page
	$.fn.center = function () 
    {
		this.css("position","absolute");
		this.css("top", ( $(window).height() - this.height() ) / 2+$(window).scrollTop() + "px");
        // show window on the right so that you can see the output from the code still and still be able to close this window
		this.css("left", ( $(window).width() - this.width() ) - 60 +$(window).scrollLeft() + "px");
		return this;
    }
        
	$(".modal-profile").center();
    $('.modal-profile').fadeIn("slow");
    $('.modal-lightsout').css("height", $(document).height());	
    $('.modal-lightsout').fadeTo("slow", .5);
    $('.modal-close-profile').show();
    
     // closes modal box once close link is clicked, or if the lights out divis clicked
	$('.modal-close-profile, .modal-lightsout').click(function() {
        if(interval)
        {
            elem.pause();
            clearInterval(interval);
		}
        //log change to db
        logBookEvent({'event':'Audio', 'change':'closeWindow', 'div_id':divid});
        $('.modal-profile').fadeOut("slow");
		$('.modal-lightsout').fadeOut("slow");
	});
    
    // Accommodate buttons for a maximum of five tours 
    
    $('#'+'button_audio_0').click(function(){
    tour(divid,audio_hash[0],bcount);});
    $('#'+'button_audio_1').click(function(){
    tour(divid,audio_hash[1],bcount);});
    $('#'+'button_audio_2').click(function(){
    tour(divid,audio_hash[2],bcount);});
    $('#'+'button_audio_3').click(function(){
    tour(divid,audio_hash[3],bcount);});
    $('#'+'button_audio_4').click(function(){
    tour(divid,audio_hash[4],bcount);});
    
     // handle the click to go to the next audio
    $('#first_audio').click(function(){
      firstAudio();});
    
    // handle the click to go to the next audio
    $('#prev_audio').click(function(){
      prevAudio();});
    
    // handle the click to pause or play the audio
    $('#pause_audio').click(function(){
      pauseAndPlayAudio();});
    
     // handle the click to go to the next audio
    $('#next_audio').click(function(){
      nextAudio();});
      
      // handle the click to go to the next audio
    $('#last_audio').click(function(){
      lastAudio();});
    
    // make the image buttons look disabled
    $("#first_audio").css('opacity',0.25);
    $("#prev_audio").css('opacity',0.25);
    $("#pause_audio").css('opacity',0.25);
    $("#next_audio").css('opacity',0.25);
    $("#last_audio").css('opacity',0.25);
    
};

var tour = function(divid,audio_type,bcount)
{
    // set globals
    buttonCount = bcount;
    theDivid = divid;
    
    // enable prev, pause/play and next buttons and make visible
    $('#first_audio').removeAttr('disabled');
    $('#prev_audio').removeAttr('disabled');
    $('#pause_audio').removeAttr('disabled');
    $('#next_audio').removeAttr('disabled');
    $('#last_audio').removeAttr('disabled');
    $("#first_audio").css('opacity',1.0);
    $("#prev_audio").css('opacity',1.0);
    $("#pause_audio").css('opacity',1.0);
    $("#next_audio").css('opacity',1.0);
    $("#last_audio").css('opacity',1.0);
    
    // disable tour buttons
    for(var i=0;i<bcount;i++)
        $('#button_audio_'+i).attr('disabled', 'disabled');
    
    var atype=audio_type.split(";");
    var name=atype[0].replaceAll("\""," ");
    $('#status').html("Starting"+name+"…");
    
    //log tour type to db
    logBookEvent({'event':'Audio', 'tour type':name, 'div_id':divid});
    
    var max=atype.length;
    var str="";
    ahash=new Array();
    aname=new Array();
    for(i=1;i<max-1;i++)
    {
        var temp=atype[i].split(":");
        var temp_line=temp[0];
        var temp_aname=temp[1];
        
        var akey=temp_aname.substring(1,temp_aname.length);
        var lnums=temp_line.substring(1,temp_line.length);
        
        //alert("akey:"+akey+"lnum:"+lnums);
        
       // str+="<audio id="+akey+" preload='auto'><source src='http://ice-web.cc.gatech.edu/ce21/audio/"+
       // akey+".mp3' type='audio/mpeg'><source src='http://ice-web.cc.gatech.edu/ce21/audio/"+akey+
       // ".ogg' type='audio/ogg'>Your browser does not support the audio tag</audio>";
        str+="<audio id="+akey+" preload='auto'><source src='../_static/audio/"+
        akey+".mp3' type='audio/mpeg'><br /><source src='../_static/audio/"+akey+
        ".wav' type='audio/wav'>Your browser does not support the audio tag</audio>";
        ahash[akey]=lnums;
        aname.push(akey);
    }
    var ahtml="#"+divid+"_audiocode";
    $(ahtml).html(str); // set the html to the audio tags
    len=aname.length;
    
    //playing audio
    dur=0;
    currIndex=0;
    
    // start outerAudio after 500 milliseconds (don't do too small of a number or several will start at once)
    interval = setInterval(outerAudio, 500);
}

var firstAudio = function()
{

      // if playing audio stop it and clear the current interval
      if (interval)
      {
        elem.pause();
        clearInterval(interval);
        // unhighlight the prev lines
        unhighlightLines(theDivid,ahash[aname[currIndex-1]]);
      }
      
      //log change to db
      logBookEvent({'event':'Audio', 'change':'first', 'div_id':theDivid});
    
   
      // move to the first audio
      currIndex=0;
      
      // start at the next audio after 500 milliseconds
      interval = setInterval(outerAudio, 500); // start timer
   
}

var prevAudio = function()
{
    // if there is a previous audio file
    if (currIndex >= 2)
    {
      // if playing audio stop it and clear the current interval
      if (interval)
      {
        elem.pause();
        clearInterval(interval);
        // unhighlight the prev lines
        unhighlightLines(theDivid,ahash[aname[currIndex-1]]);
      }
      
      //log change to db
      logBookEvent({'event':'Audio', 'change':'prev', 'div_id':theDivid});
    
   
      // move to previous to the current (but the current index has moved to the next)
      currIndex=currIndex - 2;
      
      // start at the next audio after 500 milliseconds
      interval = setInterval(outerAudio, 500); // start timer
    }
   
}

var nextAudio = function()
{
    // if playing audio stop it and clear the current interval
    if (interval)
    {
        elem.pause();
        clearInterval(interval);
    }
    
    //log change to db
    logBookEvent({'event':'Audio', 'change':'next', 'div_id':theDivid});
      
    // start at the next audio after 500 milliseconds
    interval = setInterval(outerAudio, 500); // start timer
}

var lastAudio = function()
{

      // if playing audio stop it and clear the current interval
      if (interval)
      {
        elem.pause();
        clearInterval(interval);
        // unhighlight the prev lines
        unhighlightLines(theDivid,ahash[aname[currIndex-1]]);
      }
      
      //log change to db
      logBookEvent({'event':'Audio', 'change':'last', 'div_id':theDivid});
    
      // move to the last audio
      currIndex=len-1;
      
      // start at the next audio after 500 milliseconds
      interval = setInterval(outerAudio, 500); // start timer
   
}

// play the audio at the current index
var playCurrIndexAudio = function()
{
            // clear the status
            $('#status').html(" ");
    
            // play the next audio and highlight the lines
            playaudio(currIndex,aname,theDivid,ahash);

            currIndex++; // increment the current index
            if (interval)
              clearInterval(interval); // stop timer if there is one
            counter = (dur * 1000); // change the time to milliseconds 
            interval = setInterval(outerAudio, counter); // start timer
}

var outerAudio = function()
{
        // if index > 0 then unhighlight previous
        if (currIndex > 0)
        {
            unhighlightLines(theDivid,ahash[aname[currIndex-1]]);
        }
            
        // if the end of the tour
        if(currIndex==len && interval)
        {
            
            // stop the timer
            clearInterval(interval);
            
            // disable the prev, pause/play, and next buttons and make them more invisible
            $('#first_audio').attr('disabled', 'disabled');
            $('#prev_audio').attr('disabled', 'disabled');
            $('#pause_audio').attr('disabled', 'disabled');
            $('#next_audio').attr('disabled', 'disabled');
            $('#last_audio').attr('disabled', 'disabled');
            $("#first_audio").css('opacity',0.25);
            $("#prev_audio").css('opacity',0.25);
            $("#pause_audio").css('opacity',0.25);
            $("#next_audio").css('opacity',0.25);
            $("#last_audio").css('opacity',0.25);
            
            // enable the tour buttons
            for(var j=0;j<buttonCount;j++)
               $('#button_audio_'+j).removeAttr('disabled');
        }
        else if (currIndex < len)
        {
           // play the audio at the current index
           playCurrIndexAudio();
        }
}

// play the audio and set the duration and highlight the lines
var playaudio=function(i,aname,divid,ahash)
{
    var afile=aname[i];
    elem=document.getElementById(afile);
    elem.currentTime = 0;
    elem.play();
    dur=elem.duration; // the length of the audio in seconds
    highlightLines(divid,ahash[afile]);
}

// pause if playing and play if paused
var pauseAndPlayAudio=function()
{
    var btn = document.getElementById('pause_audio'); 
    
    // if paused and clicked then continue from current
    if (elem.paused)
    {
            // calcualte the time left to play in milliseconds
            counter = (dur - elem.currentTime) * 1000;
            elem.play(); // start the audio from current spot
            interval = setInterval(outerAudio, counter); // set timer
            document.getElementById("pause_audio").src = "../_static/pause.png";
            document.getElementById("pause_audio").title = "Pause current audio";
            //log change to db
            logBookEvent({'event':'Audio', 'change':'play', 'div_id':theDivid});
    }
    
    // if audio was playing pause it
   else if(interval)
    {
            elem.pause(); // pause the audio
            clearInterval(interval); // clear the highlight 
            document.getElementById("pause_audio").src = "../_static/play.png";
            document.getElementById("pause_audio").title = "Play paused audio";
            //log change to db
            logBookEvent({'event':'Audio', 'change':'pause', 'div_id':theDivid});
    }
    
}

// process the lines
var processLines = function(divid, lnum, color)
{
    var comma= lnum.split(",");

    if (comma.length>1)
    {
        for(i=0;i<comma.length;i++)
        {
            setBackroundForLines(divid,comma[i], color);
        }
    }
    else
    {
       setBackroundForLines(divid,lnum, color);
    }
}

// unhighlight the lines - set the background back to transparent
var unhighlightLines=function(divid,lnum)
{
    processLines(divid,lnum,'transparent');
}

// highlight the lines - set the background to a yellow color
var highlightLines=function(divid,lnum)
{
    processLines(divid,lnum,'#ffff99');
}

// set the background to the passed color
var setBackroundForLines = function(divid,lnum,color)
{
    var hyphen=lnum.split("-");
    
    // if a range of lines
    if(hyphen.length > 1)
    {
        var start=parseInt(hyphen[0]);
        var end=parseInt(hyphen[1])+1;
        for(var k=start;k<end;k++)
            {
                //alert(k);
                var str="#"+divid+"_l"+k;
                if($(str).text() != "")
                  $(str).css('background-color',color);
                //$(str).effect("highlight",{},(dur*1000)+4500);
            }
    }
    else
    {
        //alert(lnum);
        var str="#"+divid+"_l"+lnum;
        $(str).css('background-color',color);
        //$(str).effect("highlight",{},(dur*1000)+4500);
    }
}
