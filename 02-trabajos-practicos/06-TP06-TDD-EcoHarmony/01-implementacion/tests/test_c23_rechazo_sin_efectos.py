"""C23 — Rechazo por exceso de entradas y ausencia de efectos secundarios (DD02).

Se realiza una solicitud con 11 entradas (superando el límite de 10) para 
comprobar el rechazo previo y garantizar que no se invoquen servicios externos.
"""

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
    assert resultado.motivo == MotivoRechazo.CANTIDAD_EXCEDIDA  # Ajustar según tu Enum si difiere
    assert resultado.compra is None

    # Garantía DD02: No debe haberse solicitado pago ni enviado correo
    pago.assert_not_called()
    correo.enviar.assert_not_called()