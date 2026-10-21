"""Traducción de los motivos estables del contrato a mensajes para el visitante."""

from ecoharmony.modelos import MotivoRechazo

MENSAJES_RECHAZO: dict[MotivoRechazo, str] = {
    MotivoRechazo.USUARIO_NO_REGISTRADO: (
        "Solo los usuarios registrados pueden comprar entradas."
    ),
    MotivoRechazo.FECHA_AUSENTE: "Indicá la fecha de visita.",
    MotivoRechazo.FECHA_FORMATO_INVALIDO: "La fecha de visita no es una fecha válida.",
    MotivoRechazo.FECHA_PASADA: "La fecha de visita no puede ser anterior a hoy.",
    MotivoRechazo.PARQUE_CERRADO: "El parque está cerrado en la fecha elegida.",
    MotivoRechazo.CANTIDAD_AUSENTE: "Indicá la cantidad de entradas.",
    MotivoRechazo.CANTIDAD_INVALIDA: (
        "La cantidad de entradas debe ser un número entero mayor que cero."
    ),
    MotivoRechazo.CANTIDAD_EXCEDE_MAXIMO: (
        "No se pueden comprar más de diez entradas por operación."
    ),
    MotivoRechazo.EDADES_INCOMPLETAS: "Indicá la edad de cada visitante.",
    MotivoRechazo.EDAD_INVALIDA: "Las edades deben ser números enteros no negativos.",
    MotivoRechazo.TIPO_PASE_AUSENTE: "Seleccioná el tipo de pase (regular o VIP).",
    MotivoRechazo.TIPO_PASE_INVALIDO: "El tipo de pase elegido no existe.",
    MotivoRechazo.FORMA_PAGO_AUSENTE: "Seleccioná la forma de pago.",
    MotivoRechazo.FORMA_PAGO_INVALIDA: "La forma de pago elegida no está disponible.",
    MotivoRechazo.ERROR_PAGO: (
        "No se pudo iniciar el pago con tarjeta. La compra no fue confirmada."
    ),
}

MENSAJE_FORMATO_INVALIDO = (
    "Algún dato tiene un formato que no se puede interpretar. "
    "La validación de formatos de fecha y edad está pendiente (casos C27–C28)."
)

MENSAJE_ERROR_INTERNO = (
    "El servidor no pudo procesar la solicitud. Puede tratarse de un caso cuya "
    "validación todavía no se construyó (ver la asignación de casos del TP6)."
)
