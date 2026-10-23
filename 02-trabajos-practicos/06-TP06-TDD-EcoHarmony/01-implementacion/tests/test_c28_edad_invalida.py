"""C28 (DG04) — Rechazar edades negativas o no enteras."""

from collections.abc import Callable

import pytest

from ecoharmony.entrada import ErrorEntrada, convertir_solicitud
from ecoharmony.modelos import MotivoRechazo, SolicitudCompra, Usuario
from ecoharmony.servicio_compras import ServicioCompras
from ecoharmony.web.app import crear_app
from tests.dobles import CorreoDoble, PagoDoble, RepositorioDoble


@pytest.mark.parametrize(
    "edades",
    [
        (-1, 30),
        (25, -5),
    ],
)
def test_c28_rechaza_edad_negativa_en_servicio_sin_efectos(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
    edades: tuple[int, ...],
) -> None:
    solicitud = crear_solicitud(cantidad_entradas=2, edades=edades)

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is False
    assert resultado.motivo == MotivoRechazo.EDAD_INVALIDA
    assert resultado.compra is None
    assert resultado.url_redireccion is None
    assert repositorio.compras == {}
    assert pago.solicitudes == []
    assert correo.intentos == []


@pytest.mark.parametrize(
    "edad_no_entera",
    [
        "25.5",
        "veinte",
    ],
)
def test_c28_rechaza_edad_no_entera_en_limite_de_entrada(
    edad_no_entera: str,
) -> None:
    usuario = Usuario("visitante01", "visitante@example.com", registrado=True)
    datos = {
        "usuario": "visitante01",
        "fecha_visita": "2030-06-13",
        "cantidad_entradas": 2,
        "edades": [edad_no_entera, 30],
        "tipo_pase": "REGULAR",
        "forma_pago": "EFECTIVO",
    }

    with pytest.raises(ErrorEntrada) as exc_info:
        convertir_solicitud(datos, usuario)

    assert exc_info.value.motivo == MotivoRechazo.EDAD_INVALIDA


def test_c28_rechaza_edad_no_entera_en_api() -> None:
    cliente = crear_app().test_client()
    respuesta = cliente.post(
        "/api/compras",
        json={
            "usuario": "visitante01",
            "fecha_visita": "2030-06-13",
            "cantidad_entradas": 2,
            "edades": ["25.5", 30],
            "tipo_pase": "REGULAR",
            "forma_pago": "EFECTIVO",
        },
    )

    assert respuesta.status_code == 400
    assert respuesta.json["aceptada"] is False
    assert respuesta.json["motivo"] == MotivoRechazo.EDAD_INVALIDA.value
    assert respuesta.json["compra"] is None


def test_c28_acepta_edad_cero_y_edad_avanzada_sin_limite_ni_descuento(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
) -> None:
    solicitud = crear_solicitud(cantidad_entradas=2, edades=(0, 105))

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    assert resultado.compra.edades == (0, 105)
