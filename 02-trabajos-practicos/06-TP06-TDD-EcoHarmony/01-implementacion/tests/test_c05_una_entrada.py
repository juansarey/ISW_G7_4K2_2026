"""C05 — Compra válida de exactamente una entrada."""

from ecoharmony.modelos import FormaPago


def test_c05_acepta_exactamente_una_entrada(servicio_compras, crear_solicitud):
    solicitud = crear_solicitud(
        cantidad_entradas=1,
        edades=(24,),
        forma_pago=FormaPago.EFECTIVO,
    )

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    assert resultado.compra.cantidad_entradas == 1