document.getElementById("btn_generate_files").setAttribute("onclick", "get_zip_images()");

async function get_zip_images() {
    let response = await axios.post("{{url_for('get_zip_images')}}");
    var zip = new JSZip();
    for (let [key, value] of Object.entries(response.data)) {
        let img = value.replace("b'", "").replace("'", "");
        zip.file(key, img, {base64: true});
    }
    let zip_file = await zip.generateAsync({type: "base64"});
    let link = document.createElement('a');
    link.href = "data:application/zip;base64," + zip_file;
    link.download = "images.zip";
    link.click();
}
