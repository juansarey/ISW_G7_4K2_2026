"""Coordinación de la compra de entradas (User Story «Comprar entradas»)."""

from uuid import uuid4

from ecoharmony.dependencias import (
    Calendario,
    ErrorServicioCorreo,
    ErrorServicioPago,
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
        motivo = self._motivo_de_rechazo(solicitud)
        if motivo is not None:
            return ResultadoCompra(aceptada=False, motivo=motivo)
        if solicitud.forma_pago == FormaPago.TARJETA:
            return self._iniciar_pago_con_tarjeta(solicitud)
        return self._confirmar_en_efectivo(solicitud)

    def _motivo_de_rechazo(self, solicitud: SolicitudCompra) -> MotivoRechazo | None:
        """Primer motivo que impide la compra, o ``None`` si la solicitud es válida.

        Respeta el orden del contrato (§4): usuario, fecha, cantidad, edades, tipo
        de pase y forma de pago. No produce efectos: se consulta antes de registrar
        la compra, iniciar el pago o enviar el correo.
        """
        if not solicitud.usuario.registrado:
            return MotivoRechazo.USUARIO_NO_REGISTRADO
        fecha = solicitud.fecha_visita
        if fecha is None:
            return MotivoRechazo.FECHA_AUSENTE
        if fecha < self._reloj.hoy():
            return MotivoRechazo.FECHA_PASADA
        if not self._calendario.esta_abierto(fecha):
            return MotivoRechazo.PARQUE_CERRADO
        cantidad = solicitud.cantidad_entradas
        if cantidad is None:
            return MotivoRechazo.CANTIDAD_AUSENTE
        if cantidad <= 0:
            return MotivoRechazo.CANTIDAD_INVALIDA
        if cantidad > MAXIMO_ENTRADAS:
            return MotivoRechazo.CANTIDAD_EXCEDE_MAXIMO
        if len(solicitud.edades) < cantidad:
            return MotivoRechazo.EDADES_INCOMPLETAS
        if any(edad < 0 for edad in solicitud.edades):
            return MotivoRechazo.EDAD_INVALIDA
        if solicitud.tipo_pase is None:
            return MotivoRechazo.TIPO_PASE_AUSENTE
        if solicitud.forma_pago is None:
            return MotivoRechazo.FORMA_PAGO_AUSENTE
        return None

    def _confirmar_en_efectivo(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        """Confirma la compra; un fallo de correo no modifica compra ni pago."""
        compra = self._crear_compra(
            solicitud, EstadoCompra.CONFIRMADA, EstadoPago.PENDIENTE_BOLETERIA
        )
        self._repositorio.guardar(compra)
        self._solicitar_correo_confirmacion(compra)
        return ResultadoCompra(aceptada=True, compra=compra)

    def _solicitar_correo_confirmacion(self, compra: Compra) -> None:
        """Conserva la compra ante un fallo específico del correo (A04)."""
        try:
            self._servicio_correo.enviar_confirmacion(compra)
        except ErrorServicioCorreo:
            compra.estado_correo = EstadoCorreo.CORREO_PENDIENTE
        else:
            compra.estado_correo = EstadoCorreo.ENVIADO

        self._repositorio.guardar(compra)

    def registrar_resultado_pago(
        self, id_compra: str, aprobado: bool
    ) -> ResultadoCompra:
        """Procesa una notificación simulada según A02.

        Aceptada indica que se procesó la notificación; los estados informan
        el resultado del pago.
        """
        compra = self._repositorio.obtener(id_compra)
        if compra is None:
            raise ValueError("Compra inexistente.")

        if compra.forma_pago != FormaPago.TARJETA:
            raise ValueError("La compra no corresponde a un pago con tarjeta.")

        estado_destino = EstadoCompra.CONFIRMADA if aprobado else EstadoCompra.CANCELADA
        pago_destino = EstadoPago.APROBADO if aprobado else EstadoPago.RECHAZADO

        estado_actual = (compra.estado_compra, compra.estado_pago)
        destino = (estado_destino, pago_destino)

        if estado_actual == destino:
            return ResultadoCompra(aceptada=True, compra=compra)

        pendiente = (EstadoCompra.PENDIENTE, EstadoPago.PENDIENTE_PASARELA)
        if estado_actual != pendiente:
            raise ValueError("El pago ya fue resuelto o su estado es incompatible.")

        compra.estado_compra = estado_destino
        compra.estado_pago = pago_destino
        self._repositorio.guardar(compra)

        if aprobado:
            self._solicitar_correo_confirmacion(compra)

        return ResultadoCompra(aceptada=True, compra=compra)

    def reintentar_correo(self, id_compra: str) -> ResultadoCompra:
        """Reenvía la confirmación solo cuando quedó pendiente (A04)."""
        compra = self._repositorio.obtener(id_compra)
        if compra is None:
            raise ValueError("Compra inexistente.")
        if compra.estado_correo != EstadoCorreo.CORREO_PENDIENTE:
            raise ValueError("El correo no está pendiente de reintento.")

        self._solicitar_correo_confirmacion(compra)
        return ResultadoCompra(aceptada=True, compra=compra)

    def _iniciar_pago_con_tarjeta(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        """A02 y DD05: abrir la pasarela no acredita el pago; todo queda pendiente."""
        compra = self._crear_compra(
            solicitud, EstadoCompra.PENDIENTE, EstadoPago.PENDIENTE_PASARELA
        )
        self._repositorio.guardar(compra)
        try:
            url_redireccion = self._servicio_pago.iniciar_pago_tarjeta(
                compra.id_compra, compra.total
            )
        except ErrorServicioPago:
            return ResultadoCompra(
                aceptada=False,
                motivo=MotivoRechazo.ERROR_PAGO,
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
