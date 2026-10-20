"""C14 (CA09) — Solo un visitante registrado puede comprar entradas.

El visitante conserva el nombre y el correo de referencia, pero figura como no
registrado; fecha, cantidad, edades y pase son los de la solicitud base. Se
prueba con efectivo y con tarjeta porque la condición de registro tiene que
cortar la compra antes de que cualquiera de los dos caminos de pago empiece.
"""

from collections.abc import Callable
from dataclasses import replace

import pytest

from ecoharmony.modelos import FormaPago, MotivoRechazo, SolicitudCompra, Usuario
from ecoharmony.servicio_compras import ServicioCompras
from tests.dobles import CorreoDoble, PagoDoble, RepositorioDoble


@pytest.mark.parametrize("forma_pago", [FormaPago.EFECTIVO, FormaPago.TARJETA])
def test_c14_rechaza_compra_de_visitante_sin_registro(
    servicio_compras: ServicioCompras,
    crear_solicitud: Callable[..., SolicitudCompra],
    usuario_registrado: Usuario,
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
    forma_pago: FormaPago,
) -> None:
    # Se cambia solo la marca de registro para que sea la única causa posible.
    visitante_sin_registro = replace(usuario_registrado, registrado=False)
    solicitud = crear_solicitud(
        usuario=visitante_sin_registro,
        forma_pago=forma_pago,
    )

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is False
    assert resultado.motivo == MotivoRechazo.USUARIO_NO_REGISTRADO
    assert resultado.compra is None
    assert resultado.url_redireccion is None
    assert repositorio.compras == {}
    assert pago.solicitudes == []
    assert correo.intentos == []
