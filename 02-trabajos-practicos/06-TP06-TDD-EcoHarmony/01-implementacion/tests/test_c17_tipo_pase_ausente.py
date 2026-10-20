"""C17 (CA01) — Rechazar la compra cuando no se indica el tipo de pase.

Se parte de la solicitud base y se deja sin elegir únicamente el tipo de pase
(None). Se prueba con efectivo y con tarjeta de crédito para garantizar que la
falta de tipo de pase corta el proceso antes de registrar la compra, iniciar el
pago o solicitar el correo.
"""

from collections.abc import Callable

import pytest

from ecoharmony.modelos import FormaPago, MotivoRechazo, SolicitudCompra
from ecoharmony.servicio_compras import ServicioCompras
from tests.dobles import CorreoDoble, PagoDoble, RepositorioDoble


@pytest.mark.parametrize("forma_pago", [FormaPago.EFECTIVO, FormaPago.TARJETA])
def test_c17_rechaza_compra_sin_tipo_de_pase(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
    forma_pago: FormaPago,
) -> None:
    solicitud = crear_solicitud(tipo_pase=None, forma_pago=forma_pago)

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is False
    assert resultado.motivo == MotivoRechazo.TIPO_PASE_AUSENTE
    assert resultado.compra is None
    assert resultado.url_redireccion is None
    assert repositorio.compras == {}
    assert pago.solicitudes == []
    assert correo.intentos == []
