"""C10 — Rechazo de compra con fecha anterior a la actual (CA02).

Se cambia la fecha de visita por D0 - 1. El calendario preparado mantiene ese día
abierto para aislar la regla de fecha pasada de la de parque cerrado.
"""

from datetime import timedelta

from ecoharmony.modelos import MotivoRechazo


def test_c10_rechaza_fecha_anterior_a_la_actual(
    servicio_compras, crear_solicitud, fecha_actual, calendario
):
    fecha_pasada = fecha_actual - timedelta(days=1)
    assert calendario.esta_abierto(fecha_pasada) is True

    solicitud = crear_solicitud(fecha_visita=fecha_pasada)

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is False
    assert resultado.compra is None
    assert resultado.motivo == MotivoRechazo.FECHA_PASADA
