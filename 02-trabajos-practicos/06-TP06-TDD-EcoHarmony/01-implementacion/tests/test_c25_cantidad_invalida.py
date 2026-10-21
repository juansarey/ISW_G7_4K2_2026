"""C25 (DG01) — Rechazar cantidades de entradas inválidas."""

from collections.abc import Callable

import pytest

from ecoharmony.modelos import MotivoRechazo, SolicitudCompra
from ecoharmony.servicio_compras import ServicioCompras
from ecoharmony.web.app import crear_app
from tests.dobles import CorreoDoble, PagoDoble, RepositorioDoble


@pytest.mark.parametrize("cantidad", [0, -1])
def test_c25_rechaza_cantidad_no_positiva_sin_efectos(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
    cantidad: int,
) -> None:
    solicitud = crear_solicitud(cantidad_entradas=cantidad)

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is False
    assert resultado.motivo == MotivoRechazo.CANTIDAD_INVALIDA
    assert resultado.compra is None
    assert resultado.url_redireccion is None
    assert repositorio.compras == {}
    assert pago.solicitudes == []
    assert correo.intentos == []


def test_c25_rechaza_cantidad_no_entera_en_el_limite_de_entrada() -> None:
    cliente = crear_app().test_client()
    respuesta = cliente.post(
        "/api/compras",
        json={
            "usuario": "visitante01",
            "fecha_visita": "2030-06-13",
            "cantidad_entradas": "1.5",
            "edades": [24, 36],
            "tipo_pase": "REGULAR",
            "forma_pago": "EFECTIVO",
        },
    )

    assert respuesta.status_code == 400
    assert respuesta.json["aceptada"] is False
    assert respuesta.json["motivo"] == MotivoRechazo.CANTIDAD_INVALIDA.value
    assert respuesta.json["compra"] is None
