
window.addEventListener("pageshow", function(_) {
    if(performance.navigation.type == 2) {
        location.reload(true);
    }
});

(() => {
    let got_image = ("{{ frame_controll['success'] }}");
    if(got_image == "False") {
        title = "Problemas para configurar sua webcam &#128533;"
        body = `Infelizmente, não conseguimos obter imagens da sua webcam. 
            Por favor, verifique se a mesma está instalada e disponível para uso...`
        complement = `<button type="button" class="btn btn-lg btn-block btn-dark" onclick="location.reload(true);">
            Tentar novamente </button>`
        show_message(title, body, complement);
    }
}) () // Função auto executada
