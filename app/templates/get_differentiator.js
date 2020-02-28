function get_differentiator(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            var colors = JSON.parse(xhttp.responseText);
            document.getElementById("red").innerHTML = "Red: " + colors[0]
            document.getElementById("green").innerHTML = "Green: " + colors[1]
            document.getElementById("blue").innerHTML = "Blue: " + colors[2]
        }
    };
    xhttp.open("POST", "{{ url_for('get_differentiator') }}", true);
    xhttp.send();
}