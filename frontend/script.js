async function cargarDatos() {
  const respuesta = await fetch("/ver_progreso");
  const data = await respuesta.json();
  const cuerpo = document.getElementById("cuerpo-tabla");
  cuerpo.innerHTML = "";

  for (const [codigo, info] of Object.entries(data)) {
    const fila = document.createElement("tr");

    const tdCodigo = document.createElement("td");
    tdCodigo.textContent = codigo;

    const tdModulo = document.createElement("td");
    tdModulo.textContent = info.modulo_actual;

    const tdPorcentaje = document.createElement("td");
    const porcentaje = Math.round((info.modulo_actual / 18) * 100);
    tdPorcentaje.textContent = `${porcentaje}%`;

    fila.appendChild(tdCodigo);
    fila.appendChild(tdModulo);
    fila.appendChild(tdPorcentaje);
    cuerpo.appendChild(fila);
  }
}

cargarDatos();
setInterval(cargarDatos, 10000); // actualiza cada 10s
