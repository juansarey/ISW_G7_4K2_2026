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
    FormaPago,
    MotivoRechazo,
    ResultadoCompra,
    SolicitudCompra,
)
from ecoharmony.tarifas import MAXIMO_ENTRADAS, calcular_total


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
        if (
            solicitud.fecha_visita is not None
            and solicitud.fecha_visita < self._reloj.hoy()
        ):
            return ResultadoCompra(aceptada=False, motivo=MotivoRechazo.FECHA_PASADA)
        if solicitud.fecha_visita is not None and not self._calendario.esta_abierto(
            solicitud.fecha_visita
        ):
            return ResultadoCompra(aceptada=False, motivo=MotivoRechazo.PARQUE_CERRADO)
        cantidad = solicitud.cantidad_entradas
        if cantidad is not None and cantidad > MAXIMO_ENTRADAS:
            return ResultadoCompra(
                aceptada=False,
                motivo=MotivoRechazo.CANTIDAD_EXCEDE_MAXIMO,
            )
        if solicitud.forma_pago == FormaPago.TARJETA:
            return self._iniciar_pago_con_tarjeta(solicitud)
        return self._confirmar_en_efectivo(solicitud)

    def _confirmar_en_efectivo(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        """A02: la compra queda confirmada y el pago se hace en boletería."""
        compra = self._crear_compra(
            solicitud, EstadoCompra.CONFIRMADA, EstadoPago.PENDIENTE_BOLETERIA
        )
        self._repositorio.guardar(compra)
        self._servicio_correo.enviar_confirmacion(compra)
        compra.estado_correo = EstadoCorreo.ENVIADO
        return ResultadoCompra(aceptada=True, compra=compra)

    def _iniciar_pago_con_tarjeta(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        """A02 y DD05: abrir la pasarela no acredita el pago; todo queda pendiente."""
        compra = self._crear_compra(
            solicitud, EstadoCompra.PENDIENTE, EstadoPago.PENDIENTE_PASARELA
        )
        self._repositorio.guardar(compra)
        url_redireccion = self._servicio_pago.iniciar_pago_tarjeta(
            compra.id_compra, compra.total
        )
        return ResultadoCompra(
            aceptada=True, compra=compra, url_redireccion=url_redireccion
        )

    def _crear_compra(
        self,
        solicitud: SolicitudCompra,
        estado_compra: EstadoCompra,
        estado_pago: EstadoPago,
    ) -> Compra:
        return Compra(
            id_compra=uuid4().hex,
            usuario=solicitud.usuario,
            fecha_visita=solicitud.fecha_visita,
            cantidad_entradas=solicitud.cantidad_entradas,
            edades=solicitud.edades,
            tipo_pase=solicitud.tipo_pase,
            forma_pago=solicitud.forma_pago,
            total=calcular_total(solicitud.cantidad_entradas, solicitud.tipo_pase),
            estado_compra=estado_compra,
            estado_pago=estado_pago,
        )
