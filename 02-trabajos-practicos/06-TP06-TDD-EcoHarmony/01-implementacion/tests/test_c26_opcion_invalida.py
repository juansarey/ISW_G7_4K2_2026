"""C26 (DG02) — Rechazar opciones de pase y pago no admitidas."""

import pytest

from ecoharmony.modelos import MotivoRechazo
from ecoharmony.web.app import crear_app


@pytest.mark.parametrize(
    ("campo", "valor", "motivo"),
    [
        ("tipo_pase", "PREMIUM", MotivoRechazo.TIPO_PASE_INVALIDO),
        ("forma_pago", "TRANSFERENCIA", MotivoRechazo.FORMA_PAGO_INVALIDA),
    ],
)
def test_c26_rechaza_opcion_no_admitida(
    campo: str,
    valor: str,
    motivo: MotivoRechazo,
) -> None:
    datos = {
        "usuario": "visitante01",
        "fecha_visita": "2030-06-13",
        "cantidad_entradas": 2,
        "edades": [24, 36],
        "tipo_pase": "REGULAR",
        "forma_pago": "EFECTIVO",
    }
    datos[campo] = valor

    respuesta = crear_app().test_client().post("/api/compras", json=datos)

    assert respuesta.status_code == 400
    assert respuesta.json["aceptada"] is False
    assert respuesta.json["motivo"] == motivo.value
    assert respuesta.json["compra"] is None
