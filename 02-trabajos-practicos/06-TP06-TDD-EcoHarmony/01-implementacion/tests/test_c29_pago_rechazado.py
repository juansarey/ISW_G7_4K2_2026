"""C29 — Rechazo de pago sin confirmar la compra ni solicitar correo."""

from collections.abc import Callable

from ecoharmony.modelos import (
    EstadoCompra,
    EstadoCorreo,
    EstadoPago,
    FormaPago,
    SolicitudCompra,
)
from ecoharmony.servicio_compras import ServicioCompras
from tests.dobles import CorreoDoble, PagoDoble, RepositorioDoble


def test_c29_rechaza_pago_y_conserva_estados_sin_correo(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
) -> None:
    # Preparación: iniciar una compra válida con tarjeta.
    inicio = servicio_compras.comprar(crear_solicitud(forma_pago=FormaPago.TARJETA))
    assert inicio.compra is not None
    id_compra = inicio.compra.id_compra

    # Ejecución: procesar el rechazo informado por la pasarela.
    resultado = servicio_compras.registrar_resultado_pago(id_compra, aprobado=False)

    # Verificación: cancelar la compra y conservar el rechazo sin enviar correo.
    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    assert resultado.compra.estado_compra == EstadoCompra.CANCELADA
    assert resultado.compra.estado_pago == EstadoPago.RECHAZADO
    assert resultado.compra.estado_correo == EstadoCorreo.NO_SOLICITADO
    assert pago.solicitudes == [(id_compra, resultado.compra.total)]
    assert correo.intentos == []

    registrada = repositorio.obtener(id_compra)
    assert registrada is not None
    assert registrada.estado_compra == EstadoCompra.CANCELADA
    assert registrada.estado_pago == EstadoPago.RECHAZADO
    assert registrada.estado_correo == EstadoCorreo.NO_SOLICITADO
    assert len(repositorio.compras) == 1
