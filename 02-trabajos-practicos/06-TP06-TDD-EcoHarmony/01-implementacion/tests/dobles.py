"""Dobles controlados para los tests (DD04, regla 11).

Cada doble registra las interacciones para poder verificarlas y permite
configurar fallos (A04). Se crean nuevos en cada test mediante las fixtures de
``conftest.py``.
"""

from datetime import date
from decimal import Decimal

from ecoharmony.dependencias import ErrorServicioCorreo, ErrorServicioPago
from ecoharmony.modelos import Compra

URL_PASARELA_DOBLE = "https://pasarela.doble/pago"


class RelojDoble:
    def __init__(self, fecha_actual: date) -> None:
        self.fecha_actual = fecha_actual

    def hoy(self) -> date:
        return self.fecha_actual


class CalendarioDoble:
    """Solo están abiertas las fechas indicadas; el resto se considera cerrado."""

    def __init__(self, dias_abiertos: set[date]) -> None:
        self.dias_abiertos = dias_abiertos

    def esta_abierto(self, fecha: date) -> bool:
        return fecha in self.dias_abiertos


class PagoDoble:
    def __init__(self, falla_al_iniciar: bool = False) -> None:
        self.falla_al_iniciar = falla_al_iniciar
        self.solicitudes: list[tuple[str, Decimal]] = []

    def iniciar_pago_tarjeta(self, id_compra: str, monto: Decimal) -> str:
        self.solicitudes.append((id_compra, monto))
        if self.falla_al_iniciar:
            raise ErrorServicioPago("Fallo configurado en el doble de pago.")
        return f"{URL_PASARELA_DOBLE}/{id_compra}"


class CorreoDoble:
    def __init__(self, falla_al_enviar: bool = False) -> None:
        self.falla_al_enviar = falla_al_enviar
        self.intentos: list[Compra] = []

    def enviar_confirmacion(self, compra: Compra) -> None:
        self.intentos.append(compra)
        if self.falla_al_enviar:
            raise ErrorServicioCorreo("Fallo configurado en el doble de correo.")


class RepositorioDoble:
    def __init__(self) -> None:
        self.compras: dict[str, Compra] = {}

    def guardar(self, compra: Compra) -> None:
        self.compras[compra.id_compra] = compra

    def obtener(self, id_compra: str) -> Compra | None:
        return self.compras.get(id_compra)
