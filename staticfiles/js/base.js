document.addEventListener('DOMContentLoaded', () => {
  const btnConsultar = document.getElementById('btn-consultar');
  const btnNuevaConsulta = document.getElementById('btn-nueva-consulta');
  const form = document.getElementById('consulta-form');
  const resultadosContainer = document.getElementById('resultados-container');

  btnConsultar.addEventListener('click', () => {
    const url = form.dataset.urlConsultar;
    const cedula = form.cedula.value.trim();

    if (!cedula) {
      resultadosContainer.innerHTML = '<p class="error">Por favor ingresa una cédula.</p>';
      return;
    }

    // Crear objeto FormData con la cédula y csrf token
    const formData = new FormData(form);

    fetch(url, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        resultadosContainer.innerHTML = data.html;
      } else {
        resultadosContainer.innerHTML = `<p class="error">${data.error}</p>`;
      }
    })
    .catch(error => {
      resultadosContainer.innerHTML = '<p class="error">Error en la consulta. Intenta nuevamente.</p>';
      console.error('Error:', error);
    });
  });

  btnNuevaConsulta.addEventListener('click', () => {
    form.reset();
    resultadosContainer.innerHTML = '';
    form.cedula.focus();
  });
});
