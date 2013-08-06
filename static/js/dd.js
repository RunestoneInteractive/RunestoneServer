

function allowDrop(ev)
{
   ev.preventDefault();
}

function drag(ev)
{
   ev.dataTransfer.setData("Text",ev.target.id);
   return true;
}

function drop(ev)
{
   var data=ev.dataTransfer.getData("Text");
   ev.target.appendChild(document.getElementById(data));
   ev.preventDefault();
}

function dragDefine(ev) {
	ev.dataTransfer.effectAllowed = 'move';
	ev.dataTransfer.setData("text/plain", ev.target.getAttribute('id'));
	ev.dataTransfer.setDragImage(ev.target, 0, 0);
	return true;
}

function addModBlock()
{
    var cboxes = document.getElementById("chapterboxes");
    var divelement = document.createElement('div');
    
    divelement.setAttribute("id","box2");
    divelement.setAttribute("class","boxclass");
    divelement.setAttribute("ondrop","drop(event)" );
    divelement.setAttribute("ondragover","allowDrop(event)");
    divelement.innerHTML='<input id="title" type="text" placeholder="Your section title here" name="label" />';
    
    cboxes.appendChild(divelement)
}

function displayContents()
{
   var cdiv = document.getElementById("chapterboxes");
   txt="";
   var cchildren = cdiv.childNodes;
   
   var bchildren = cchildren[1].childNodes;

   var txt=txt+bchildren[1].value + "<br/>";

   for (var i=3; i<bchildren.length; i++)
      {
        txt=txt + "ID="+bchildren[i].id +" "+ bchildren[i].innerHTML + "<br/>";
      }

   for (var c=3; c<cchildren.length; c=c+1)
   {
      var bchildren = cchildren[c].childNodes

      var txt=txt+bchildren[0].value + "<br/>";

      for (var i=1; i<bchildren.length; i++)
      {
        txt=txt + "ID="+bchildren[i].id +" "+ bchildren[i].innerHTML + "<br/>";
      };
   }
   var x=document.getElementById("output");  
   x.innerHTML=txt;
}

function buildSuccess(data,status,ignore) {
    var iid = setInterval(function() {
        d = {
             task_name:data.task_name,
             course_url:data.course_url
            };
        $.post(eBookConfig.ajaxURL+'getSphinxBuildStatus.json', d, function(retdata) {
            if (retdata.status == "true") {
                window.location.href = retdata.course_url;
            }
            if (retdata.status == "failed") {
                clearInterval(iid);
                $("#spinner").hide();
                $("#title").text("An error occurred.");
                $("#message").html("An error occurred while rebuilding this course. Please check that you are not attempting " +
                    "to rebuild a course that you do not have permission for. If you are sure that you are registered for the correct " +
                    "course, please submit an error report <a href='https://github.com/bnmnetp/runestone/issues/new'>here</a>. " +
                    "Make sure you include the following traceback information:" +
                    "<pre>" + retdata.traceback + "</pre>");
            }
        });
    }, 3000);
}

function buildIndexFile(projname, startdate, loginreq) {
    var cdiv = document.getElementById("chapterboxes");

    var txt="";
    var cchildren = cdiv.childNodes;
    var bchildren = cchildren[1].childNodes;

    txt=txt+bchildren[1].value + " ";

    for (var i=3; i<bchildren.length; i++) {
        txt=txt + bchildren[i].getAttribute("data-filename") + " ";
    }
   
    for (var c=3; c<cchildren.length; c=c+1) {
        var bchildren = cchildren[c].childNodes;

        var txt=txt+bchildren[0].value + " ";

        for (var i=1; i<bchildren.length; i++) {
            txt=txt + bchildren[i].getAttribute("data-filename") + " ";
        }
    }

    data = {};
    data.coursetype='custom';
    data.loginreq = loginreq;
    data.projectname=projname;
    data.startdate = startdate;
    data.toc=txt;
    jQuery.post(eBookConfig.app +'/designer/build_custom.json',data,buildSuccess)
}

function displayItems(boxid)
{
   var bdiv = document.getElementById(boxid)
   var bchildren = bdiv.childNodes

   var txt=bchildren[1].value + "<br/>";
   console.log(bchildren.length)
   for (var i=3; i<bchildren.length; i++)
   {
     txt=txt + "ID="+bchildren[i].id +" "+ bchildren[i].innerHTML + "<br/>";
   };
   var x=document.getElementById("output");  
   x.innerHTML=txt;
}

function showDetails(dbid)
{
    console.log(dbid)
}

addH1 = function(theText)
{
   var newh1 = document.createElement("h1")
   newh1.innerHTML = theText
   document.body.appendChild(newh1)
}

