"""C24 — Redirección solicitada sin confirmación de pago ni envío de correo (DD05).

Una solicitud válida con tarjeta inicia la redirección, pero mantiene la compra 
y el pago en estado pendiente hasta recibir la confirmación de la pasarela.
"""

def test_c24_redireccion_sin_confirmacion_de_pago(
    servicio_compras, crear_solicitud, pago, correo
):
    # Preparación: Solicitud válida con pago por tarjeta
    solicitud = crear_solicitud(forma_pago="tarjeta")

    # Ejecución
    resultado = servicio_compras.comprar(solicitud)

    # Verificación: Se acepta y se solicita la redirección a la pasarela de pago
    assert resultado.aceptada is True
    assert resultado.requiere_redireccion is True

    # Comprobación DD05: La compra y el pago quedan pendientes, y el correo NO se solicita
    assert resultado.compra.estado == "PENDIENTE"
    assert resultado.pago.estado == "PENDIENTE"
    correo.enviar.assert_not_called()