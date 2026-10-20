"""C16 (CA01) — Rechazar la compra cuando las edades están incompletas.

La solicitud base especifica dos entradas; aquí solo se informa la edad de un
visitante (una sola edad para dos entradas), dejando el resto de los datos válidos.
Se verifica tanto en efectivo como con tarjeta de crédito que la compra es rechazada
por no contar con la edad de cada visitante, sin guardar la compra, abrir la pasarela
de pago ni enviar correo de confirmación.
"""

from collections.abc import Callable

import pytest

from ecoharmony.modelos import FormaPago, MotivoRechazo, SolicitudCompra
from ecoharmony.servicio_compras import ServicioCompras
from tests.dobles import CorreoDoble, PagoDoble, RepositorioDoble


@pytest.mark.parametrize("forma_pago", [FormaPago.EFECTIVO, FormaPago.TARJETA])
def test_c16_rechaza_compra_con_edades_incompletas(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
    forma_pago: FormaPago,
) -> None:
    # Dos entradas (de la solicitud base) pero solo una edad informada.
    solicitud = crear_solicitud(
        cantidad_entradas=2,
        edades=(24,),
        forma_pago=forma_pago,
    )

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is False
    assert resultado.motivo == MotivoRechazo.EDADES_INCOMPLETAS
    assert resultado.compra is None
    assert resultado.url_redireccion is None
    assert repositorio.compras == {}
    assert pago.solicitudes == []
    assert correo.intentos == []
