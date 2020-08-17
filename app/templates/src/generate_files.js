document.getElementById("btn_get_zip_images").setAttribute("onclick", "get_zip_images()");
document.getElementById("btn_get_xlsx_results").setAttribute("onclick", "get_xlsx_results()");

async function get_zip_images() {
    let response = await axios.post("{{url_for('get_zip_images')}}");
    if(response.data == "") {
        showError();
        return;
    }

    let headers = response.headers;
    let imagesZip = await zipImages(response.data, headers["format"]);
    submitDownload(imagesZip, headers["file-name"], headers["content-type"], headers["format"])
}

async function zipImages(data, format) {
    let zip = new JSZip();
    for (let key of Object.keys(data)) {
        zip.file(key, data[key].replace("b'", "").replace("'", ""), {base64: true});
    }
    return await zip.generateAsync({type: format});
}

async function get_xlsx_results() {
    let response = await axios.post("{{url_for('get_xlsx_results')}}");
    if(response.data == "") {
        showError();
        return;
    }

    let headers = response.headers;
    submitDownload(response.data, headers['file-name'], headers["content-type"], headers["format"]);
}

function submitDownload(data, title, contentType, format) {
    let link = document.createElement('a');
    link.href = `data:${contentType};${format},${data}`;
    link.download = title;
    link.click();
}

function showError() {
    title = "Falha no download do arquivo &#128533;"
    body = `Infelizmente, não foi possível fazer o download do arquivo solicitado. 
        Por favor, tente novamente mais tarde...`
    show_message(title, body, undefined, true);
}
