async function cargarProgreso() {
  const res = await fetch("/ver_progreso");
  const data = await res.json();
  const tbody = document.querySelector("#tabla-progreso tbody");
  tbody.innerHTML = "";

  for (const [codigo, info] of Object.entries(data)) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${codigo}</td>
      <td>${info.modulo}/18</td>
    `;
    tbody.appendChild(tr);
  }
}

cargarProgreso();
