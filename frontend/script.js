fetch('/ver_progreso')
  .then(res => res.json())
  .then(data => {
    const tbody = document.querySelector("#tabla-progreso tbody");
    data.forEach(user => {
      const fila = document.createElement("tr");
      fila.innerHTML = `
        <td>${user.id}</td>
        <td>${user.codigo}</td>
        <td>${user.modulo}/18</td>
      `;
      tbody.appendChild(fila);
    });
  });
