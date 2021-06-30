function drawCharts(signals, interval, calibration_values) {
  try {
    _drawSignalsChart(signals, interval);
    _drawCalibrationChart(calibration_values);
  } catch (error) {
    console.warn(error);
    let message = 'Um erro impediu que os gráficos fossem renderizados corretamente';
    showMessage('Problemas nos gráficos', message, undefined, false);
  }
}

function _drawSignalsChart(signals, interval) {
  let xValues = [], yValues = [];
  for (let index = 0; index < signals.length; index++) {
    xValues.push(((index + 1) * interval).toFixed(1).toString());
    yValues.push(parseFloat(signals[index]).toFixed(4));
  }
  _registerChart(xValues, yValues, 'Sinal', 'Tempo (segundos)', 'Sinal', 'lineChartCanvas', false);
}

function _drawCalibrationChart(calibration_values) {
  if (calibration_values.length == 0) return;
  let xValues = [0];
  let yValues = [null];
  for (let index = 0; index < calibration_values.length; index++) {
    xValues.push((index + 1).toString());
    yValues.push(parseFloat(calibration_values[index]).toFixed(4));
  }
  xValues.push(calibration_values.length + 1);
  yValues.push(null);
  _registerChart(xValues, yValues, 'Sinal', 'Ciclo', 'Sinal', 'calibrationChartCanvas', true);
}

function _registerChart(xValues, yValues, dataLabel, xLabel, yLabel, htmlComponent, isTransparent) {
  var options = { display: true, fontSize: 16 };
  var configAndData = {
    type: 'line',
    data: {
      labels: xValues,
      datasets: [{
        label: dataLabel, data: yValues, lineTension: 0, fill: false,
        pointBackgroundColor: 'rgba(52, 58, 64, 1)', borderColor: `rgba(52, 58, 64, ${isTransparent ? '0.0' : '0.7'})`,
      }],
    },
    options: {
      responsive: true,
      scales: {
        xAxes: [{ scaleLabel: { ...options, labelString: xLabel } }],
        yAxes: [{ scaleLabel: { ...options, labelString: yLabel } }],
      }
    }
  };
  new Chart(document.getElementById(htmlComponent), configAndData);
}
