"""C21 — Inicio del pago con tarjeta: éxito y fallo de la pasarela."""

from collections.abc import Callable
from decimal import Decimal

from ecoharmony.modelos import (
    EstadoCompra,
    EstadoCorreo,
    EstadoPago,
    FormaPago,
    MotivoRechazo,
    SolicitudCompra,
)
from ecoharmony.servicio_compras import ServicioCompras
from tests.dobles import (
    URL_PASARELA_DOBLE,
    CorreoDoble,
    PagoDoble,
    RepositorioDoble,
)


def test_c21_inicia_pago_una_vez_y_conserva_compra_pendiente_sin_correo(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
) -> None:
    # Preparación
    solicitud = crear_solicitud(forma_pago=FormaPago.TARJETA)

    # Ejecución
    resultado = servicio_compras.comprar(solicitud)

    # Verificación
    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    compra = resultado.compra

    assert compra.forma_pago == FormaPago.TARJETA
    assert compra.total == Decimal("20000")
    assert pago.solicitudes == [(compra.id_compra, compra.total)]
    assert resultado.url_redireccion == f"{URL_PASARELA_DOBLE}/{compra.id_compra}"

    assert compra.estado_compra == EstadoCompra.PENDIENTE
    assert compra.estado_pago == EstadoPago.PENDIENTE_PASARELA
    assert compra.estado_correo == EstadoCorreo.NO_SOLICITADO
    assert correo.intentos == []

    registrada = repositorio.obtener(compra.id_compra)
    assert registrada is not None
    assert registrada.id_compra == compra.id_compra
    assert registrada.estado_compra == EstadoCompra.PENDIENTE
    assert registrada.estado_pago == EstadoPago.PENDIENTE_PASARELA
    assert registrada.estado_correo == EstadoCorreo.NO_SOLICITADO
    assert len(repositorio.compras) == 1


def test_c21_rechaza_con_error_pago_si_falla_el_inicio_de_pasarela(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    pago: PagoDoble,
    correo: CorreoDoble,
) -> None:
    # Preparación
    pago.falla_al_iniciar = True
    solicitud = crear_solicitud(forma_pago=FormaPago.TARJETA)

    # Ejecución
    resultado = servicio_compras.comprar(solicitud)

    # Verificación
    assert resultado.aceptada is False
    assert resultado.motivo == MotivoRechazo.ERROR_PAGO
    assert resultado.compra is None
    assert resultado.url_redireccion is None
    assert len(pago.solicitudes) == 1
    assert correo.intentos == []
