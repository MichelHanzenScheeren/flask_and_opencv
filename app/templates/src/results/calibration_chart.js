function drawCalibrationChart(calibration_values) {
  try {
    if (calibration_values.length == 0) return;
    let xValues = [0];
    let yValues = [null];
    for (let index = 0; index < calibration_values.length; index++) {
      xValues.push((index + 1).toString());
      yValues.push(parseFloat(calibration_values[index]).toFixed(4));
    }
    xValues.push(calibration_values.length + 1);
    yValues.push(null);
    let options = { display: true, fontSize: 16 };
    let bgColor = 'rgba(52, 58, 64, 1)';
    let borderColor = 'rgba(52, 58, 64, 0.7)';
    let configAndData = {
      type: 'line',
      data: {
        labels: xValues,
        datasets: [{
          label: 'Sinal',
          data: yValues, pointBackgroundColor: bgColor,
          borderColor: borderColor, lineTension: 0, fill: false
        }],
      },
      options: {
        responsive: true,
        scales: {
          yAxes: [{ scaleLabel: { ...options, labelString: 'Sinal médio' } }],
          xAxes: [{ scaleLabel: { ...options, labelString: 'Concentração' } }],
        }
      }
    };
    new Chart(document.getElementById('calibrationChartCanvas'), configAndData);
  } catch (error) {
    console.warn(error);
    let message = 'Não foi possível renderizar o gráfico de calibração corretamente';
    showMessage('Problemas ao exibir os gráficos', message, undefined, false);
  }
}
