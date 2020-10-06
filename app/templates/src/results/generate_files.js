(() => {
	document.getElementById('getAllImagesButton').setAttribute('onclick', 'getAllImages()');
	document.getElementById('getXlsxResultsButton').setAttribute('onclick', 'getXlsxResults()');
}) () //Função auto-executada

async function getAllImages() {
	try {
		document.getElementById('getAllImagesButton').disabled = true;
		let response = await axios.post('{{url_for("get_all_images")}}');
		if(response.data == "") {
			showError();
		} else {
			let headers = response.headers;
			let zip = response.data
			submitDownload(zip, headers['file-name'], headers['content-type'], headers['format']);
		}
	} catch (error) {
		showErrorMessage(error);
	} finally {
		document.getElementById('getAllImagesButton').disabled = false;
	}
}

async function getXlsxResults() {
	try {
		document.getElementById('getXlsxResultsButton').disabled = true;
		let response = await axios.post('{{url_for("get_xlsx_results")}}');
		if(response.data == '') {
			showError();
		} else {
			let headers = response.headers;
			submitDownload(response.data, headers['file-name'], headers['content-type'], headers['format']);
		}
	} catch (error) {
		showErrorMessage(error);
	} finally {
		document.getElementById('getXlsxResultsButton').disabled = false;
	}
}

function submitDownload(data, title, contentType, format) {
	let link = document.createElement('a');
	link.href = `data:${contentType};${format},${data}`;
	link.download = title;
	link.click();
}

function showError() {
	title = 'Falha no download do arquivo &#128533;'
	body = `Infelizmente, não foi possível fazer o download do arquivo solicitado. 
			Por favor, tente novamente mais tarde...`
	showMessage(title, body, undefined, true);
}
