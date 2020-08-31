(() => {
    google.charts.load('current', {packages: ['corechart']});
    google.charts.setOnLoadCallback(drawChart); 
}) () // Função auto-executada.

function drawChart() {
    try {  
        var auxiliarData = [["Tempo", "Sinal"]];
        for (let index = 0; index < signals.length; index++) {
            const element = signals[index];
            auxiliarData.push([((index + 1) * interval).toString(), parseFloat(element)]);
        }
        var data = google.visualization.arrayToDataTable(auxiliarData);
        var style = {color: '#343a40', fontSize: 18, fontName: 'Arial', bold: false};
        var options = {
            height: 500,
            hAxis: {title: 'Tempo(seg)', textStyle: style, titleTextStyle: style},
            vAxis: {title: 'Sinal', textStyle: style, titleTextStyle: style},
            legend: { position: 'none' },
            backgroundColor: "#FFFFFF",
            colors: ['#343a40'],
            pointsVisible: true,
        };
        var chart_div = document.getElementById('lineChartDiv');
        var chart = new google.visualization.LineChart(chart_div);
        chart.draw(data, options);
    } catch (error) {
        console.log("entrei");
        showErrorMessage(error);
    }
}