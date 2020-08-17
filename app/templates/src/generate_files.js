document.getElementById("btn_get_all_images").setAttribute("onclick", "get_all_images()");
document.getElementById("btn_get_xlsx_results").setAttribute("onclick", "get_xlsx_results()");

async function get_all_images() {
    document.getElementById("btn_get_all_images").disabled = true;
    let response = await axios.post("{{url_for('get_all_images')}}");
    if(response.data == "") {
        showError();
    } else {
        let headers = response.headers;
        let imagesZip = await zipImages(response.data, headers["format"]);
        submitDownload(imagesZip, headers["file-name"], headers["content-type"], headers["format"]);
    }
    document.getElementById("btn_get_all_images").disabled = false;
}

async function zipImages(data, format) {
    let zip = new JSZip();
    for (let key of Object.keys(data)) {
        zip.file(key, data[key].replace("b'", "").replace("'", ""), {base64: true});
    }
    return await zip.generateAsync({type: format});
}

async function get_xlsx_results() {
    document.getElementById("btn_get_xlsx_results").disabled = true;
    let response = await axios.post("{{url_for('get_xlsx_results')}}");
    if(response.data == "") {
        showError();
    } else {
        let headers = response.headers;
        submitDownload(response.data, headers['file-name'], headers["content-type"], headers["format"]);
    }
    document.getElementById("btn_get_xlsx_results").disabled = false;
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
