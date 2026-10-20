"""C09 — Compra válida con pase regular."""

from decimal import Decimal

from ecoharmony.modelos import TipoPase


def test_c09_acepta_y_conserva_el_pase_regular(servicio_compras, crear_solicitud):
    solicitud = crear_solicitud(tipo_pase=TipoPase.REGULAR)

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    assert resultado.compra.tipo_pase == TipoPase.REGULAR
    assert resultado.compra.total == Decimal("20000")
