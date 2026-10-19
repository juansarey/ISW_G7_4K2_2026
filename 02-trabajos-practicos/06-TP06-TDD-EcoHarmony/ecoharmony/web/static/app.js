// Formulario de compra. Solo recoge datos y muestra la respuesta del servidor:
// no valida reglas de negocio, para poder demostrar los rechazos (regla 12).

const formulario = document.getElementById("formulario-compra");
const listaEdades = document.getElementById("lista-edades");
const campoCantidad = document.getElementById("cantidad_entradas");
const panelResultado = document.getElementById("resultado");

let configuracion = null;

const EDADES_BASE = [24, 36];

function agregarCampoEdad(valor = "") {
  const fila = crearElemento("div", "edad");
  const entrada = document.createElement("input");
  entrada.type = "number";
  entrada.inputMode = "numeric";
  entrada.value = valor;
  entrada.setAttribute("aria-label", `Edad del visitante ${listaEdades.children.length + 1}`);
  const quitar = crearElemento("button", "boton boton--icono", "×");
  quitar.type = "button";
  quitar.title = "Quitar edad";
  quitar.addEventListener("click", () => fila.remove());
  fila.append(entrada, quitar);
  listaEdades.append(fila);
}

function cargarEdades(edades) {
  listaEdades.replaceChildren();
  edades.forEach((edad) => agregarCampoEdad(edad));
}

// Ayuda de carga: ajusta la cantidad de campos de edad, conservando los valores.
function ajustarEdadesALaCantidad() {
  const cantidad = Number.parseInt(campoCantidad.value, 10);
  if (!Number.isInteger(cantidad) || cantidad < 0 || cantidad > 20) return;
  while (listaEdades.children.length < cantidad) agregarCampoEdad("30");
  while (listaEdades.children.length > cantidad) listaEdades.lastElementChild.remove();
}

function cargarSolicitudBase() {
  formulario.usuario.value = "visitante01";
  formulario.fecha_visita.value = sumarDias(configuracion.fecha_actual, 1);
  campoCantidad.value = "2";
  cargarEdades(EDADES_BASE);
  formulario.tipo_pase.value = "REGULAR";
  formulario.forma_pago.value = "EFECTIVO";
}

const ESCENARIOS = {
  tarjeta: () => { formulario.forma_pago.value = "TARJETA"; },
  vip: () => { formulario.tipo_pase.value = "VIP"; },
  once: () => { campoCantidad.value = "11"; ajustarEdadesALaCantidad(); },
  pasada: () => { formulario.fecha_visita.value = sumarDias(configuracion.fecha_actual, -1); },
  cerrado: () => { formulario.fecha_visita.value = sumarDias(configuracion.fecha_actual, 2); },
  "sin-pago": () => { formulario.forma_pago.value = ""; },
  "no-registrado": () => { formulario.usuario.value = "invitado02"; },
};

function leerSolicitud() {
  return {
    usuario: formulario.usuario.value,
    fecha_visita: formulario.fecha_visita.value,
    cantidad_entradas: campoCantidad.value,
    edades: [...listaEdades.querySelectorAll("input")].map((entrada) => entrada.value),
    tipo_pase: formulario.tipo_pase.value,
    forma_pago: formulario.forma_pago.value,
  };
}

function mostrarResultado(tipo, titulo, contenido = []) {
  panelResultado.className = `resultado resultado--${tipo}`;
  panelResultado.replaceChildren(crearElemento("p", "resultado__titulo", titulo), ...contenido);
}

function presentarRespuesta(estadoHttp, respuesta) {
  if (estadoHttp >= 500 || respuesta.error) {
    mostrarResultado("error", "Error del servidor", [
      crearElemento("p", "", respuesta.error ?? "Error inesperado."),
      ...(respuesta.detalle ? [crearElemento("code", "detalle", respuesta.detalle)] : []),
    ]);
    return;
  }
  if (!respuesta.aceptada) {
    const contenido = [crearElemento("p", "", respuesta.mensaje ?? "La solicitud fue rechazada.")];
    if (respuesta.motivo) contenido.push(crearElemento("code", "motivo", respuesta.motivo));
    mostrarResultado("rechazo", "Compra rechazada", contenido);
    return;
  }
  const { compra } = respuesta;
  if (respuesta.url_redireccion) {
    const enlace = crearElemento("a", "boton boton--primario", "Ir a la pasarela de pago simulada");
    enlace.href = respuesta.url_redireccion;
    mostrarResultado("pendiente", "Compra pendiente de pago", [
      crearResumenCompra(compra),
      crearElemento("p", "ayuda", "La compra se confirmará cuando se apruebe el pago."),
      enlace,
    ]);
    return;
  }
  mostrarResultado("exito", `Compraste ${compra.cantidad_entradas} entrada(s) para el ${formatearFecha(compra.fecha_visita)}`, [
    crearResumenCompra(compra),
  ]);
}

async function enviarSolicitud(evento) {
  evento.preventDefault();
  const boton = formulario.querySelector("[type=submit]");
  boton.disabled = true;
  try {
    const respuesta = await fetch("/api/compras", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(leerSolicitud()),
    });
    presentarRespuesta(respuesta.status, await respuesta.json());
    await actualizarBandeja();
  } catch (error) {
    mostrarResultado("error", "No se pudo contactar al servidor", [crearElemento("p", "", String(error))]);
  } finally {
    boton.disabled = false;
  }
}

function mostrarConfiguracion() {
  document.getElementById("fecha-actual").textContent = formatearFecha(configuracion.fecha_actual);

  formulario.usuario.replaceChildren(
    ...configuracion.usuarios.map((usuario) => {
      const opcion = crearElemento(
        "option", "", `${usuario.nombre_usuario} — ${usuario.registrado ? "registrado" : "no registrado"}`,
      );
      opcion.value = usuario.nombre_usuario;
      return opcion;
    }),
  );

  document.getElementById("tarifas").replaceChildren(
    ...configuracion.tipos_pase.map((pase) => {
      const item = crearElemento("li", "tarifa");
      item.append(
        crearElemento("span", "", `Pase ${TEXTOS_PASE[pase]}`),
        crearElemento("strong", "", formatearMoneda(configuracion.tarifas[pase])),
      );
      return item;
    }),
  );

  document.getElementById("calendario").replaceChildren(
    ...configuracion.calendario.map(({ fecha, abierto }) => {
      const dia = parsearFechaIso(fecha);
      const item = crearElemento("li", `dia ${abierto ? "dia--abierto" : "dia--cerrado"}`);
      if (fecha === configuracion.fecha_actual) item.classList.add("dia--hoy");
      item.title = `${formatearFecha(fecha)}: ${abierto ? "abierto" : "cerrado"}`;
      item.append(
        crearElemento("span", "dia__nombre", NOMBRES_DIAS[dia.getDay()]),
        crearElemento("span", "dia__numero", String(dia.getDate())),
      );
      item.addEventListener("click", () => { formulario.fecha_visita.value = fecha; });
      return item;
    }),
  );
}

async function actualizarBandeja() {
  const correos = await (await fetch("/api/correos")).json();
  const bandeja = document.getElementById("bandeja");
  if (correos.length === 0) {
    bandeja.replaceChildren(crearElemento("li", "ayuda", "Sin correos enviados."));
    return;
  }
  bandeja.replaceChildren(
    ...correos.map((compra) => {
      const item = crearElemento("li", "correo");
      item.append(
        crearElemento("strong", "", `Para: ${compra.correo}`),
        crearElemento("span", "", `${compra.cantidad_entradas} entrada(s) · ${formatearFecha(compra.fecha_visita)} · ${formatearMoneda(compra.total)}`),
      );
      return item;
    }),
  );
}

async function iniciar() {
  configuracion = await (await fetch("/api/configuracion")).json();
  mostrarConfiguracion();
  cargarSolicitudBase();
  await actualizarBandeja();

  formulario.addEventListener("submit", enviarSolicitud);
  campoCantidad.addEventListener("change", ajustarEdadesALaCantidad);
  document.getElementById("agregar-edad").addEventListener("click", () => agregarCampoEdad());
  document.getElementById("cargar-base").addEventListener("click", cargarSolicitudBase);
  document.querySelectorAll("[data-escenario]").forEach((boton) => {
    boton.addEventListener("click", () => {
      cargarSolicitudBase();
      ESCENARIOS[boton.dataset.escenario]();
    });
  });
}

iniciar();
