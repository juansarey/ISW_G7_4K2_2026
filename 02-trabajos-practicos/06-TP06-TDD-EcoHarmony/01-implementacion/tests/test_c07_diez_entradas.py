"""C07 — Compra válida de exactamente diez entradas."""

from decimal import Decimal

from ecoharmony.modelos import FormaPago


def test_c07_acepta_el_maximo_de_diez_entradas(servicio_compras, crear_solicitud):
    edades = (24,) * 10
    solicitud = crear_solicitud(
        cantidad_entradas=10,
        edades=edades,
        forma_pago=FormaPago.EFECTIVO,
    )

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    assert resultado.compra.cantidad_entradas == 10
    assert resultado.compra.edades == edades
    assert resultado.compra.total == Decimal("100000")
