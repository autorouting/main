$(document).ready(function() {
    $.getJSON(location.origin + "/cgi-bin/webgui.py" + location.search, function(data) {
            console.log(data);
    });
});