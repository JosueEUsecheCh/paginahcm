document.addEventListener('DOMContentLoaded', function () {
    const consultarBtn = document.getElementById('btn-consultar');
    const cedulaInput = document.getElementById('cedula');
    const form = document.getElementById('consulta-form');
    const nuevaConsultaBtn = document.getElementById('btn-nueva-consulta');
    const resultadosContainer = document.getElementById('resultados-container');

    // Estado inicial botón según sesión
    if (sessionStorage.getItem('consultarDisabled') === 'true') {
        consultarBtn.disabled = true;
    } else {
        consultarBtn.disabled = false;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    function mostrarErrorEnContenedor(msg) {
        resultadosContainer.innerHTML = `<p class="error">${msg}</p>`;
    }

    consultarBtn.addEventListener('click', function () {
        const cedula = cedulaInput.value.trim();

        // Validación rápida
        if (!/^\d+$/.test(cedula)) {
            alert('Solo se permiten números.');
            return;
        }
        if (cedula.length > 14) {
            alert('La cédula no debe exceder los 14 dígitos.');
            return;
        }

        // Desactivar botón para evitar doble click
        consultarBtn.disabled = true;
        resultadosContainer.innerHTML = ''; // Limpiar resultados previos

        const data = new FormData();
        data.append('cedula', cedula);

        fetch(form.getAttribute('action'), {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
            body: data,
        })
        .then(response => response.json())
        .then(json => {
            if (json.success) {
                resultadosContainer.innerHTML = json.html;
                // Guardar estado botón deshabilitado
                sessionStorage.setItem('consultarDisabled', 'true');
            } else {
                if (json.error === "No se encontraron resultados para la cédula proporcionada.") {
                    mostrarErrorEnContenedor(json.error);
                    // También deshabilitar botón y guardar estado
                    sessionStorage.setItem('consultarDisabled', 'true');
                } else {
                    alert(json.error || 'Error en la consulta.');
                    consultarBtn.disabled = false;
                    sessionStorage.removeItem('consultarDisabled');
                }
            }
        })
        .catch(error => {
            alert('Error en la consulta. Intente de nuevo.');
            console.error(error);
            consultarBtn.disabled = false;
            sessionStorage.removeItem('consultarDisabled');
        });
    });

    nuevaConsultaBtn.addEventListener('click', function () {
        sessionStorage.removeItem('consultarDisabled');
        consultarBtn.disabled = false;
        resultadosContainer.innerHTML = '';
        cedulaInput.value = '';
        cedulaInput.focus();
    });

    // Bloquear selección de texto
    document.body.style.userSelect = 'none';

    // Bloquear clic derecho
    document.addEventListener('contextmenu', function (e) {
        e.preventDefault();
    });

    // Bloquear Ctrl+C o Cmd+C
    document.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'c') {
            e.preventDefault();
        }
    });
});
