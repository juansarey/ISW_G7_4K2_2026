"""C01 — Compra válida en efectivo.

CA01, CA06, CA08 y CA09. Solicitud base completa con usuario registrado y efectivo.
Comportamiento esperado: confirmar la compra con pago pendiente en boletería;
conservar dos entradas y D0 + 1 y solicitar el correo según A02.
"""

from datetime import timedelta

from ecoharmony.modelos import EstadoCompra, EstadoPago


def test_c01_confirma_compra_en_efectivo_con_pago_pendiente_en_boleteria(
    servicio_compras, solicitud_base
):
    # Ejecución
    resultado = servicio_compras.comprar(solicitud_base)

    # Verificación
    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra.estado_compra == EstadoCompra.CONFIRMADA
    assert resultado.compra.estado_pago == EstadoPago.PENDIENTE_BOLETERIA


def test_c01_conserva_cantidad_y_fecha_validadas(
    servicio_compras, solicitud_base, fecha_actual
):
    resultado = servicio_compras.comprar(solicitud_base)

    assert resultado.compra.cantidad_entradas == 2
    assert resultado.compra.fecha_visita == fecha_actual + timedelta(days=1)


def test_c01_registra_la_compra_confirmada(
    servicio_compras, solicitud_base, repositorio
):
    resultado = servicio_compras.comprar(solicitud_base)

    compra_registrada = repositorio.obtener(resultado.compra.id_compra)
    assert compra_registrada is not None
    assert compra_registrada.estado_compra == EstadoCompra.CONFIRMADA


def test_c01_solicita_un_correo_al_visitante(servicio_compras, solicitud_base, correo):
    servicio_compras.comprar(solicitud_base)

    assert len(correo.intentos) == 1
    assert correo.intentos[0].usuario.correo == "visitante@example.com"
