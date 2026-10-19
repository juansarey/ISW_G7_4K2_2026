"""Coordinación de la compra de entradas (User Story «Comprar entradas»)."""

from ecoharmony.dependencias import (
    Calendario,
    Reloj,
    RepositorioCompras,
    ServicioCorreo,
    ServicioPago,
)
from ecoharmony.modelos import ResultadoCompra, SolicitudCompra


class ServicioCompras:
    def __init__(
        self,
        reloj: Reloj,
        calendario: Calendario,
        servicio_pago: ServicioPago,
        servicio_correo: ServicioCorreo,
        repositorio: RepositorioCompras,
    ) -> None:
        self._reloj = reloj
        self._calendario = calendario
        self._servicio_pago = servicio_pago
        self._servicio_correo = servicio_correo
        self._repositorio = repositorio

    def comprar(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        raise NotImplementedError("Pendiente: construir mediante TDD a partir de C01.")
