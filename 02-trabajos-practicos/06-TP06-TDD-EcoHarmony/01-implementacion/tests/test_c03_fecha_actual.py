"""C03 — Aceptar la fecha actual cuando el parque está abierto (CA02 y CA05).

Se cambia la fecha de la solicitud base por D0. Se comprueba la aceptación y la
conservación de la fecha en el resultado y en el registro para ambas formas de pago.
"""

from collections.abc import Callable
from datetime import date

import pytest

from ecoharmony.modelos import FormaPago, SolicitudCompra
from ecoharmony.servicio_compras import ServicioCompras
from tests.dobles import CalendarioDoble, RepositorioDoble


@pytest.mark.parametrize("forma_pago", [FormaPago.EFECTIVO, FormaPago.TARJETA])
def test_c03_acepta_fecha_actual_con_parque_abierto(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    fecha_actual: date,
    calendario: CalendarioDoble,
    repositorio: RepositorioDoble,
    forma_pago: FormaPago,
) -> None:
    solicitud = crear_solicitud(fecha_visita=fecha_actual, forma_pago=forma_pago)
    assert calendario.esta_abierto(fecha_actual) is True

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    assert resultado.compra.fecha_visita == fecha_actual
    compra_registrada = repositorio.obtener(resultado.compra.id_compra)
    assert compra_registrada is not None
    assert compra_registrada.fecha_visita == fecha_actual
