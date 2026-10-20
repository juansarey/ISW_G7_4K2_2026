"""C15 (CA01) — Rechazar la compra cuando no se indica fecha de visita.

Se parte de la solicitud base (usuario registrado, dos entradas con sus dos edades,
pase regular) y se deja la fecha de visita sin indicar (None). Se prueba tanto con
efectivo como con tarjeta de crédito para garantizar que la falta de fecha corta el
proceso antes de que se inicie el pago, se envíe el correo o se guarde la compra.
"""

from collections.abc import Callable

import pytest

from ecoharmony.modelos import FormaPago, MotivoRechazo, SolicitudCompra
from ecoharmony.servicio_compras import ServicioCompras
from tests.dobles import CorreoDoble, PagoDoble, RepositorioDoble


@pytest.mark.parametrize("forma_pago", [FormaPago.EFECTIVO, FormaPago.TARJETA])
def test_c15_rechaza_compra_sin_fecha_de_visita(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
    forma_pago: FormaPago,
) -> None:
    solicitud = crear_solicitud(
        fecha_visita=None,
        forma_pago=forma_pago,
    )

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is False
    assert resultado.motivo == MotivoRechazo.FECHA_AUSENTE
    assert resultado.compra is None
    assert resultado.url_redireccion is None
    assert repositorio.compras == {}
    assert pago.solicitudes == []
    assert correo.intentos == []
