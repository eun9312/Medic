$("input.is_doctor").on( "click", function() {
	if ($("input:checked").val() == 'doctor') {
		$("#doctor_register").css("display", "block");
	} else {
		$("#doctor_register").css("display", "none");
	}
});

document.getElementById("uploadBtn1").onchange = function () {
    document.getElementById("uploadFile1").value = this.value;
};

document.getElementById("uploadBtn2").onchange = function () {
    document.getElementById("uploadFile2").value = this.value;
};