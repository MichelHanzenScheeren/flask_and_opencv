function drawChart(signals, interval) {
  try {
    var chartLabels = [];
    var chartData = [];
    for (let index = 0; index < signals.length; index++) {
      chartLabels.push(((index + 1) * interval).toFixed(1).toString());
      chartData.push(parseFloat(signals[index]).toFixed(4));
    }
    var options = { display: true, fontSize: 16 };
    var configAndData = {
      type: 'line',
      data: {
        labels: chartLabels,
        datasets: [{
          label: 'Sinal',
          data: chartData,
          pointBackgroundColor: 'rgba(52, 58, 64, 1)',
          borderColor: 'rgba(52, 58, 64, 0.7)',
          lineTension: 0,
          fill: false,
        }],
      },
      options: {
        responsive: true,
        scales: {
          yAxes: [{ scaleLabel: { ...options, labelString: 'Sinal' } }],
          xAxes: [{ scaleLabel: { ...options, labelString: 'Tempo (segundos)' } }],
        }
      }
    };
    new Chart(document.getElementById('lineChartCanvas'), configAndData);
  } catch (error) {
    console.warn(error);
    let message = 'Não foi possível renderizar os gráficos corretamente';
    showMessage('Problemas ao exibir os gráficos', message, undefined, false);
  }
}
