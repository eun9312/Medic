function refresh_detail() {
	if (req.readyState != 4 || req.status != 200) {
		return;
	}
	
	detail_list = JSON.parse(req.responseText);
	html_list = document.getElementById("symptom_detail_list");
	inner_html = "";
	for (var i = 0; i < detail_list.length; i++) {
		detail_pk = detail_list[i]['pk'];
		detail_name = detail_list[i]['name'];
		detail_type = detail_list[i]['type'];
		inner_html += "<div class='selection_elem' id='detail_elem_"+detail_pk+"' onclick='select_detail("+detail_pk+", \""+detail_type+"\", \""+detail_name+"\")'>"+detail_type+": "+detail_name+"</div>"
	}
	html_list.innerHTML = inner_html;
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

function select_type(pk) {
	if (window.XMLHttpRequest) {
		req = new XMLHttpRequest();
	} else {
		req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	req.onreadystatechange = refresh_detail;
	req.open("POST", "/medic/get_detail_list", true);
	req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	req.send("pk="+pk+"&csrfmiddlewaretoken="+getCSRFToken());
	
	html_list = document.getElementById("symptom_type_list").getElementsByClassName("selection_elem");
	for (var i = 0; i < html_list.length; i++) {
		html_list[i].style.backgroundColor = ""
		html_list[i].style.color = "";
	}
	
	html_type = document.getElementById("type_elem_"+pk);
	html_type.style.backgroundColor = "#089CCB";
	html_type.style.color = "white";
}

function select_detail(pk, type, detail) {
	html_list = document.getElementById("your_list");
	new_html = "<div class='your_selection_elem' id='select_elem_"+pk+"' onclick='delete_elem("+pk+")'>"+type+": "+detail+"</div>";
	inner_html_list = html_list.getElementsByClassName("your_selection_elem");
	if (inner_html_list.length == 0) {
		html_list.innerHTML = new_html;
		checkboxes = document.getElementById("hidden_checkboxes");
		checkboxes.innerHTML = "<input class='checkbox' id='checkbox_elem_"+pk+"' type='checkbox' name='selected' value='"+pk+"' checked>";
	} else {
		already_present = false;
		for (var i = 0; i < inner_html_list.length; i++) {
			if (inner_html_list[i].id == 'select_elem_'+pk) {
				already_present = true;
			}
		}
		if (!already_present) {
			html_list.innerHTML += new_html;
			checkboxes = document.getElementById("hidden_checkboxes");
			checkboxes.innerHTML += "<input class='checkbox' id='checkbox_elem_"+pk+"' type='checkbox' name='selected' value='"+pk+"' checked>";
		}
	}	
}

function delete_elem(pk) {
	html_list = document.getElementById("your_list");
	inner_html_list = html_list.getElementsByClassName("your_selection_elem");
	for (var i = 0; i < inner_html_list.length; i++) {
		if (inner_html_list[i].id == 'select_elem_'+pk) {
			html_list.removeChild(inner_html_list[i]);
		}
	}
	checkboxes = document.getElementById("hidden_checkboxes");
	inner_checkboxes = checkboxes.getElementsByClassName("checkbox");
	for (var i = 0; i < inner_checkboxes.length; i++) {
		if (inner_checkboxes[i].id == 'checkbox_elem_'+pk) {
			checkboxes.removeChild(inner_checkboxes[i]);
		}
	}
}