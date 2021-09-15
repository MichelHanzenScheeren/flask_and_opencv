
window.addEventListener('pageshow', function (_) {
  try {
    const entries = performance.getEntriesByType("navigation");
    if (entries.map(nav => nav.type)[0] == "back_forward") {
      location.reload();
    }
  } catch (_) { }
}); // Tenta atualizar a pagina quando voltar da página de resultados (para ativar webcam)

(() => {
  defineImageStyle('{{ parameters["style"] }}');
  validateWebcam();
  addEventToWebcam();
})() // Função auto-executada

function defineImageStyle(style) {
  document.getElementById('frameImg').style = style;
  leftDivHeigth = document.getElementById('div-items-left').offsetHeight;
  document.getElementById('div-items-rigth').style.minHeight = `${leftDivHeigth}px`;
}

function validateWebcam() {
  let got_image = ('{{ parameters["success"] }}');
  if (got_image == 'False') {
    messageInvalidWebcam();
  }
} // validação inicial de funcionamento da webcam

function messageInvalidWebcam() {
  title = 'Problemas para configurar sua webcam &#128533;'
  body = `Infelizmente, não conseguimos obter imagens da sua webcam. 
      Por favor, verifique se a mesma está instalada e disponível para uso...`
  complement = `<button type="button" class="btn btn-lg btn-block btn-dark" onclick="location.reload();">
      Tentar novamente </button>`
  showMessage(title, body, complement);
}

function addEventToWebcam() {
  document.getElementById('selectCurrentWebcam').setAttribute('onchange', 'changeCurrentWebcam()');
  document.getElementById('recalibrateWebcamButton').setAttribute('onclick', 'recalibrateWebcam()');
}

function changeCurrentWebcam() {
  let select = document.getElementById('selectCurrentWebcam');
  axios.post(`{{url_for("change_current_webcam")}}/${select.value}`).then(function (response) {
    defineImageStyle(response.data.data['style']);
    $('#my-toast').remove();
  }).catch(showErrorMessage);
}

// RECALIBRATION PROCESS
let recalibrateWebcamCondition = false;
let recalibrationInterval;
let turnOnInterval;

function recalibrateWebcam() {
  if(!recalibrateWebcamCondition) {
    $('#recalibrateWebcamButton').text('Tem certeza?');
    recalibrateWebcamCondition = true;
    recalibrateInterval();
  } else {
    axios.post(`{{url_for("recalibrateWebcam")}}`).catch(showErrorMessage);
    redefineCalibration();
    $('#recalibrateWebcamButton').prop("disabled", true);
    turnOnInterval = setInterval(() => turnOnCalibrationButton(), 15000);
  }
}

function redefineCalibration() {
  clearInterval(recalibrationInterval);
  recalibrateWebcamCondition = false;
  $('#recalibrateWebcamButton').text('Recalibrar webcam');
}

function recalibrateInterval() {
  recalibrationInterval = setInterval(() => recalibrateWebcamCondition ? redefineCalibration() : false, 5000);
}

function turnOnCalibrationButton() {
  clearInterval(turnOnInterval);
  $('#recalibrateWebcamButton').prop("disabled", false);
}

