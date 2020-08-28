
window.addEventListener("pageshow", function(_) {
    if(performance.navigation.type == 2) {
        location.reload(true);
    }
}); // Atualizar pagina quando voltar dos resultados (para ativar webcam)

function defineImageStyle(style) {
    document.getElementById("desenho").style = style
}

function validateWebcam() {
    let got_image = ("{{ frame_status['success'] }}");
    if(got_image == "False") {
        message_invalid_webcam()
    }
} // validação inicial de funcionamento da webcam

function message_invalid_webcam() {
    title = "Problemas para configurar sua webcam &#128533;"
    body = `Infelizmente, não conseguimos obter imagens da sua webcam. 
        Por favor, verifique se a mesma está instalada e disponível para uso...`
    complement = `<button type="button" class="btn btn-lg btn-block btn-dark" onclick="location.reload(true);">
        Tentar novamente </button>`
    show_message(title, body, complement);
}

function addEventToChangeWebcam() {
    document.getElementById("select-webcam").setAttribute("onchange", "changeCurrentWebcam()");
}

async function changeCurrentWebcam () {
    let response = await axios.post(`{{url_for("change_current_webcam")}}/${document.getElementById("select-webcam").value}`);
    if(response == '' || response.data["success"] == false) {
        message_invalid_webcam()
    } else {
        defineImageStyle(response.data["style"])
        $("#my-toast").remove();
    }
}

defineImageStyle("{{ frame_status['style'] }}")
validateWebcam()
addEventToChangeWebcam()
