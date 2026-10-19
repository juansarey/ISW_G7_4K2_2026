"""Fixtures comunes (regla 10). Todas tienen alcance de función: cada test recibe
reloj, calendario, dobles y servicio nuevos, sin estado compartido.

Datos de referencia (entregable, página 6):
- Usuario visitante01, registrado, correo visitante@example.com.
- D0 = 12/06/2030. Calendario: D0 - 1, D0 y D0 + 1 abiertos; D0 + 2 cerrado.
- Solicitud base: D0 + 1, dos entradas, edades 24 y 36, pase regular, efectivo.
"""

from collections.abc import Callable
from dataclasses import replace
from datetime import date, timedelta

import pytest

from ecoharmony.modelos import FormaPago, SolicitudCompra, TipoPase, Usuario
from ecoharmony.servicio_compras import ServicioCompras
from tests.dobles import (
    CalendarioDoble,
    CorreoDoble,
    PagoDoble,
    RelojDoble,
    RepositorioDoble,
)

FECHA_ACTUAL_D0 = date(2030, 6, 12)
UN_DIA = timedelta(days=1)


@pytest.fixture
def fecha_actual() -> date:
    return FECHA_ACTUAL_D0


@pytest.fixture
def reloj(fecha_actual: date) -> RelojDoble:
    return RelojDoble(fecha_actual)


@pytest.fixture
def calendario(fecha_actual: date) -> CalendarioDoble:
    # D0 + 2 queda fuera del conjunto: es el cierre que permite comprobar CA05.
    return CalendarioDoble({fecha_actual - UN_DIA, fecha_actual, fecha_actual + UN_DIA})


@pytest.fixture
def pago() -> PagoDoble:
    return PagoDoble()


@pytest.fixture
def correo() -> CorreoDoble:
    return CorreoDoble()


@pytest.fixture
def repositorio() -> RepositorioDoble:
    return RepositorioDoble()


@pytest.fixture
def servicio_compras(
    reloj: RelojDoble,
    calendario: CalendarioDoble,
    pago: PagoDoble,
    correo: CorreoDoble,
    repositorio: RepositorioDoble,
) -> ServicioCompras:
    return ServicioCompras(reloj, calendario, pago, correo, repositorio)


@pytest.fixture
def usuario_registrado() -> Usuario:
    return Usuario(
        nombre_usuario="visitante01",
        correo="visitante@example.com",
        registrado=True,
    )


@pytest.fixture
def solicitud_base(fecha_actual: date, usuario_registrado: Usuario) -> SolicitudCompra:
    return SolicitudCompra(
        usuario=usuario_registrado,
        fecha_visita=fecha_actual + UN_DIA,
        cantidad_entradas=2,
        edades=(24, 36),
        tipo_pase=TipoPase.REGULAR,
        forma_pago=FormaPago.EFECTIVO,
    )


@pytest.fixture
def crear_solicitud(
    solicitud_base: SolicitudCompra,
) -> Callable[..., SolicitudCompra]:
    """Devuelve la solicitud base cambiando solo los campos indicados.

    Ejemplo: ``crear_solicitud(forma_pago=None)`` para C13. Al cambiar la cantidad,
    indicar también edades coherentes (regla 10).
    """

    def _crear(**cambios: object) -> SolicitudCompra:
        return replace(solicitud_base, **cambios)

    return _crear
