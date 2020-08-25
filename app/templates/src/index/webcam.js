
window.addEventListener("pageshow", function(_) {
    if(performance.navigation.type == 2) {
        location.reload(true);
    }
});

(() => {
    let got_image = ("{{ frame_controll['success'] }}");
    if(got_image == "False") {
        message_invalid_webcam()
    }
}) () // função auto executada (validação inicial de funcionamento da webcam)

function message_invalid_webcam() {
    title = "Problemas para configurar sua webcam &#128533;"
    body = `Infelizmente, não conseguimos obter imagens da sua webcam. 
        Por favor, verifique se a mesma está instalada e disponível para uso...`
    complement = `<button type="button" class="btn btn-lg btn-block btn-dark" onclick="location.reload(true);">
        Tentar novamente </button>`
    show_message(title, body, complement);
}

let selectWebcam = document.getElementById("select-webcam");
selectWebcam.setAttribute("onchange", "changeCurrentWebcam()");
async function changeCurrentWebcam () {
    let response = await axios.post(`{{url_for("change_current_webcam")}}/${selectWebcam.value}`);
    if(response.data["success"] == false) {
        message_invalid_webcam()
    } else {
        $("#my-toast").remove();
    }
}