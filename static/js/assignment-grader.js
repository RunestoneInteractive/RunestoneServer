jQuery(document).ready(function(){
	jQuery('.gradable').on('click',function(event){
		event.preventDefault();
		var gradable = jQuery(this);
		if(gradable.data('acid') && gradable.data('student-id')){
			getGradingModal(gradable.parent(), gradable.data('acid'), gradable.data('student-id'));
		}
	});
	jQuery('.mass-grade').on('click', function(event){
		event.preventDefault();
		var btn = jQuery(this);
		if(btn.data('acid')){
			getMassGradingModal(btn.data('acid'));
		}
	})
});

function getGradingModal(element, acid, studentId){
	if(!eBookConfig.gradingURL){
		alert("Can't grade without a URL");
		return false;
	}

	function save(event){
		event.preventDefault();

		var form = jQuery(this);
		var grade = jQuery('#input-grade', form).val();
		var comment = jQuery('#input-comments', form).val();
		jQuery.ajax({
			url:eBookConfig.gradingURL,
			type:"POST",
			dataType:"JSON",
			data:{
				acid:acid,
				sid:studentId,
				grade:grade,
				comment:comment,
			},
			success:function(data){
				//alert("saved");
				jQuery('.grade',element).html(data.grade);
				jQuery('.comment',element).html(data.comment);
			}
		});
	}

	function show(data){
		// get rid of any other modals -- incase they are just hanging out.
		jQuery('.modal.modal-grader:not(#modal-template .modal)').remove();
		
		var modal_markup = jQuery('#modal-template').html();
		jQuery('body').append(modal_markup);
		var modal = jQuery('.modal.modal-grader:not(#modal-template .modal)');
		jQuery('.modal-title',modal).html(data.name+' <em>'+data.acid+'</em>');
		jQuery('.activecode-target',modal).attr('id',data.acid+"_"+data.username);
		jQuery('#input-grade',modal).val(data.grade);
		jQuery('#input-comments',modal).val(data.comment);
        // outerdiv, acdiv, sid, initialcode, language
		// for backward compatibility check for Factory otherwise use old function
		if (ACFactory) {
			ACFactory.addActiveCodeToDiv(data.acid, data.acid + "_" + data.username, data.username, null, data.lang);
		} else {
			createActiveCode(data.acid,null,data.username);
		}
		jQuery('form',modal).submit(save);
		jQuery('.next',modal).click(function(event){
			event.preventDefault();
			modal.on('hidden.bs.modal', function (e) {
				next_element = element.next();
				jQuery('form',modal).submit();
				jQuery('.gradable',next_element).click();
			});

			modal.modal('hide');
		});
		modal.modal('show');
		jQuery('#'+data.id).focus();
	}

	element.addClass("loading");
	jQuery.ajax({
		url:eBookConfig.gradingURL,
		type:"POST",
		dataType:"JSON",
		data:{
			acid:acid,
			sid:studentId,
		},
		success:function(data){
			show(data);
		}
	});
}

function getMassGradingModal(acid){
	// get rid of any other modals -- incase they are just hanging out.
	jQuery('.modal.modal-mass-grader:not(#mass-grade-modal-template .modal-mass-grader)').remove();

	var modal_markup = jQuery('#mass-grade-modal-template').html();
	jQuery('body').append(modal_markup);
	var modal = jQuery('.modal.modal-mass-grader:not(#mass-grade-modal-template .modal-mass-grader)');
	jQuery('.modal-title',modal).html(acid);

	jQuery('form',modal).submit(function(event){
		event.preventDefault();
		jQuery.ajax({
			url:eBookConfig.massGradingURL,
			type:"POST",
			dataType:"JSON",
			data:{
				acid:acid,
				csv:jQuery('textarea',modal).val()
			},
			success:function(data){
				if(!data['scores'] || data['scores'].length < 1){
					return False;
				}
				alert("saved");
				for(indx in data['scores']){
					var score = data['scores'][indx];
					var item = jQuery('.gradable[data-student-id="'+score['username']+'"][data-acid="'+score['acid']+'"]').parents('li:first');
					jQuery('.grade',item).html(score['grade']);
					jQuery('.comment',item).html(score['comment']);
				}
			}
		});
	});

	modal.modal('show');
}