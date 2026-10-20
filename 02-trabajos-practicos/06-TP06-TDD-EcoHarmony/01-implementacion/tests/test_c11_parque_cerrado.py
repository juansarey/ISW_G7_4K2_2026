"""C11 — Rechazar una fecha futura cuando el parque está cerrado."""

from collections.abc import Callable
from datetime import date, timedelta

import pytest

from ecoharmony.modelos import FormaPago, MotivoRechazo, SolicitudCompra
from ecoharmony.servicio_compras import ServicioCompras
from tests.dobles import (
    CalendarioDoble,
    CorreoDoble,
    PagoDoble,
    RepositorioDoble,
)


@pytest.mark.parametrize("forma_pago", [FormaPago.EFECTIVO, FormaPago.TARJETA])
def test_c11_rechaza_fecha_futura_con_parque_cerrado(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    fecha_actual: date,
    calendario: CalendarioDoble,
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
    forma_pago: FormaPago,
) -> None:
    fecha_visita = fecha_actual + timedelta(days=2)
    solicitud = crear_solicitud(
        fecha_visita=fecha_visita,
        forma_pago=forma_pago,
    )
    assert fecha_visita > fecha_actual
    assert calendario.esta_abierto(fecha_visita) is False

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is False
    assert resultado.motivo == MotivoRechazo.PARQUE_CERRADO
    assert resultado.compra is None
    assert resultado.url_redireccion is None
    assert pago.solicitudes == []
    assert correo.intentos == []
    assert repositorio.compras == {}
