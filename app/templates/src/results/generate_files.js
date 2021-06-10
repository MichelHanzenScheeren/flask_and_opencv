(() => {
	document.getElementById('getAllImagesButton').setAttribute('onclick', 'getAllImages()');
	document.getElementById('getXlsxResultsButton').setAttribute('onclick', 'getXlsxResults()');
	document.getElementById('getProgrammingJsonButton')?.setAttribute('onclick', 'getProgrammingJson()');
})() //Função auto-executada

function getAllImages() {
	document.getElementById('getAllImagesButton').disabled = true;
	axios.post('{{url_for("get_all_images")}}').then(function (response) {
		let headers = response.headers;
		let zip = response.data
		submitDownload(zip, headers['file-name'], headers['content-type'], headers['format']);
	}).catch(showErrorMessage).then(function () {
		document.getElementById('getAllImagesButton').disabled = false;
	});
}

function getXlsxResults() {
	document.getElementById('getXlsxResultsButton').disabled = true;
	axios.post('{{url_for("get_xlsx_results")}}').then(function (response) {
		let headers = response.headers;
		submitDownload(response.data, headers['file-name'], headers['content-type'], headers['format']);
	}).catch(showErrorMessage).then(function () {
		document.getElementById('getXlsxResultsButton').disabled = false;
	});
}

function getProgrammingJson() {
	document.getElementById('getProgrammingJsonButton').disabled = true;
	axios.post('{{url_for("download_programming")}}').then(function (response) {
		let title = response["headers"]["content-disposition"]?.split('=')[1] ?? 'file.json';
		let data = encodeURIComponent(JSON.stringify(response.data));
		submitDownload(data, title, response["headers"]["content-type"], 'charset=utf-8');
	}).catch(showErrorMessage).then(function () {
		document.getElementById('getProgrammingJsonButton').disabled = false;
	});
}

function submitDownload(data, title, contentType, format) {
	let link = document.createElement('a');
	link.href = `data:${contentType};${format},${data}`;
	link.download = title;
	link.click();
}
