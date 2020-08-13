document.getElementById("buttonGetDifferentiator").setAttribute("onclick", "get_differentiator()");

window.addEventListener("pageshow", function(_) {
    if(performance.navigation.type == 2) {
        location.reload(true);
    }
});

function config_analyze() {
    document.getElementById("buttonGetDifferentiator").disabled = true;
    document.getElementById("refresh_button").disabled = true;
    document.getElementById("clear_button").disabled = true;
    document.getElementById("div1").style.display = "none";
    document.getElementById("div2").style.display = "block";
}

async function get_differentiator(){
    let response = await axios.post("{{ url_for('get_differentiator') }}");
    if(response.data[0] == "[") return;
    document.getElementById("red").innerHTML = "Red: " + response.data[0];
    document.getElementById("green").innerHTML = "Green: " + response.data[1];
    document.getElementById("blue").innerHTML = "Blue: " + response.data[2];
    document.getElementById("start").disabled = false;

    get_differentiator_image()
}

async function get_differentiator_image() {
    let response = await axios.post("{{ url_for('get_differentiator_image') }}");
    if(response.data == "") return; 

    let differentiator_image = document.getElementById("differentiator_image")
    differentiator_image.setAttribute("src", "data:image/jpeg;base64," + response.data);
}

(() => {
    let got_image = ("{{ frame_controll['got_image'] }}");
    if(got_image == "False") {
        $(".toast").toast("show");
    } else {
        document.getElementById("my-toast").innerHTML = "" //remove da tela, para que não atrapalhe
    }
}) () // Função auto executada

$('.toast').on('hidden.bs.toast', function () {
    let my_toast = document.getElementById("my-toast");
    if(my_toast == undefined) return;
    my_toast.innerHTML = ""  //remove da tela, para que não atrapalhe
}) 


