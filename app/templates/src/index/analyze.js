(() => {
  document.getElementById('getDifferentiatorButton').setAttribute('onclick', 'getDifferentiator()');
  document.getElementById('analyzeForm').setAttribute('onsubmit', 'configAnalyze()');
}) () // Função auto-executada

async function getDifferentiator(){
  try {
    let response = await axios.post('{{ url_for("get_differentiator") }}');
    if(response.data == "" || response.data[0] == "[") {
      failedToGetDifferentiator();
    } else {
      document.getElementById('red').innerHTML = 'Red: ' + response.data[0];
      document.getElementById('green').innerHTML = 'Green: ' + response.data[1];
      document.getElementById('blue').innerHTML = 'Blue: ' + response.data[2];
      document.getElementById('startAnalyzeButton').disabled = false;
      getDifferentiatorImage()
    }
  } catch (error) {
    showErrorMessage(error);
  }
}

async function getDifferentiatorImage() {
  try {
    let response = await axios.post('{{ url_for("get_differentiator_image") }}');
    if(response.data == '') return;
    let differentiatorImage = document.getElementById('differentiatorImage')
    differentiatorImage.setAttribute('src', 'data:image/jpeg;base64,' + response.data);
  } catch (error) {
    showErrorMessage(error);
  }
}

function failedToGetDifferentiator() {
  title = 'Problemas para calcular o diferenciador &#128533;'
  body = `Infelizmente, não conseguimos calcular o diferenciador. 
      Por favor, verifique a solicitação e tente novamente...
      Se isso não funcionar, tente recarregar a página.`
  complement = `<button type="button" class="btn btn-lg btn-block btn-dark" onclick="location.reload();">
      Atualizar página </button>`
  showMessage(title, body, complement, true);
}

function configAnalyze() {
  document.getElementById('getDifferentiatorButton').disabled = true;
  document.getElementById('refreshRectangleButton').disabled = true;
  document.getElementById('clearRectangleButton').disabled = true;
  document.getElementById('div1').style.display = 'none';
  document.getElementById('div2').style.display = 'block';
  return false;
}


