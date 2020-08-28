
window.addEventListener("pageshow", function(_) {
    if(performance.navigation.type == 2) {
        location.reload(true);
    }
}); // Atualizar pagina quando voltar dos resultados (para ativar webcam)

function defineImageStyle(style) {
    document.getElementById("frameImg").style = style
}

function validateWebcam() {
    let got_image = ("{{ frame_status['success'] }}");
    if(got_image == "False") {
        messageInvalidWebcam()
    }
} // validação inicial de funcionamento da webcam

function messageInvalidWebcam() {
    title = "Problemas para configurar sua webcam &#128533;"
    body = `Infelizmente, não conseguimos obter imagens da sua webcam. 
        Por favor, verifique se a mesma está instalada e disponível para uso...`
    complement = `<button type="button" class="btn btn-lg btn-block btn-dark" onclick="location.reload(true);">
        Tentar novamente </button>`
    showMessage(title, body, complement);
}

function addEventToChangeWebcam() {
    document.getElementById("selectCurrentWebcam").setAttribute("onchange", "changeCurrentWebcam()");
}

async function changeCurrentWebcam () {
    try {
        let select = document.getElementById("selectCurrentWebcam");
        let response = await axios.post(`{{url_for("change_current_webcam")}}/${select.value}`);
        if(response == '' || response.data["success"] == false) {
            messageInvalidWebcam()
        } else {
            defineImageStyle(response.data["style"])
            $("#my-toast").remove();
        }
    } catch (error) {
        showErrorMessage(error);
    }
}

(() => {
    defineImageStyle("{{ frame_status['style'] }}");
    validateWebcam();
    addEventToChangeWebcam();
}) () // Função auto-executada
