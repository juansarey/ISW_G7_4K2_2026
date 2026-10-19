"""C02 — Compra válida con tarjeta de crédito.

CA01, CA04 y CA06. Cambiar efectivo por tarjeta de crédito; servicio de pago
disponible. Comportamiento esperado: aceptar y abrir la pasarela simulada.
Mantener compra y pago pendientes hasta la aprobación, según A02.
"""

from ecoharmony.modelos import EstadoCompra, EstadoPago, FormaPago


def test_c02_acepta_y_abre_la_pasarela_de_pago(servicio_compras, crear_solicitud, pago):
    # Preparación
    solicitud = crear_solicitud(forma_pago=FormaPago.TARJETA)

    # Ejecución
    resultado = servicio_compras.comprar(solicitud)

    # Verificación
    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert len(pago.solicitudes) == 1
    assert resultado.url_redireccion is not None


def test_c02_mantiene_compra_y_pago_pendientes_hasta_la_aprobacion(
    servicio_compras, crear_solicitud
):
    solicitud = crear_solicitud(forma_pago=FormaPago.TARJETA)

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.compra.estado_compra == EstadoCompra.PENDIENTE
    assert resultado.compra.estado_pago == EstadoPago.PENDIENTE_PASARELA
