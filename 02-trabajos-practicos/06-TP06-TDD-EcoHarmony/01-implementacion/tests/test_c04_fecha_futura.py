"""C04 — Aceptar una fecha futura en el calendario de apertura (CA02 y CA05).

Se mantiene D0 + 1 abierto y el resto de la solicitud base válido. Se comprueba
que ambas formas de pago conservan la fecha futura en el resultado y en el registro.
"""

from collections.abc import Callable
from datetime import date, timedelta

import pytest

from ecoharmony.modelos import FormaPago, SolicitudCompra
from ecoharmony.servicio_compras import ServicioCompras
from tests.dobles import CalendarioDoble, RepositorioDoble


@pytest.mark.parametrize("forma_pago", [FormaPago.EFECTIVO, FormaPago.TARJETA])
def test_c04_acepta_fecha_futura_con_parque_abierto(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    fecha_actual: date,
    calendario: CalendarioDoble,
    repositorio: RepositorioDoble,
    forma_pago: FormaPago,
) -> None:
    fecha_visita = fecha_actual + timedelta(days=1)
    solicitud = crear_solicitud(fecha_visita=fecha_visita, forma_pago=forma_pago)
    assert calendario.esta_abierto(fecha_visita) is True

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    assert resultado.compra.fecha_visita == fecha_visita
    compra_registrada = repositorio.obtener(resultado.compra.id_compra)
    assert compra_registrada is not None
    assert compra_registrada.fecha_visita == fecha_visita
