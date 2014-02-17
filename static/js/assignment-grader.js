jQuery(document).ready(function(){
	jQuery('.gradable').on('click',function(event){
		event.preventDefault();
		var gradable = jQuery(this);
		if(gradable.data('acid') && gradable.data('student-id')){
			getGradingModal(gradable, gradable.data('acid'), gradable.data('student-id'));
		}
	});
});

function getGradingModal(bttn, acid, studentId){
	if(!eBookConfig.gradingURL){
		alert("Can't grade with out a URL");
		return false;
	}
	bttn.addClass("loading");
	jQuery.ajax({
		url:eBookConfig.gradingURL,
		type:"POST",
		dataType:"JSON",
		data:{
			acid:acid,
			sid:studentId,
		},
		success:function(data){
			showModal(data);
		}
	});
}

function showModal(data){
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
	modal.modal('show');
	jQuery('#'+data.id).focus();
}