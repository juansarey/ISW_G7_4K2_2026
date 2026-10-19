"""C06 — Compra válida de exactamente nueve entradas."""

from ecoharmony.modelos import FormaPago


def test_c06_acepta_y_conserva_nueve_entradas(servicio_compras, crear_solicitud):
    edades = (24,) * 9
    solicitud = crear_solicitud(
        cantidad_entradas=9,
        edades=edades,
        forma_pago=FormaPago.EFECTIVO,
    )

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    assert resultado.compra.cantidad_entradas == 9
    assert resultado.compra.edades == edades