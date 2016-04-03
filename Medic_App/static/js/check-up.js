function refresh_detail() {
	if (req.readyState != 4 || req.status != 200) {
		return;
	}
	
	detail_list = JSON.parse(req.responseText);
	html_list = document.getElementById("symptom_detail_list");
	inner_html = "";
	for (var i = 0; i < detail_list.length; i++) {
		detail_name = detail_list[i]['name'];
		detail_type = detail_list[i]['type'];
		inner_html += "<div class='selection_elem' onclick='select_detail(\""+detail_type+"\",\""+detail_name+"\")'>"+detail_type+": "+detail_name+"</div>"
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

function select_type(type) {
	if (window.XMLHttpRequest) {
		req = new XMLHttpRequest();
	} else {
		req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	req.onreadystatechange = refresh_detail;
	req.open("POST", "/medic/get_detail_list", true);
	req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	req.send("type="+type+"&csrfmiddlewaretoken="+getCSRFToken());
	
	html_list = document.getElementById("symptom_type_list").getElementsByClassName("selection_elem");
	for (var i = 0; i < html_list.length; i++) {
		html_list[i].style.backgroundColor = ""
		html_list[i].style.color = "";
	}
	
	html_type = document.getElementById("type_elem_"+type);
	html_type.style.backgroundColor = "#089CCB";
	html_type.style.color = "white";
}

function select_detail(type, detail) {
	html_list = document.getElementById("your_list");
	new_html = "<div class='your_selection_elem' onclick='delete_elem(\""+type+"\", \""+detail+"\")'>"+type+": "+detail+"</div>";
	inner_html_list = html_list.getElementsByClassName("your_selection_elem");
	if (inner_html_list.length == 0) {
		html_list.innerHTML = new_html;
	} else {
		already_present = false;
		for (var i = 0; i < inner_html_list.length; i++) {
			if (inner_html_list[i].innerHTML == type+": "+detail) {
				already_present = true;
			}
		}
		if (!already_present) {
			html_list.innerHTML += new_html;
		}
	}	
}

function delete_elem(type, detail) {
	html_list = document.getElementById("your_list");
	inner_html_list = html_list.getElementsByClassName("your_selection_elem");
	for (var i = 0; i < inner_html_list.length; i++) {
		if (inner_html_list[i].innerHTML == type+": "+detail) {
			html_list.removeChild(inner_html_list[i]);
		}
	}
}