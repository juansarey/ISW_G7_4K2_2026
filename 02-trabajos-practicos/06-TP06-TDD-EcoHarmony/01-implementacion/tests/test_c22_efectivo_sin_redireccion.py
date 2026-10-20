"""C22 — Compra en efectivo sin invocar ni redirigir a la pasarela."""

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


@pytest.mark.parametrize(
    "falla_al_iniciar",
    [False, True],
    ids=["pago_disponible", "pago_configurado_para_fallar"],
)
def test_c22_confirma_efectivo_sin_invocar_pasarela_ni_redirigir(
    servicio_compras: ServicioCompras,
    solicitud_base: SolicitudCompra,
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
    falla_al_iniciar: bool,
) -> None:
    # Preparación
    pago.falla_al_iniciar = falla_al_iniciar

    # Ejecución
    resultado = servicio_compras.comprar(solicitud_base)

    # Verificación
    assert resultado.aceptada is True
    assert resultado.motivo is None
    assert resultado.compra is not None
    compra = resultado.compra

    assert compra.forma_pago == FormaPago.EFECTIVO
    assert compra.estado_compra == EstadoCompra.CONFIRMADA
    assert compra.estado_pago == EstadoPago.PENDIENTE_BOLETERIA
    assert compra.estado_correo == EstadoCorreo.ENVIADO
    assert resultado.url_redireccion is None
    assert pago.solicitudes == []

    registrada = repositorio.obtener(compra.id_compra)
    assert registrada is not None
    assert registrada.id_compra == compra.id_compra
    assert registrada.estado_compra == EstadoCompra.CONFIRMADA
    assert registrada.estado_pago == EstadoPago.PENDIENTE_BOLETERIA
    assert len(repositorio.compras) == 1

    assert len(correo.intentos) == 1
    assert correo.intentos[0].id_compra == compra.id_compra
