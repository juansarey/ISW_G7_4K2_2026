// Utilidades de presentación compartidas por las páginas de la demostración.

const formatoMoneda = new Intl.NumberFormat("es-AR", {
  style: "currency",
  currency: "ARS",
  maximumFractionDigits: 0,
});

const NOMBRES_DIAS = ["dom", "lun", "mar", "mié", "jue", "vie", "sáb"];

const TEXTOS_ESTADO = {
  CONFIRMADA: "Compra confirmada",
  PENDIENTE: "Compra pendiente",
  CANCELADA: "Compra cancelada",
  PENDIENTE_BOLETERIA: "Pago pendiente en boletería",
  PENDIENTE_PASARELA: "Pago pendiente en la pasarela",
  APROBADO: "Pago aprobado",
  RECHAZADO: "Pago rechazado",
  NO_SOLICITADO: "Correo aún no enviado",
  ENVIADO: "Correo de confirmación enviado",
  CORREO_PENDIENTE: "Correo pendiente de reenvío",
};

const TEXTOS_PASE = { REGULAR: "Regular", VIP: "VIP" };
const TEXTOS_PAGO = { EFECTIVO: "Efectivo en boletería", TARJETA: "Tarjeta de crédito" };

function parsearFechaIso(textoIso) {
  const [anio, mes, dia] = textoIso.split("-").map(Number);
  return new Date(anio, mes - 1, dia);
}

function formatearFecha(textoIso) {
  return parsearFechaIso(textoIso).toLocaleDateString("es-AR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}

function formatearMoneda(textoDecimal) {
  return formatoMoneda.format(Number(textoDecimal));
}

function sumarDias(textoIso, dias) {
  const fecha = parsearFechaIso(textoIso);
  fecha.setDate(fecha.getDate() + dias);
  const mes = String(fecha.getMonth() + 1).padStart(2, "0");
  const dia = String(fecha.getDate()).padStart(2, "0");
  return `${fecha.getFullYear()}-${mes}-${dia}`;
}

function crearElemento(etiqueta, clase, texto) {
  const elemento = document.createElement(etiqueta);
  if (clase) elemento.className = clase;
  if (texto !== undefined) elemento.textContent = texto;
  return elemento;
}

function crearFilaDato(etiqueta, valor) {
  const fila = crearElemento("div", "dato");
  fila.append(crearElemento("dt", "", etiqueta), crearElemento("dd", "", valor));
  return fila;
}

function crearResumenCompra(compra) {
  const lista = crearElemento("dl", "datos");
  lista.append(
    crearFilaDato("Entradas", String(compra.cantidad_entradas)),
    crearFilaDato("Fecha de visita", formatearFecha(compra.fecha_visita)),
    crearFilaDato("Pase", TEXTOS_PASE[compra.tipo_pase] ?? compra.tipo_pase),
    crearFilaDato("Forma de pago", TEXTOS_PAGO[compra.forma_pago] ?? "—"),
    crearFilaDato("Total", formatearMoneda(compra.total)),
    crearFilaDato("Estado", TEXTOS_ESTADO[compra.estado_compra]),
    crearFilaDato("Pago", TEXTOS_ESTADO[compra.estado_pago]),
    crearFilaDato("Correo", TEXTOS_ESTADO[compra.estado_correo]),
  );
  return lista;
}
