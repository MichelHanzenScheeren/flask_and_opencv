document.getElementById("btn_generate_files").setAttribute("onclick", "get_zip_images()");
async function get_zip_images() {
    let response = await axios.post("{{url_for('get_zip_images')}}");
    let type =  "application/zip";
    let blob = new Blob([response.data], { type });
    let link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = "capsule.zip";
    link.click();
}