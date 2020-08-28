(() => {
    document.getElementById("uploadImageInput").setAttribute("onchange", "onFileSelected(event)");
})() //Função auto-executada

function onFileSelected(event) {
    if(event.target.files.length === 0) return;

    var uploadedFile = event.target.files[0];
    var type = uploadedFile.type;
    if((type != "image/jpeg" && type != "image/png" && type != "image/bpm") || uploadedFile.name == "") {
        let body = "O arquivo enviado não é valido. Por favor, tente novamente...";
        showMessage("Arquivo inválido!", body, undefined, true);
        return;
    }
    
    var formData = new FormData();
    formData.append('file', uploadedFile);
    axios.post("{{url_for('upload_image')}}", formData);
    document.getElementById("startAnalyzeButton").disabled = true;
    configInputFile(uploadedFile.name);
}

function configInputFile(name) {
    document.getElementById("uploadImageInput").value = "";
    document.getElementById("uploadImageLabel").textContent = name;
}