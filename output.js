var data;
var xhr = new XMLHttpRequest();
xhr.responseType = "text";
xhr.onload = function(e) {
    data = JSON.parse(this.responseText);
    console.log(data);
};
xhr.open("GET", "/cgi-bin/webgui.py" + location.search, true);
xhr.responseType = "document";
xhr.send();