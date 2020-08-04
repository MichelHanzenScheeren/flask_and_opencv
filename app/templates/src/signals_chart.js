google.charts.load('current', {packages: ['corechart']});
google.charts.setOnLoadCallback(drawChart);    

function drawChart() {
    var auxiliarData = [["Captura", "Sinal"]];
    for (let index = 0; index < signals.length; index++) {
        const element = signals[index];
        auxiliarData.push([`${index + 1}`, parseFloat(element)]);
    }
    var data = google.visualization.arrayToDataTable(auxiliarData);
    var style = {color: '#343a40', fontSize: 18, fontName: 'Arial', bold: false};
    var options = {
        height: 500,
        hAxis: {title: 'Captura', textStyle: style, titleTextStyle: {...style, fontSize: 24}},
        vAxis: {title: 'Sinal', textStyle: style, titleTextStyle: {...style, fontSize: 24}},
        legend: { position: 'none' },
        backgroundColor: "#e7e7e8",
        colors: ['#343a40'],
        pointsVisible: true,
    };
    var chart_div = document.getElementById('line_chart');
    var chart = new google.visualization.LineChart(chart_div);
    chart.draw(data, options);
}