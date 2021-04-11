$(document).ready(function() {
    $.getJSON(location.origin + "/cgi-bin/webgui.py" + location.search, function(data) {
        switch (data.status) {
            case ("made_route"):
                document.querySelector("#containerbox").innerHTML = "";
                console.log(data);
                var solution_display = document.createElement("p");
                solution_display.innerHTML = data.route_solution;
                document.querySelector("#containerbox").appendChild(solution_display);
                var route_link = decodeURIComponent(data.route_link);
                var a = document.createElement("a");
                a.href = route_link;
                a.innerText = "Open Google Maps link";
                document.querySelector("#containerbox").appendChild(a);
                var br = document.createElement("br");
                document.querySelector("#containerbox").appendChild(br);
                var qrcode = new Image();
                qrcode.src = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=" + data.route_link;
                document.querySelector("#containerbox").appendChild(qrcode);
                break;
            case ("invalid_address"):
              document.querySelector("#containerbox").innerHTML = "";
              var solution_display = document.createElement("p");
              solution_display.innerHTML = data.route_solution;
              document.querySelector("#containerbox").appendChild(solution_display);
        }
    });
});

var i = 0;
function startLoadingBar() {
  if (i == 0) {
    i = 1;
    var elem = document.getElementById("loadingBar");
    var width = 1;
    var id = setInterval(move, 8);
    function move() {
      if (width >= 100) {
        clearInterval(id);
        i = 0;
      } 
      
      else {
        width += (100 - width) ** 1.2 / 90 ** 1.2;
        elem.style.width = width + "px";
                
      }
    }
  }
}

startLoadingBar()