jQuery(document).ready(function(){
	jQuery('.gradable').on('click',function(event){
		event.preventDefault();
		var gradable = jQuery(this);
		if(gradable.data('acid') && gradable.data('student-id')){
			getGradingModal(gradable.parent(), gradable.data('acid'), gradable.data('student-id'));
		}
	});
});

function getGradingModal(element, acid, studentId){
	if(!eBookConfig.gradingURL){
		alert("Can't grade with out a URL");
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
				alert("saved");
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
		jQuery('.modal-title',modal).html(data.name);
		jQuery('.activecode-target',modal).attr('id',data.id);
		jQuery('.input-grade',modal).val(data.grade);
		jQuery('.input-comment',modal).val(data.comment);

		createActiveCode(data.id,data.code);
		jQuery('form',modal).submit(save);
		jQuery('.next',modal).click(function(event){
			event.preventDefault();
			modal.on('hidden.bs.modal', function (e) {
				next_element = element.next();
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