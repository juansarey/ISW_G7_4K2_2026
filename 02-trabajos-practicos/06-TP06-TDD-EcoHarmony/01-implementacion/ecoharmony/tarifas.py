"""Tarifas ficticias de la simulación (A03), en pesos argentinos."""

from decimal import Decimal

from ecoharmony.modelos import TipoPase

MAXIMO_ENTRADAS = 10

TARIFAS_POR_PASE: dict[TipoPase, Decimal] = {
    TipoPase.REGULAR: Decimal("10000"),
    TipoPase.VIP: Decimal("15000"),
}


def calcular_total(cantidad_entradas: int, tipo_pase: TipoPase) -> Decimal:
    """Total = cantidad × tarifa, sin descuentos por edad ni cargos extra (A03)."""
    return TARIFAS_POR_PASE[tipo_pase] * cantidad_entradas
