const ctxBarras3 = document.getElementById('grafico-barras-comparativo');
$.ajax({
    url: '/api-titulos-comparar',
    type: 'POST',
    async: false,
    dataType: 'json',
    contentType: 'application/json',
    success: function (data) {
        const myChart3 = new Chart(ctxBarras3, {
            type: 'bar',
            data: {
                labels: data.meses,
                datasets: [{
                    backgroundColor: 'rgb(54, 162, 235)',
                    borderColor: 'rgb(54, 162, 235)',
                    color: 'rgb(54, 162, 235)',
                    label: data.anoAtual,
                    data: data.valorresAtual,
                },
                {
                    backgroundColor: 'rgb(247, 99, 142)',
                    borderColor: 'rgb(247, 99, 142)',
                    color: 'rgb(247, 99, 142)',
                    label: data.anoAnterior,
                    data: data.valoresAnteriror,
                }]
            },
            options: {
                animation: {
                    duration: 1500,
                    easing: 'linear'
                },
                plugins: {
                    legend: {
                        display: true,
                        position: "bottom",
                        labels: {
                            color: 'rgb(0, 0, 0)'
                        }
                    },
                    title: {
                        display: true,
                        text: "Comparação de Recebidos entre anos",
                        position: 'top'
                    },
                    tooltips: {
                        enabled: true,
                        intersect: true,
                        backgroundColor: 'rgba(41, 128, 185,0.8)'
                    }
                },
                responsive: true,
            }
        })
    }
});


// Gráfico de pizza com a comparação dos títulos por devolução e baixas normais
const ctxBarras4 = document.getElementById('grafico-pizza-comparativo');
const myChart4 = new Chart(ctxBarras4, {
    type: 'doughnut',
    data: {
        labels: labelsChart,
        datasets: [{
            backgroundColor: [
                '#8A7EF0',
                '#61ED51',
                '#ED8E51',
                '#987A66',
                '#5E5C6E',
                'rgb(54, 120, 235)',
            ],
            data: dataChart,
        }]
    },
    options: {
        animation: {
            duration: 1500,
            easing: 'linear'
        },
        plugins: {
            legend: {
                display: true,
                position: "bottom",
                labels: {
                    color: 'rgb(0, 0, 0)'
                }
            },
            title: {
                display: true,
                text: "Comparação entre Segmentos (mês atual)",
                position: 'top'
            },
            tooltips: {
                enabled: true,
                intersect: true,
                backgroundColor: 'rgba(41, 128, 185,0.8)'
            }
        },
    }
});