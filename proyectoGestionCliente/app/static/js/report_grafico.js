document.addEventListener("DOMContentLoaded", function () {

    const reportData = window.reportData;

    // BARRAS
    const generalCanvas = document.getElementById("general-bar-chart");

    if (generalCanvas) {

        new Chart(generalCanvas, {
            type: "bar",
            data: {
                labels: ["Ventas", "Campañas"],
                datasets: [{
                    label: "Cantidad",
                    data: [
                        reportData.totalVentas,
                        reportData.totalCampanias
                    ],
                    backgroundColor: [
                        "#7c3aed",
                        "#2563eb"
                    ],
                    borderRadius: 12,
                    barThickness: 24
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

    }

    // DONA
    const pieCanvas = document.getElementById("state-pie-chart");

    if (pieCanvas) {

        new Chart(pieCanvas, {
            type: "doughnut",
            data: {
                labels: reportData.labels,
                datasets: [{
                    data: reportData.valores,
                    backgroundColor: [
                        "#7c3aed",
                        "#2dd4bf",
                        "#f59e0b",
                        "#ef4444",
                        "#3b82f6"
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });

    }

    // LINEAS
    const lineCanvas = document.getElementById("reports-line-chart");

    if (lineCanvas) {

        new Chart(lineCanvas, {
            type: "line",
            data: {
                labels: reportData.periodosOrdenados,
                datasets: [{
                    label: "Reportes por Período",
                    data: reportData.conteos,
                    borderColor: "#4f46e5",
                    backgroundColor: "rgba(79,70,229,0.1)",
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

    }

});