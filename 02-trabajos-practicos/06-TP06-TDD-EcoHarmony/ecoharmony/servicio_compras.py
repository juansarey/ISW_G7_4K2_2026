"""Coordinación de la compra de entradas (User Story «Comprar entradas»)."""

from uuid import uuid4

from ecoharmony.dependencias import (
    Calendario,
    Reloj,
    RepositorioCompras,
    ServicioCorreo,
    ServicioPago,
)
from ecoharmony.modelos import (
    Compra,
    EstadoCompra,
    EstadoCorreo,
    EstadoPago,
    ResultadoCompra,
    SolicitudCompra,
)
from ecoharmony.tarifas import calcular_total


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
        compra = Compra(
            id_compra=uuid4().hex,
            usuario=solicitud.usuario,
            fecha_visita=solicitud.fecha_visita,
            cantidad_entradas=solicitud.cantidad_entradas,
            edades=solicitud.edades,
            tipo_pase=solicitud.tipo_pase,
            forma_pago=solicitud.forma_pago,
            total=calcular_total(solicitud.cantidad_entradas, solicitud.tipo_pase),
            estado_compra=EstadoCompra.CONFIRMADA,
            estado_pago=EstadoPago.PENDIENTE_BOLETERIA,
        )
        self._repositorio.guardar(compra)
        self._servicio_correo.enviar_confirmacion(compra)
        compra.estado_correo = EstadoCorreo.ENVIADO
        return ResultadoCompra(aceptada=True, compra=compra)
