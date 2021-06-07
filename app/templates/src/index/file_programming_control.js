(() => {
  document.getElementById('uploadUserProgrammingInput').setAttribute('onchange', 'onFileSelected(event)');
})() //Função auto-executada

function onFileSelected(event) {
  if (_isValidJsonFile(event)) {
    let uploadedFile = event.target.files[0];
    let reader = new FileReader();
    reader.onload = onFileRead;
    reader.readAsText(uploadedFile);
    configInputFile(uploadedFile.name);
  }
}

function _isValidJsonFile(event) {
  if (event.target.files.length === 0) return false;
  let uploadedFile = event.target.files[0];
  if (uploadedFile.type != 'application/json' || uploadedFile.name == '') {
    var body = 'O arquivo selecionado não corresponde a um json válido para a programação das válvulas.';
    showMessage('Arquivo inválido', body);
    return false;
  }
  return true;
}

function onFileRead(event) {
  let converterJson = JSON.parse(event.target.result);
  axios.post('{{url_for("upload_user_programming")}}', converterJson).then(function (response) {
    addNewHtmlContent(response.data['data']);
  }).catch(showErrorMessage);
}

function addNewHtmlContent(html) {
  $('#programmingDataDiv').remove();
  $('#modalBody').append(html);
  $('#openProgrammingModal').html('Editar programação');
  savedProgramming = true;
}

function configInputFile(name) {
  document.getElementById('uploadUserProgrammingInput').value = '';
  document.getElementById('uploadUserProgrammingLabel').textContent = name;
}
