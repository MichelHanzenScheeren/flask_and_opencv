function get_differentiator(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            document.getElementById("differentiator").innerHTML = xhttp.responseText;
        }
    };
    xhttp.open("POST", "{{ url_for('get_differentiator') }}", true);
    xhttp.send();
}