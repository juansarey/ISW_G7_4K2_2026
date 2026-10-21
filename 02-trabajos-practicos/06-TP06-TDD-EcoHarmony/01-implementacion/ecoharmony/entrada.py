"""Límite de entrada: convierte los datos de la interfaz en tipos del dominio.

Un valor vacío o ausente se convierte en ``None`` (o se omite, en las edades) para
que la lógica de compra pueda rechazarlo con su motivo. Las cantidades no enteras
y las opciones no admitidas producen ``ErrorEntrada`` con motivos estables; los
formatos de fecha y edad todavía propagan ``ValueError``.
"""

from collections.abc import Mapping
from datetime import date
from enum import Enum
from typing import TypeVar

from ecoharmony.modelos import (
    FormaPago,
    MotivoRechazo,
    SolicitudCompra,
    TipoPase,
    Usuario,
)

Opcion = TypeVar("Opcion", bound=Enum)


class ErrorEntrada(ValueError):
    def __init__(self, motivo: MotivoRechazo) -> None:
        self.motivo = motivo
        super().__init__(motivo.value)


def convertir_solicitud(
    datos: Mapping[str, object], usuario: Usuario
) -> SolicitudCompra:
    return SolicitudCompra(
        usuario=usuario,
        fecha_visita=_convertir_fecha(datos.get("fecha_visita")),
        cantidad_entradas=_convertir_entero(datos.get("cantidad_entradas")),
        edades=_convertir_edades(datos.get("edades")),
        tipo_pase=_convertir_opcion(TipoPase, datos.get("tipo_pase")),
        forma_pago=_convertir_opcion(FormaPago, datos.get("forma_pago")),
    )


def _texto_o_none(valor: object) -> str | None:
    if valor is None:
        return None
    texto = str(valor).strip()
    return texto or None


def _convertir_fecha(valor: object) -> date | None:
    texto = _texto_o_none(valor)
    return None if texto is None else date.fromisoformat(texto)


def _convertir_entero(valor: object) -> int | None:
    # Se convierte desde texto para que "2.5" no se trunque silenciosamente a 2.
    texto = _texto_o_none(valor)
    if texto is None:
        return None
    try:
        return int(texto)
    except ValueError as error:
        raise ErrorEntrada(MotivoRechazo.CANTIDAD_INVALIDA) from error


def _convertir_edades(valor: object) -> tuple[int, ...]:
    if not isinstance(valor, list | tuple):
        return ()
    textos = (_texto_o_none(edad) for edad in valor)
    return tuple(int(texto) for texto in textos if texto is not None)


def _convertir_opcion(tipo_opcion: type[Opcion], valor: object) -> Opcion | None:
    texto = _texto_o_none(valor)
    if texto is None:
        return None
    try:
        return tipo_opcion(texto)
    except ValueError as error:
        motivo = (
            MotivoRechazo.TIPO_PASE_INVALIDO
            if tipo_opcion is TipoPase
            else MotivoRechazo.FORMA_PAGO_INVALIDA
        )
        raise ErrorEntrada(motivo) from error
