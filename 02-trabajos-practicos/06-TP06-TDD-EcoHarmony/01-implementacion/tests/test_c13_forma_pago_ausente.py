"""C13 (CA06) — Una solicitud sin forma de pago elegida no puede avanzar.

Se parte de la solicitud base (usuario registrado, D0 + 1 abierto, dos entradas
con sus dos edades y pase regular) y solo se deja sin elegir la forma de pago.
No se parametriza por efectivo o tarjeta porque el dato faltante es justamente
ese: el servicio debe identificar la omisión sin elegir ningún camino de pago.
"""

from collections.abc import Callable

from ecoharmony.modelos import MotivoRechazo, SolicitudCompra
from ecoharmony.servicio_compras import ServicioCompras
from tests.dobles import CorreoDoble, PagoDoble, RepositorioDoble


def test_c13_rechaza_compra_sin_forma_de_pago_seleccionada(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
) -> None:
    solicitud_sin_pago = crear_solicitud(forma_pago=None)

    resultado = servicio_compras.comprar(solicitud_sin_pago)

    assert resultado.aceptada is False
    assert resultado.motivo == MotivoRechazo.FORMA_PAGO_AUSENTE
    assert resultado.compra is None
    assert resultado.url_redireccion is None
    # Sin forma de pago no debe quedar ningún rastro de la operación.
    assert repositorio.compras == {}
    assert pago.solicitudes == []
    assert correo.intentos == []
