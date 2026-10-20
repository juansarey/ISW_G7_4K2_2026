"""C12 — Rechazar once entradas con once edades válidas."""

from collections.abc import Callable

import pytest

from ecoharmony.modelos import FormaPago, MotivoRechazo, SolicitudCompra
from ecoharmony.servicio_compras import ServicioCompras
from ecoharmony.tarifas import MAXIMO_ENTRADAS
from tests.dobles import CorreoDoble, PagoDoble, RepositorioDoble


@pytest.mark.parametrize("forma_pago", [FormaPago.EFECTIVO, FormaPago.TARJETA])
def test_c12_rechaza_mas_de_diez_entradas(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
    forma_pago: FormaPago,
) -> None:
    cantidad = MAXIMO_ENTRADAS + 1
    solicitud = crear_solicitud(
        cantidad_entradas=cantidad,
        edades=(30,) * cantidad,
        forma_pago=forma_pago,
    )

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is False
    assert resultado.motivo == MotivoRechazo.CANTIDAD_EXCEDE_MAXIMO
    assert resultado.compra is None
    assert resultado.url_redireccion is None
    assert pago.solicitudes == []
    assert correo.intentos == []
    assert repositorio.compras == {}
