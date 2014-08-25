/*global variable declarations*/
var myHighlightApplier;
var cssClassApplierModule = rangy.modules.CssClassApplier;
var range, sel, highlightAction = "save";
var highlightResponseText;
var extendHighlightClass;
var urlList;
var extendType;

function enableUserHighlights(){
	//check if it's not the contents or index page.
	if ((window.location.href).match( /(index.html|genindex.html|navhelp.html|toc.html)/ ) == null){
		//checksum generator for each div.section and paragraph. Add that checksum as a class _[checksumValue]
		$('body p, body .section').each(function(index) {
			var s = $(this).text();
			var i;
			var chk = 0;
			for (i = 0; i < s.length; i++) {
				chk += (s.charCodeAt(i)*i);
			}
			$(this).addClass("_"+chk);
		});

		// Get the completion status
		var currentPathname = window.location.pathname;
		if (currentPathname.indexOf("?") !== -1)
			currentPathname = currentPathname.substring(0, currentPathname.lastIndexOf("?"));
		var data = {lastPageUrl:currentPathname};
		jQuery.ajax({url: eBookConfig.ajaxURL+'getCompletionStatus',data: data, async: false}).done(function(data) {
			if (data !="None"){
				var completionData = $.parseJSON(data);
				var completionClass, completionMsg;
				if (completionData[0].completionStatus == 1){
					completionClass= "buttonConfirmCompletion";
					completionMsg= "<i class='glyphicon glyphicon-ok'></i> Completed. Well Done!";
				}
				else{
					completionClass= "buttonAskCompletion";
					completionMsg= "Mark as completed";
				}
				$("#main-content").append('<div style="text-align:center"><button class="btn btn-lg '+completionClass+'" id="completionButton">'+completionMsg+'</button></div>');
			}
		});


		var lastPositionVal = $.getUrlVar('lastPosition');
		if ( typeof lastPositionVal !== "undefined"){
			$("body").append('<img src="../_static/last-point.png" style="position:absolute; padding-top:55px; left: 10px; top: '+parseInt(lastPositionVal)+'px;"/>');
			$("html, body").animate({scrollTop: parseInt(lastPositionVal)}, 1000);
		}

		//Add the highlights on the page
		restoreSelection();

		//Add a container for highlights in the sidebar and populate
		$(".sphinxsidebarwrapper").append('<div id="highlightbox"><h3>My Highlights</h3><ul></ul></div>');
		updateHighlightBox();

		 var navLinkBgRightHiddenPosition = -$("#navLinkBgRight").outerWidth()-5;
		  var navLinkBgRightHalfOpen;
		  var navLinkBgRightFullOpen = 0;

		  if ($("#completionButton").hasClass("buttonAskCompletion")){
			navLinkBgRightHalfOpen = navLinkBgRightHiddenPosition + 70;
		  }
		  else if ($("#completionButton").hasClass("buttonConfirmCompletion")){
			navLinkBgRightHalfOpen = 0;
		  }
		  var relationsNextIconInitialPosition = $("#relations-next").css("right");
		  var relationsNextIconNewPosition = -(navLinkBgRightHiddenPosition + 35);

		  $("#navLinkBgRight").css("right", navLinkBgRightHiddenPosition).show();
		  var navBgShown = false;
		  $( window ).scroll(function() {
			  if($(window).scrollTop() + $(window).height() == $(document).height()) {
			   $("#navLinkBgRight").animate(
					{"right":navLinkBgRightHalfOpen},200
			   );
				$("#navLinkBgLeft").animate(
							{"left":"0px"},200
					   );
				if ($("#completionButton").hasClass("buttonConfirmCompletion")){
					$("#relations-next").animate({"right":relationsNextIconNewPosition},200);
				}
			   navBgShown = true;
		   }
		   else if (navBgShown){
				   $("#navLinkBgRight").animate(
					{"right":navLinkBgRightHiddenPosition},200
			   );
				   $("#navLinkBgLeft").animate(
					{"left":"-65px"},200
			   );
			   $("#relations-next").animate({"right":relationsNextIconInitialPosition});
			   navBgShown = false;
		   }
		  });

		  var completionFlag = 0 ;
          if ($("#completionButton").hasClass("buttonAskCompletion") ) {
              completionFlag = 0;
          } else {
              completionFlag = 1;
          }
		  $("#completionButton").on("click", function(){
			if ($(this).hasClass("buttonAskCompletion")){
				$(this).removeClass("buttonAskCompletion")
						.addClass("buttonConfirmCompletion")
						.html("<i class='glyphicon glyphicon-ok'></i> Completed. Well Done!");
				$("#navLinkBgRight").animate({"right":navLinkBgRightFullOpen});
				$("#relations-next").animate({"right":relationsNextIconNewPosition});
				navLinkBgRightHalfOpen = 0;
				completionFlag = 1;
			}
			else if ($(this).hasClass("buttonConfirmCompletion")){
				$(this).removeClass("buttonConfirmCompletion")
						.addClass("buttonAskCompletion")
						.html("Mark as completed");
				navLinkBgRightHalfOpen = navLinkBgRightHiddenPosition + 70;
				$("#navLinkBgRight").animate({"right":navLinkBgRightHalfOpen});
				$("#relations-next").animate({"right":relationsNextIconInitialPosition});
				completionFlag = 0;
			}
			processPageState(completionFlag);
		  });

		  $(window).on('beforeunload', function(e){
			if (completionFlag == 0){
				processPageState(completionFlag);
			}
		});


		$("body").append('<ul class="dropdown-menu" id="highlight-option-box" style="display:none;"><li><a href="javascript:void(0);" id="option-highlight-text" style="display:block;">Highlight</a></li></ul>');

		$('body .section').on("mouseup", function(evt) {
			sel = rangy.getSelection();
			if (typeof sel !== "undefined" && sel.anchorNode != null && sel.focusNode != null){
				var currAnchorNode = sel.anchorNode.parentElement;
				var currFocusNode = sel.focusNode.parentElement;
			}
			if (typeof sel === "undefined" || (sel.anchorOffset == sel.focusOffset) && sel.anchorNode == sel.focusNode) {
				$("#highlight-option-box").hide();
			}
			else if($(currAnchorNode).hasClass("my-highlighted-text") && $(currFocusNode).hasClass("my-highlighted-text")){
				sel.expand("word"); //expands selection to closest word only if user selects atleast one character
				highlightAction = "delete";
				toggleHighlightOptionBox(evt,"Delete Highlight");
			}
			else if($(sel.getRangeAt(0).getNodes([1])).hasClass("my-highlighted-text")){
				sel.expand("word");
				toggleHighlightOptionBox(evt,"Extend Highlight");
				if($(sel.getRangeAt(0).startContainer.parentElement).hasClass("my-highlighted-text")){ //extendEnd
					var classList = $(sel.getRangeAt(0).startContainer.parentElement).attr('class').split(/\s+/); //get all classes applied to anchor element
					extendType = "extendEnd";
				}
				else if($(sel.getRangeAt(0).endContainer.parentElement).hasClass("my-highlighted-text")){ //extendBeginning
					var classList = $(sel.getRangeAt(0).endContainer.parentElement).attr('class').split(/\s+/); //get all classes applied to focus element
					extendType = "extendBeginning";
				}
				else{ //extendBoth
					var classList = "";
					$(sel.getRangeAt(0).getNodes([1])).each(function(index, value) {
						if($(value).hasClass("my-highlighted-text")){
							classList = $(value).attr('class').split(/\s+/);
						}
					});
					extendType = "extendBoth";
				}
				extendHighlightClass = findHighlightClass(classList);
				highlightAction = "extend";
			}
			else if(!($(currAnchorNode).hasClass("my-highlighted-text") || $(currFocusNode).hasClass("my-highlighted-text"))){
					sel.expand("word");
					toggleHighlightOptionBox(evt,"Highlight");
					highlightAction = "save";
			}
		});

		$("#option-highlight-text").on('click', function(){
			$("#highlight-option-box").hide();
			switch(highlightAction){
				case "save":
				{
					var uniqueId = "hl"+saveSelection(sel);
					myHighlightApplier = rangy.createCssClassApplier("my-highlighted-text "+uniqueId, {normalize: true});
					myHighlightApplier.applyToSelection();
					$("."+uniqueId).first().attr("id",uniqueId);
					window.getSelection().removeAllRanges();
					updateHighlightBox();
					break;
				}
				case "delete":
				{
					var classList =$($(sel.anchorNode)[0].parentElement).attr('class').split(/\s+/); //get all classes applied to element
					var toDeleteHighlightClass = findHighlightClass(classList);
					range = rangy.createRange();
					myHighlightApplier = rangy.createCssClassApplier("my-highlighted-text", {normalize: true});
					$(".hl"+toDeleteHighlightClass).each(function() { //loop over all nodes with the given class and remove the my-highlighted-text class
						range.selectNodeContents(this);
						myHighlightApplier.undoToRange(range);
					});
					window.getSelection().removeAllRanges();
					toDelete = false;
					deleteHighlight(toDeleteHighlightClass);
					$(".hl"+toDeleteHighlightClass).attr("id","");
					$(".hl"+toDeleteHighlightClass).removeClass("hl"+toDeleteHighlightClass);
					updateHighlightBox();
					break;
				}
				case "extend":
				{
					var existingHighlight = $(".hl"+extendHighlightClass);
					var range = sel.getRangeAt(0);
					//expand the selection to include the original highlight based on if it is extendEnd or extendBeginning
					if (extendType == "extendEnd")
						range.setStartBefore(existingHighlight[0]);
					else if (extendType == "extendBeginning")
						range.setEndAfter(existingHighlight[existingHighlight.length -1]);
					sel.removeAllRanges(); //remove any existing ranges in selection
					sel.addRange(range); //add the new expanded range to selection
					//delete old highlight and save the expanded range as a new highlight
					$(existingHighlight).removeClass("my-highlighted-text");
					$(".hl"+extendHighlightClass).attr("id","");
					$(".hl"+extendHighlightClass).removeClass("hl"+extendHighlightClass);
					deleteHighlight(extendHighlightClass);
					var newExtendHighlightClass = saveSelection(sel);
					myHighlightApplier = rangy.createCssClassApplier("my-highlighted-text "+"hl"+newExtendHighlightClass, {normalize: true});
					myHighlightApplier.applyToSelection();
					$(".hl"+newExtendHighlightClass).first().attr("id","hl"+newExtendHighlightClass);
					window.getSelection().removeAllRanges();
					updateHighlightBox();
					break;
				}
			}
		});
	}
    // If this **is** the toc then we want to add a link to last known position.
	// As well as add either an orange in progress bullet or a checkmark on
	// in-progress or completed sections.
	else if ((window.location.href).toLowerCase().indexOf("toc.html") != -1 ||
             (window.location.href).toLowerCase().indexOf("index.html") != -1) {
		jQuery.get(eBookConfig.ajaxURL+'getAllCompletionStatus', function(data) {
			if (data !="None"){
				subChapterList = $.parseJSON(data);

				var allSubChapterURLs = $("#main-content div li a");
				$.each( subChapterList, function(index, item){
					for (var s = 0; s < allSubChapterURLs.length; s++){
						if (allSubChapterURLs[s].href.indexOf(item.chapterName+"/"+item.subChapterName) != -1){
							if (item.completionStatus == 1)
								$(allSubChapterURLs[s].parentElement).addClass("completed").append('<span class="infoTextCompleted">- Completed this topic on '+item.endDate+"</span>").children().first().hover(
									 function() {
										$( this ).next(".infoTextCompleted").show();
									  }, function() {
										$( this ).next(".infoTextCompleted").hide()
									  }
								);
							else if(item.completionStatus == 0)
								$(allSubChapterURLs[s].parentElement).addClass("active").append('<span class="infoTextActive">Last read this topic on '+item.endDate+"</span>").children().first().hover(
									 function() {
										$( this ).next(".infoTextActive").show();
									  }, function() {
										$( this ).next(".infoTextActive").hide()
									  }
								);
						}
					}
				});

			}
		});
		data = {course:eBookConfig.course};
		jQuery.get(eBookConfig.ajaxURL+'getlastpage', data, function(data) {
			if (data !="None"){
				lastPageData = $.parseJSON(data);
				if (lastPageData[0].lastPageChapter != null){
                    $("#continue-reading").show().html('<div id="jump-to-chapter" class="alert alert-info" ><strong>You were Last Reading:</strong> '+lastPageData[0].lastPageChapter+ ((lastPageData[0].lastPageSubchapter) ? ' &gt; '+lastPageData[0].lastPageSubchapter : "")+' <a href="'+lastPageData[0].lastPageUrl+'?lastPosition='+lastPageData[0].lastPageScrollLocation+'">Continue Reading</a></div>');
				}
			}
		});

	}
};

function findHighlightClass(classList){
	var className;
	$.each( classList, function(index, item){
			if (item.indexOf("hl") !== -1) { //locate class with hl
			   className = item;
			}
	});
	return className.replace("hl","");
}

function toggleHighlightOptionBox(event, highlightOptionName){
	$("#option-highlight-text").text(highlightOptionName);
	$("#highlight-option-box").show().offset({
		top: event.pageY + 5,
		left: event.pageX + 5
	});
}

//function to process the selection made by the user to identify the range and the parent selector. Calls function saveHighlight
function saveSelection(sel) {
		var parentNode = sel._ranges[0].commonAncestorContainer;
		var parentSelectorClass;
		while(!(($(parentNode).is("p") || $(parentNode).is("div")) && $(parentNode).attr('class'))){
			parentNode = $(parentNode)[0].parentElement;
		}
		$.each($(parentNode).attr('class').split(' '), function(index, value) {
			if (value.indexOf("_") == 0){
				parentSelectorClass = value;
			}
		});
		var currentRange = sel.saveCharacterRanges(parentNode);
		if(currentRange.length > 1){
			currentRange[0].range.end = currentRange[currentRange.length -1].range.end;
			var tempRange = currentRange.slice(0,1);
			currentRange = tempRange;
		}
		var serializedRange = JSON.stringify(currentRange);
		return saveHighlight(parentSelectorClass,serializedRange,"self");
}

//function called to save a new highlight
function saveHighlight(parentSelectorClass,serializedRange,saveMethod) {
	var currPage = window.location.pathname;
	var newId;
	var currSection = window.location.pathname+window.location.hash;
    var data = {parentClass:parentSelectorClass, range:serializedRange, method:saveMethod, page:currPage, pageSection: currSection, course:eBookConfig.course};
    $(document).ajaxError(function(e,jqhxr,settings,exception){
        console.log("Request Failed for "+settings.url);
    });
    jQuery.ajax({url: eBookConfig.ajaxURL+'savehighlight',data: data, async: false}).done(function(returndata) {
		newId = returndata;
	});
    if (eBookConfig.logLevel > 0){
        logBookEvent({'event':'highlight','act': 'save', 'div_id':currPage}); // Log the run event
    }
	return newId;
}

//function called to delete an existing highlight
function deleteHighlight(uniqueId) {
	var currPage = window.location.pathname;
    var data = {uniqueId: uniqueId};
    $(document).ajaxError(function(e,jqhxr,settings,exception){
        console.log("Request Failed for"+settings.url)
    });
    jQuery.post(eBookConfig.ajaxURL+'deletehighlight',data);
    if (eBookConfig.logLevel > 0){
        logBookEvent({'event':'highlight','act': 'delete', 'div_id':currPage}); // Log the run event
    }

}

//add links to the highlights in sidebar on the right. Function called on page load and every edit of highlight
function updateHighlightBox() {
	$("#highlightbox ul").html("");
	var highlightJumpText = "";
	var highlightLink;
	var processingHighlight = false;
	$("body .my-highlighted-text").each(function(index,value){
		if($(value).attr("id")){
			if (processingHighlight){
				highlightJumpText = highlightJumpText.split(/\s+/, 12).join(" ")+"...";
				$("#highlightbox ul").append("<li><a class='sidebar-highlights' href='"+window.location.pathname+"#"+highlightLink+"'>"+highlightJumpText+"</a></li><br/>");
			}
			highlightJumpText = "";
			highlightLink = $(value).attr("id");
			if ($(value)[0].firstChild)
				highlightJumpText += $(value)[0].firstChild.textContent;
			else
				highlightJumpText +=$(value)[0].textContent;
			processingHighlight = true;
		}
		else{
			if ($(value)[0].firstChild)
				highlightJumpText += $(value)[0].firstChild.textContent;
			else
				highlightJumpText +=$(value)[0].textContent;
		}
	});
	if (processingHighlight){
		highlightJumpText = highlightJumpText.split(/\s+/, 12).join(" ")+"...";
		$("#highlightbox ul").append("<li><a class='sidebar-highlights' href='"+window.location.pathname+"#"+highlightLink+"'>"+highlightJumpText+"</a></li><br/>");
	}
}

//function called at load time to fetch all highlights from database for the user and rendered on the page
function restoreSelection() {
	rangy.init();
	var currPage = window.location.pathname;
	var data = {page: currPage ,course:eBookConfig.course};
	jQuery.ajax({url: eBookConfig.ajaxURL+'gethighlights',data: data, async: false}).done(function(data) {
		highlightResponseText = $.parseJSON(data);
		var parentClassName, uniqueId;
		$.each(highlightResponseText, function(index, value) {
			parentClassName = "."+value.parentClass;
			highlightClassName = "hl"+value.uniqueId;
			rangy.getSelection().restoreCharacterRanges($(parentClassName)[0], $.parseJSON(value.range));
			myHighlightApplier = rangy.createCssClassApplier("my-highlighted-text "+highlightClassName, {normalize: true});
			myHighlightApplier.toggleSelection();
			$("."+highlightClassName).first().attr("id",highlightClassName);
			window.getSelection().removeAllRanges();
		});
	});
}

function processPageState(completionFlag){
	/*Log last page visited*/
	var currentPathname = window.location.pathname;
	if (currentPathname.indexOf("?") !== -1)
		currentPathname = currentPathname.substring(0, currentPathname.lastIndexOf("?"));
	var data = {lastPageUrl:currentPathname, lastPageScrollLocation: $(window).scrollTop(), completionFlag:completionFlag, course:eBookConfig.course};
	$(document).ajaxError( function(e,jqhxr,settings,exception) {
        console.log("Request Failed for "+settings.url)
    } );
	jQuery.ajax({url: eBookConfig.ajaxURL+'updatelastpage',data: data,  async: false});
}

$.extend({
  getUrlVars: function(){
    var vars = [], hash;
    var hashes = window.location.search.slice(window.location.search.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }
    return vars;
  },
  getUrlVar: function(name){
    return $.getUrlVars()[name];
  }
});
