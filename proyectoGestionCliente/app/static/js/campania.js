document.addEventListener('DOMContentLoaded', function () {
    const selectAll = document.getElementById('select-all');
    const clearAll = document.getElementById('clear-all');
    const automateAllButton = document.getElementById('automatizar-todas-campanias');

    if (selectAll) {
        selectAll.addEventListener('click', function () {
            const select = document.getElementById('clientes');
            if (!select) return;
            for (let i = 0; i < select.options.length; i++) {
                select.options[i].selected = true;
            }
        });
    }

    if (clearAll) {
        clearAll.addEventListener('click', function () {
            const select = document.getElementById('clientes');
            if (!select) return;
            for (let i = 0; i < select.options.length; i++) {
                select.options[i].selected = false;
            }
        });
    }

    if (automateAllButton) {
        automateAllButton.addEventListener('click', function () {
            if (!confirm('¿Deseas generar la siguiente campaña automática?')) {
                return;
            }
            window.location.href = '/campanias/automatizar';
        });
    }
});
