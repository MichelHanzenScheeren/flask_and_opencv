try {
  var chartLabels = [];
  var chartData = [];
  for (let index = 0; index < signals.length; index++) {
    chartLabels.push(((index + 1) * interval).toFixed(1).toString());
    chartData.push(parseFloat(signals[index]).toFixed(4));
  }
  var options = {display: true,fontSize: 16};
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
      scales: {
        xAxes: [{scaleLabel: {...options, labelString:'Tempo(seg)'}}],
        yAxes: [{scaleLabel:{...options, labelString:'Sinal'}}],
      }
    }
  };
  new Chart(document.getElementById('lineChartCanvas'), configAndData);
} catch (error) {
  console.log(error);
  showErrorMessage(error);
}
