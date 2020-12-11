(() => {
  document.getElementById('getDifferentiatorButton').setAttribute('onclick', 'getDifferentiator()');
  document.getElementById('startAnalyzeButton').setAttribute('onclick', 'validateToAnalyze()');
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

function validateToAnalyze() {
  try {
    var stringTempo = document.getElementById('timeInput').value;
    var stringQtd = document.getElementById('qtdInput').value;
    var tempo = parseInt(stringTempo);
    var qtd = parseInt(stringQtd);
    if(tempo != stringTempo ||  tempo < 1) {
      var body = 'Tempo deve ser um valor inteiro maior do que 0.';
      showMessage('Preenchimento inválido', body);
    } else if (qtd != stringQtd || qtd < 1 || qtd > 10) {
      var body = 'Nº de capturas deve ser um valor inteiro maior do que 0 e menor do que 11.';
      showMessage('Preenchimento inválido', body);
    } else {
      clearMessage();
      configAnalyze();
      document.getElementById('analyzeForm').submit();
    }
  } catch (error) {
    var title = 'Não foi possível completar a solicitação.';
    var body = 'Por favor, verifique o preenchimento do formulário e tente novamente';
    showMessage(title, body);
  }
}

function configAnalyze() {
  document.getElementById('getDifferentiatorButton').disabled = true;
  document.getElementById('refreshRectangleButton').disabled = true;
  document.getElementById('clearRectangleButton').disabled = true;
  document.getElementById('div1').style.display = 'none';
  document.getElementById('div2').style.display = 'block';
  let dt = new Date();
  let dateInput = document.getElementById('userDate');
  dateInput.value = `${dt.getDate()}-${dt.getMonth()+1}-${dt.getFullYear()} ${dt.getHours()}:${dt.getMinutes()}:${dt.getSeconds()}`;
}


