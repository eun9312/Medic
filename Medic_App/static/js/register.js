$("input.is_doctor").on( "click", function() {
	if ($("input:checked").val() == 'doctor') {
		$("#doctor_register").css("display", "block");
	} else {
		$("#doctor_register").css("display", "none");
	}
});