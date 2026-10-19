"""Interfaces de las dependencias controlables (DD01).

La lógica de compra solo conoce estos protocolos. La demostración usa las
implementaciones de ``ecoharmony.simulados`` y los tests, los dobles de
``tests/dobles.py``.
"""

from datetime import date
from decimal import Decimal
from typing import Protocol

from ecoharmony.modelos import Compra


class ErrorServicioPago(Exception):
    """El servicio de pago no pudo iniciar la operación (A04, C21)."""


class ErrorServicioCorreo(Exception):
    """El servicio de correo no pudo enviar la confirmación (A04, C19)."""


class Reloj(Protocol):
    def hoy(self) -> date: ...


class Calendario(Protocol):
    def esta_abierto(self, fecha: date) -> bool: ...


class ServicioPago(Protocol):
    def iniciar_pago_tarjeta(self, id_compra: str, monto: Decimal) -> str:
        """Solicita la redirección a la pasarela y devuelve su URL.

        Iniciar el pago no lo aprueba (DD05). Lanza ``ErrorServicioPago`` si falla.
        """
        ...


class ServicioCorreo(Protocol):
    def enviar_confirmacion(self, compra: Compra) -> None:
        """Envía la confirmación al correo del usuario de la compra.

        Lanza ``ErrorServicioCorreo`` si el envío falla.
        """
        ...


class RepositorioCompras(Protocol):
    def guardar(self, compra: Compra) -> None: ...

    def obtener(self, id_compra: str) -> Compra | None: ...
