$(document).ready(function() {
    $.getJSON(location.origin + "/cgi-bin/webgui.py" + location.search, function(data) {
        switch (data.status) {
            case ("made_route"):
                document.querySelector("#loadingscreen").remove();
                document.querySelector("#finalscreen").style.display = "block";
                console.log(data);
                var solution_display = document.getElementById("solution_display");
                for (var i = 0; i < data.route_solution.length; i++) {
                  solution_display.innerHTML += `<tr><td>${i + 1}</td><td>${data.route_solution_nonformatted[i]}</td><td>${data.route_solution[i]}</td>`;
                }
                var route_link = data.route_link;
                var a = document.getElementById("route_link");
                a.href = route_link;
                var qrcode = document.getElementById("qrcode");
                qrcode.src = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=" + encodeURIComponent(route_link);
                break;
            case ("invalid_address"):
              console.log(data);
              document.querySelector("#containerbox").innerHTML = "";
              var solution_display = document.createElement("p");
              solution_display.innerHTML = data.errorMessage;
              document.querySelector("#containerbox").appendChild(solution_display);
              break;
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