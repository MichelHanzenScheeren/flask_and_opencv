function show_message(title = "", body = "", complement = "", autohide = false) {
    let message = ` <div id="my-toast" data-autohide="${autohide}" data-delay="3500" class="toast my-toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header bg-warning">
        <strong class="mr-auto text-dark"> ${title} </strong>
        <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
        </div>
        <div class="toast-body bg-warning">
            <p class="text-dark"> ${body} </p>
            ${complement}
        </div>
    </div>`
    $("#my-toast").remove();
    $("body").append(message);
    $("#my-toast").toast("show");
}

(() => {
    let got_image = ("{{ frame_controll['got_image'] }}");
    if(got_image == "False") {
        title = "Problemas para configurar sua webcam &#128533;"
        body = `Infelizmente, não conseguimos obter imagens da sua webcam. 
            Por favor, verifique se a mesma está instalada e disponível para uso...`
        complement = `<button type="button" class="btn btn-lg btn-block btn-dark" onclick="location.reload(true);">
            Tentar novamente </button>`
        show_message(title, body, complement);
    }
}) () // Função auto executada


$("#my-toast").on("hidden.bs.toast", function () {
    $("#my-toast").remove(); //remove da tela, para que não atrapalhe
}) 