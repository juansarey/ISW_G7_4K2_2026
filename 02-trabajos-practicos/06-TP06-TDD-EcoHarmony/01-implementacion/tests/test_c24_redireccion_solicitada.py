"""C24 — Redirección solicitada sin confirmación de pago ni envío de correo (DD05)."""

from ecoharmony.modelos import EstadoCompra, EstadoPago, FormaPago


def test_c24_redireccion_sin_confirmacion_de_pago(
    servicio_compras, crear_solicitud, pago, correo
):
    # Preparación: Solicitud válida indicando el Enum de tarjeta
    solicitud = crear_solicitud(forma_pago=FormaPago.TARJETA)

    # Ejecución
    resultado = servicio_compras.comprar(solicitud)

    # Verificación: Se acepta y devuelve la URL de redirección
    assert resultado.aceptada is True
    assert resultado.url_redireccion is not None

    # Comprobación DD05: La compra y el pago quedan pendientes, y el correo NO se envía
    assert resultado.compra.estado_compra == EstadoCompra.PENDIENTE
    assert resultado.compra.estado_pago == EstadoPago.PENDIENTE_PASARELA
    assert len(correo.intentos) == 0
