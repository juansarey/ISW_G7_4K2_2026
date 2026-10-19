"""Servicios simulados para la demostración local (A01 y A04).

No realizan cobros ni envíos reales: registran las solicitudes para poder
mostrarlas en la interfaz. No constituyen una integración con Mercado Pago ni
con un servidor de correo.
"""

from datetime import date, timedelta
from decimal import Decimal

from ecoharmony.modelos import Compra

DIA_LUNES = 0


class RelojFijo:
    """Reloj detenido en una fecha; la demostración usa D0 = 12/06/2030 (A01)."""

    def __init__(self, fecha_actual: date) -> None:
        self._fecha_actual = fecha_actual

    def hoy(self) -> date:
        return self._fecha_actual


class CalendarioParque:
    """Abre de martes a domingo, cierra los lunes y en cierres excepcionales (A01)."""

    def __init__(self, cierres_excepcionales: set[date] | None = None) -> None:
        self._cierres_excepcionales = cierres_excepcionales or set()

    def esta_abierto(self, fecha: date) -> bool:
        if fecha.weekday() == DIA_LUNES:
            return False
        return fecha not in self._cierres_excepcionales

    def proximos_dias(self, desde: date, cantidad_dias: int) -> list[tuple[date, bool]]:
        """Ayuda para que la interfaz muestre el calendario simulado."""
        fechas = [desde + timedelta(days=dia) for dia in range(cantidad_dias)]
        return [(fecha, self.esta_abierto(fecha)) for fecha in fechas]


class PagoSimulado:
    """Pasarela local: devuelve una URL propia en lugar de redirigir a Mercado Pago."""

    def __init__(self) -> None:
        self.solicitudes: list[tuple[str, Decimal]] = []

    def iniciar_pago_tarjeta(self, id_compra: str, monto: Decimal) -> str:
        self.solicitudes.append((id_compra, monto))
        return f"/pasarela-simulada/{id_compra}"


class CorreoSimulado:
    """Bandeja de salida en memoria; la interfaz la muestra como correo enviado."""

    def __init__(self) -> None:
        self.enviados: list[Compra] = []

    def enviar_confirmacion(self, compra: Compra) -> None:
        self.enviados.append(compra)


class RepositorioComprasEnMemoria:
    def __init__(self) -> None:
        self._compras: dict[str, Compra] = {}

    def guardar(self, compra: Compra) -> None:
        self._compras[compra.id_compra] = compra

    def obtener(self, id_compra: str) -> Compra | None:
        return self._compras.get(id_compra)
