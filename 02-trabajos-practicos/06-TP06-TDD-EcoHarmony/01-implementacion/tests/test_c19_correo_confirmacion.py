"""C19 — Correo al confirmar, con envío exitoso o fallo inicial."""

from collections.abc import Callable

import pytest

from ecoharmony.modelos import (
    EstadoCompra,
    EstadoCorreo,
    EstadoPago,
    FormaPago,
    SolicitudCompra,
)
from ecoharmony.servicio_compras import ServicioCompras
from tests.dobles import CorreoDoble, PagoDoble, RepositorioDoble


@pytest.mark.parametrize("forma_pago", [FormaPago.EFECTIVO, FormaPago.TARJETA])
@pytest.mark.parametrize("falla_correo", [False, True])
def test_c19_solicita_correo_y_conserva_compra_y_pago(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    correo: CorreoDoble,
    pago: PagoDoble,
    repositorio: RepositorioDoble,
    forma_pago: FormaPago,
    falla_correo: bool,
) -> None:
    correo.falla_al_enviar = falla_correo
    solicitud = crear_solicitud(forma_pago=forma_pago)

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is True
    assert resultado.compra is not None
    id_compra = resultado.compra.id_compra

    if forma_pago == FormaPago.TARJETA:
        assert resultado.compra.estado_compra == EstadoCompra.PENDIENTE
        assert resultado.compra.estado_pago == EstadoPago.PENDIENTE_PASARELA
        assert resultado.compra.estado_correo == EstadoCorreo.NO_SOLICITADO
        assert correo.intentos == []

        resultado = servicio_compras.registrar_resultado_pago(id_compra, aprobado=True)

    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    compra = resultado.compra

    pago_esperado = (
        EstadoPago.APROBADO
        if forma_pago == FormaPago.TARJETA
        else EstadoPago.PENDIENTE_BOLETERIA
    )
    correo_esperado = (
        EstadoCorreo.CORREO_PENDIENTE if falla_correo else EstadoCorreo.ENVIADO
    )

    assert compra.id_compra == id_compra
    assert compra.estado_compra == EstadoCompra.CONFIRMADA
    assert compra.estado_pago == pago_esperado
    assert compra.estado_correo == correo_esperado
    assert len(correo.intentos) == 1
    assert correo.intentos[0].id_compra == id_compra
    assert correo.intentos[0].usuario.correo == solicitud.usuario.correo

    registrada = repositorio.obtener(id_compra)
    assert registrada is not None
    assert registrada.estado_compra == EstadoCompra.CONFIRMADA
    assert registrada.estado_pago == pago_esperado
    assert registrada.estado_correo == correo_esperado
    assert len(repositorio.compras) == 1

    if forma_pago == FormaPago.TARJETA:
        assert pago.solicitudes == [(id_compra, compra.total)]

        repetido = servicio_compras.registrar_resultado_pago(id_compra, aprobado=True)
        assert repetido.compra is not None
        assert repetido.compra.id_compra == id_compra
        assert repetido.compra.estado_correo == correo_esperado
        assert len(correo.intentos) == 1
        assert pago.solicitudes == [(id_compra, compra.total)]
        assert len(repositorio.compras) == 1


def test_pago_rechazado_no_confirma_compra_ni_solicita_correo(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    correo: CorreoDoble,
) -> None:
    solicitud = crear_solicitud(forma_pago=FormaPago.TARJETA)
    inicio = servicio_compras.comprar(solicitud)
    assert inicio.compra is not None

    resultado = servicio_compras.registrar_resultado_pago(
        inicio.compra.id_compra, aprobado=False
    )

    assert resultado.aceptada is True
    assert resultado.compra is not None
    assert resultado.compra.estado_compra == EstadoCompra.CANCELADA
    assert resultado.compra.estado_pago == EstadoPago.RECHAZADO
    assert resultado.compra.estado_correo == EstadoCorreo.NO_SOLICITADO
    assert correo.intentos == []


def test_registrar_resultado_pago_rechaza_compra_inexistente(
    servicio_compras: ServicioCompras,
) -> None:
    with pytest.raises(ValueError, match="Compra inexistente"):
        servicio_compras.registrar_resultado_pago("inexistente", aprobado=True)


def test_registrar_resultado_pago_rechaza_compra_en_efectivo(
    servicio_compras: ServicioCompras,
    solicitud_base: SolicitudCompra,
) -> None:
    resultado = servicio_compras.comprar(solicitud_base)
    assert resultado.compra is not None

    with pytest.raises(ValueError, match="pago con tarjeta"):
        servicio_compras.registrar_resultado_pago(
            resultado.compra.id_compra, aprobado=True
        )


def test_registrar_resultado_pago_rechaza_transicion_incompatible(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
) -> None:
    solicitud = crear_solicitud(forma_pago=FormaPago.TARJETA)
    inicio = servicio_compras.comprar(solicitud)
    assert inicio.compra is not None
    servicio_compras.registrar_resultado_pago(inicio.compra.id_compra, aprobado=False)

    with pytest.raises(ValueError, match="estado es incompatible"):
        servicio_compras.registrar_resultado_pago(
            inicio.compra.id_compra, aprobado=True
        )
