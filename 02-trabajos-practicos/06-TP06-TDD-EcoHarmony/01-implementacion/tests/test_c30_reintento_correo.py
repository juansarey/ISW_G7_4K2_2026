"""C30 — Reintentar el correo sin repetir la compra ni el pago."""

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


def test_c30_reintenta_correo_pendiente_sin_repetir_compra_ni_pago(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
) -> None:
    # Preparación: aprobar una compra con tarjeta cuyo primer correo falla.
    correo.falla_al_enviar = True
    inicio = servicio_compras.comprar(crear_solicitud(forma_pago=FormaPago.TARJETA))
    assert inicio.compra is not None
    id_compra = inicio.compra.id_compra
    aprobacion = servicio_compras.registrar_resultado_pago(id_compra, aprobado=True)
    assert aprobacion.compra is not None
    assert aprobacion.compra.estado_correo == EstadoCorreo.CORREO_PENDIENTE
    assert len(correo.intentos) == 1

    # Ejecución: restablecer el correo y reintentar solo el envío.
    correo.falla_al_enviar = False
    resultado = servicio_compras.reintentar_correo(id_compra)

    # Verificación: conservar compra y pago aprobados y completar el correo.
    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    assert resultado.compra.id_compra == id_compra
    assert resultado.compra.estado_compra == EstadoCompra.CONFIRMADA
    assert resultado.compra.estado_pago == EstadoPago.APROBADO
    assert resultado.compra.estado_correo == EstadoCorreo.ENVIADO
    assert [intento.id_compra for intento in correo.intentos] == [
        id_compra,
        id_compra,
    ]
    assert pago.solicitudes == [(id_compra, resultado.compra.total)]

    registrada = repositorio.obtener(id_compra)
    assert registrada is not None
    assert registrada.estado_compra == EstadoCompra.CONFIRMADA
    assert registrada.estado_pago == EstadoPago.APROBADO
    assert registrada.estado_correo == EstadoCorreo.ENVIADO
    assert len(repositorio.compras) == 1
