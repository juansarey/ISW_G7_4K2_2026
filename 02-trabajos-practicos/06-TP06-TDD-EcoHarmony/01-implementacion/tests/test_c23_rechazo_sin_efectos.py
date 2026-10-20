"""C23 — Rechazo por exceso de entradas y ausencia de efectos secundarios (DD02)."""

from ecoharmony.modelos import MotivoRechazo


def test_c23_rechaza_exceso_entradas_sin_efectos_secundarios(
    servicio_compras, crear_solicitud, pago, correo
):
    # Preparación: Solicitud con 11 entradas (supera el límite de CA07)
    solicitud = crear_solicitud(cantidad_entradas=11)

    # Ejecución
    resultado = servicio_compras.comprar(solicitud)

    # Verificación: Se rechaza y se indica el motivo correspondiente
    assert resultado.aceptada is False
    assert resultado.motivo == MotivoRechazo.CANTIDAD_EXCEDE_MAXIMO
    assert resultado.compra is None

    # Garantía DD02: No debe haberse solicitado pago ni enviado correo
    assert len(pago.solicitudes) == 0
    assert len(correo.intentos) == 0
