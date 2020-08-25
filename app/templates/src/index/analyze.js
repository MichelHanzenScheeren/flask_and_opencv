document.getElementById("buttonGetDifferentiator").setAttribute("onclick", "get_differentiator()");

function config_analyze() {
    document.getElementById("buttonGetDifferentiator").disabled = true;
    document.getElementById("refresh_button").disabled = true;
    document.getElementById("clear_button").disabled = true;
    document.getElementById("div1").style.display = "none";
    document.getElementById("div2").style.display = "block";
}

async function get_differentiator(){
    let response = await axios.post("{{ url_for('get_differentiator') }}");
    if(response.data == "" || response.data[0] == "[") {
        failed_to_get_differentiator();
        return;
    }
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

function failed_to_get_differentiator() {
    title = "Problemas para calcular o diferenciador &#128533;"
    body = `Infelizmente, não conseguimos calcular o diferenciador. 
        Por favor, verifique a solicitação e tente novamente...
        Se isso não funcionar, tente recarregar a página.`
    complement = `<button type="button" class="btn btn-lg btn-block btn-dark" onclick="location.reload(true);">
        Atualizar página </button>`
    show_message(title, body, complement, true);
}


