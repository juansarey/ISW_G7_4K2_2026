"""C20 — Resumen de dos entradas: fecha, pase, total y estado de pago."""

from collections.abc import Callable
from datetime import date, timedelta
from decimal import Decimal

import pytest

from ecoharmony.modelos import (
    EstadoCompra,
    EstadoPago,
    FormaPago,
    SolicitudCompra,
    TipoPase,
)
from ecoharmony.servicio_compras import ServicioCompras


@pytest.mark.parametrize(
    ("tipo_pase", "total_esperado"),
    [
        (TipoPase.REGULAR, Decimal("20000")),
        (TipoPase.VIP, Decimal("30000")),
    ],
)
@pytest.mark.parametrize("forma_pago", [FormaPago.EFECTIVO, FormaPago.TARJETA])
def test_c20_informa_resumen_de_compra_confirmada(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    fecha_actual: date,
    tipo_pase: TipoPase,
    total_esperado: Decimal,
    forma_pago: FormaPago,
) -> None:
    fecha_visita = fecha_actual + timedelta(days=1)
    solicitud = crear_solicitud(
        fecha_visita=fecha_visita,
        cantidad_entradas=2,
        edades=(24, 36),
        tipo_pase=tipo_pase,
        forma_pago=forma_pago,
    )

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is True
    assert resultado.compra is not None

    if forma_pago == FormaPago.TARJETA:
        resultado = servicio_compras.registrar_resultado_pago(
            resultado.compra.id_compra, aprobado=True
        )

    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    compra = resultado.compra

    assert compra.estado_compra == EstadoCompra.CONFIRMADA
    assert compra.cantidad_entradas == 2
    assert compra.fecha_visita == fecha_visita
    assert compra.tipo_pase == tipo_pase
    assert compra.forma_pago == forma_pago
    assert compra.total == total_esperado
    assert isinstance(compra.total, Decimal)

    pago_esperado = (
        EstadoPago.APROBADO
        if forma_pago == FormaPago.TARJETA
        else EstadoPago.PENDIENTE_BOLETERIA
    )
    assert compra.estado_pago == pago_esperado
