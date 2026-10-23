"""C27 (DG03) — Rechazar fecha con formato inválido en el límite de entrada."""

import pytest

from ecoharmony.entrada import ErrorEntrada, convertir_solicitud
from ecoharmony.modelos import MotivoRechazo, Usuario
from ecoharmony.web.app import crear_app


@pytest.mark.parametrize(
    "fecha_invalida",
    [
        "no-es-una-fecha",
        "2030/06/13",
        "13-06-2030",
        "2030-02-31",
    ],
)
def test_c27_rechaza_formato_fecha_invalido_en_limite_de_entrada(
    fecha_invalida: str,
) -> None:
    usuario = Usuario("visitante01", "visitante@example.com", registrado=True)
    datos = {
        "usuario": "visitante01",
        "fecha_visita": fecha_invalida,
        "cantidad_entradas": 2,
        "edades": [24, 36],
        "tipo_pase": "REGULAR",
        "forma_pago": "EFECTIVO",
    }

    with pytest.raises(ErrorEntrada) as exc_info:
        convertir_solicitud(datos, usuario)

    assert exc_info.value.motivo == MotivoRechazo.FECHA_FORMATO_INVALIDO


def test_c27_rechaza_fecha_formato_invalido_en_api() -> None:
    cliente = crear_app().test_client()
    respuesta = cliente.post(
        "/api/compras",
        json={
            "usuario": "visitante01",
            "fecha_visita": "fecha-invalida",
            "cantidad_entradas": 2,
            "edades": [24, 36],
            "tipo_pase": "REGULAR",
            "forma_pago": "EFECTIVO",
        },
    )

    assert respuesta.status_code == 400
    assert respuesta.json["aceptada"] is False
    assert respuesta.json["motivo"] == MotivoRechazo.FECHA_FORMATO_INVALIDO.value
    assert respuesta.json["compra"] is None
