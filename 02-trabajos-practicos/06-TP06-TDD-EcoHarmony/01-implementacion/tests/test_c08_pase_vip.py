"""C08 — Compra válida con pase VIP."""

from decimal import Decimal

from ecoharmony.modelos import TipoPase


def test_c08_acepta_y_conserva_el_pase_vip(servicio_compras, crear_solicitud):
    solicitud = crear_solicitud(tipo_pase=TipoPase.VIP)

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    assert resultado.compra.tipo_pase == TipoPase.VIP
    assert resultado.compra.total == Decimal("30000")
