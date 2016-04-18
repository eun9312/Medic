function select_chat(pk) {
	html_list = document.getElementById("chat_list");
	list_elem = html_list.getElementsByClassName("selection_elem");
	for (var i = 0; i < list_elem.length; i++) {
		list_elem[i].style.backgroundColor = "";
		list_elem[i].style.color = "";
	}
	selected_html = document.getElementById("chat_"+pk);
	selected_html.style.backgroundColor = "#056280";
	selected_html.style.color = "white";
	
	checkboxes = document.getElementById("hidden_checkboxes");
	checkboxes.innerHTML = "<input type='checkbox' name='selected' value='"+pk+"' checked>";	
}