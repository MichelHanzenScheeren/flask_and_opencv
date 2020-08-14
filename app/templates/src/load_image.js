document.getElementById("inputUploadImage").setAttribute("onchange", "onFileSelected(event)");

function onFileSelected(event) {
    if(event.target.files.length === 0) return;

    var uploadedFile = event.target.files[0];
    var type = uploadedFile.type;
    if((type != "image/jpeg" && type != "image/png" && type != "image/bpm") || uploadedFile.name == "") {
        let body = "O arquivo enviado não é valido. Por favor, tente novamente...";
        show_message("Arquivo inválido!", body, undefined, true);
        return;
    }
    
    var formData = new FormData();
    formData.append('file', uploadedFile);
    axios.post("{{url_for('upload_image')}}", formData);
    document.getElementById("start").disabled = true;
    config_input_file(uploadedFile.name);
}

function config_input_file(name) {
    document.getElementById("inputUploadImage").value = "";
    document.getElementById("labelUploadImage").textContent = name;
}