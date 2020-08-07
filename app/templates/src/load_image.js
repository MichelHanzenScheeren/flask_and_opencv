document.getElementById("buttonUploadImage").setAttribute("onclick", "configureButtonToInputClick()");
document.getElementById("inputUploadImage").setAttribute("onchange", "onFileSelected(event)");

function configureButtonToInputClick() { 
    document.getElementById("inputUploadImage").click();
}

function onFileSelected(event) {
    if(event.target.files.length === 0) return;

    var uploadedFile = event.target.files[0];
    var type = uploadedFile.type;
    if(type != "image/jpeg" && type != "image/png" && type != "image/bpm") return;
    if(uploadedFile.name == "") return;
    
    var formData = new FormData();
    formData.append('file', uploadedFile);
    axios.post("{{url_for('upload_image')}}", formData);
    document.getElementById("start").disabled = true;
}