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

function refresh_msg() {
	if (req.readyState != 4 || req.status != 200) {
		return;
	}
	msg_list = JSON.parse(req.responseText);
	
	for (var i = 0; i < msg_list.length; i++) {
		pk = msg_list[i]['pk'];
		sent = msg_list[i]['sent'];
		content = msg_list[i]['content'];
		
		if (document.getElementById("msg_"+pk)) {
			continue;
		}
		
		html_list = document.getElementById("chat_list");
		var new_msg = "<div class='chat_msg' id='msg_"+pk+"'> "+sent+": "+content+"</div>";
		html_list.innerHTML += new_msg;
	}
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

function send_chat(pk) {
	msg = document.getElementById("msg").value;
	if (msg == "") return;
	
	if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = refresh_msg;
    req.open("POST", "/medic/send_msg", true);
	req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	req.send("pk="+pk+"&msg="+msg+"&csrfmiddlewaretoken="+getCSRFToken());
	
	document.getElementById("msg").value = '';
}

function sendRequest(pk) {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = refresh_msg;
    req.open("POST", "/medic/get_msg", true);
	req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	req.send("pk="+pk+"&csrfmiddlewaretoken="+getCSRFToken());
}