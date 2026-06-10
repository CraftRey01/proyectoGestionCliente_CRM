document.addEventListener('DOMContentLoaded', function () {
    const ventasBar = document.getElementById('bar-ventas');
    const campaniasBar = document.getElementById('bar-campanias');
    const ventasValue = document.getElementById('bar-ventas-value');
    const campaniasValue = document.getElementById('bar-campanias-value');
    const stateChart = document.getElementById('state-chart');

    const summaryMax = Math.max(dashboardData.totalVentas, dashboardData.totalCampanias, 1);
    const ventasPercent = Math.min(90, Math.max(10, (dashboardData.totalVentas / summaryMax) * 100));
    const campaniasPercent = Math.min(90, Math.max(10, (dashboardData.totalCampanias / summaryMax) * 100));

    ventasBar.style.width = `${ventasPercent}%`;
    campaniasBar.style.width = `${campaniasPercent}%`;
    ventasValue.textContent = dashboardData.totalVentas;
    campaniasValue.textContent = dashboardData.totalCampanias;

    stateChart.innerHTML = '';
    const estados = Array.isArray(dashboardData.estados) ? dashboardData.estados : [];
    const valores = Array.isArray(dashboardData.valores) ? dashboardData.valores : [];
    const maxEstado = Math.max(...valores, 1);

    if (!valores.length) {
        stateChart.innerHTML = '<div class="text-muted">No hay datos de ventas por estado disponibles.</div>';
        return;
    }

    valores.forEach((valor, index) => {
        const estado = estados[index] || 'Sin estado';
        const ratio = (valor / maxEstado) * 100;

        const row = document.createElement('div');
        row.className = 'state-bar-row';

        const label = document.createElement('div');
        label.className = 'state-bar-label';
        label.textContent = estado;

        const track = document.createElement('div');
        track.className = 'state-bar-track';

        const fill = document.createElement('div');
        fill.className = 'state-bar-fill';
        fill.style.width = `${Math.max(ratio, 3)}%`;
        fill.textContent = valor;

        const value = document.createElement('div');
        value.className = 'state-bar-value';
        value.textContent = valor;

        track.appendChild(fill);
        row.appendChild(label);
        row.appendChild(track);
        row.appendChild(value);
        stateChart.appendChild(row);
    });
    
});
