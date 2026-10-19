"""Modelos del contrato de implementación.

Ver 00-documentacion/TP06-DES-EcoHarmony-Contrato-Implementacion.md.

Los campos que el visitante puede omitir se representan con ``None``. El límite de
entrada (``ecoharmony.entrada``) es el único lugar que convierte texto en estos
tipos; la lógica de compra recibe siempre fechas, enteros y opciones ya
convertidos.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum


class TipoPase(Enum):
    REGULAR = "REGULAR"
    VIP = "VIP"


class FormaPago(Enum):
    EFECTIVO = "EFECTIVO"
    TARJETA = "TARJETA"


class EstadoCompra(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"


class EstadoPago(Enum):
    PENDIENTE_BOLETERIA = "PENDIENTE_BOLETERIA"
    PENDIENTE_PASARELA = "PENDIENTE_PASARELA"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"


class EstadoCorreo(Enum):
    NO_SOLICITADO = "NO_SOLICITADO"
    ENVIADO = "ENVIADO"
    CORREO_PENDIENTE = "CORREO_PENDIENTE"


class MotivoRechazo(Enum):
    """Identificadores estables que los tests comprueban y la interfaz traduce."""

    USUARIO_NO_REGISTRADO = "USUARIO_NO_REGISTRADO"
    FECHA_AUSENTE = "FECHA_AUSENTE"
    FECHA_FORMATO_INVALIDO = "FECHA_FORMATO_INVALIDO"
    FECHA_PASADA = "FECHA_PASADA"
    PARQUE_CERRADO = "PARQUE_CERRADO"
    CANTIDAD_AUSENTE = "CANTIDAD_AUSENTE"
    CANTIDAD_INVALIDA = "CANTIDAD_INVALIDA"
    CANTIDAD_EXCEDE_MAXIMO = "CANTIDAD_EXCEDE_MAXIMO"
    EDADES_INCOMPLETAS = "EDADES_INCOMPLETAS"
    EDAD_INVALIDA = "EDAD_INVALIDA"
    TIPO_PASE_AUSENTE = "TIPO_PASE_AUSENTE"
    TIPO_PASE_INVALIDO = "TIPO_PASE_INVALIDO"
    FORMA_PAGO_AUSENTE = "FORMA_PAGO_AUSENTE"
    FORMA_PAGO_INVALIDA = "FORMA_PAGO_INVALIDA"
    ERROR_PAGO = "ERROR_PAGO"


@dataclass(frozen=True)
class Usuario:
    nombre_usuario: str
    correo: str
    registrado: bool


@dataclass(frozen=True)
class SolicitudCompra:
    usuario: Usuario
    fecha_visita: date | None
    cantidad_entradas: int | None
    edades: tuple[int, ...]
    tipo_pase: TipoPase | None
    forma_pago: FormaPago | None


@dataclass
class Compra:
    """Compra registrada. Es mutable porque su estado avanza según A02 y A04."""

    id_compra: str
    usuario: Usuario
    fecha_visita: date
    cantidad_entradas: int
    edades: tuple[int, ...]
    tipo_pase: TipoPase
    forma_pago: FormaPago
    total: Decimal
    estado_compra: EstadoCompra
    estado_pago: EstadoPago
    estado_correo: EstadoCorreo = EstadoCorreo.NO_SOLICITADO


@dataclass(frozen=True)
class ResultadoCompra:
    """Único mecanismo para comunicar el resultado de ``ServicioCompras.comprar``.

    - Aceptada: ``aceptada=True``, ``compra`` presente y ``motivo=None``.
    - Rechazada: ``aceptada=False``, ``motivo`` presente y ``compra=None``.
    - ``url_redireccion`` solo existe cuando se abrió la pasarela de tarjeta.
    """

    aceptada: bool
    compra: Compra | None = None
    motivo: MotivoRechazo | None = None
    url_redireccion: str | None = None
