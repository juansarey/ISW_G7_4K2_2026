# Registro de TDD

Evidencia real de cada ciclo Red → Green → Refactor (regla 8). Copiar la salida
observada de pytest; no reconstruir ejecuciones.

Entorno de las ejecuciones registradas: Python 3.13.7, pytest 9.1.1, Ruff 0.17.1,
Windows 11.

## Estructura inicial

Se crearon el contrato (`modelos.py`, `dependencias.py`, `tarifas.py`), los servicios
simulados, las fixtures y dobles de `tests/` y `ServicioCompras` sin comportamiento:
`comprar` lanza `NotImplementedError`. Los archivos `test_c03`–`test_c28` contienen
solo la especificación del caso.

`tarifas.calcular_total` se definió como parte del contrato A03. Al escribir C05–C09
y C20 es posible que sus tests de total pasen en la primera ejecución: registrar
ese resultado como comportamiento existente, sin provocar un fallo artificial.

## C01 — Compra válida en efectivo

**Red.** Se escribieron cuatro tests en `tests/test_c01_compra_valida_efectivo.py`
(confirmación con pago pendiente en boletería, cantidad y fecha conservadas,
registro de la compra confirmada y un correo al visitante). Fallan porque
`comprar` todavía no tiene comportamiento:

```text
$ python -m pytest -k c01 -v --tb=line
E   NotImplementedError: Pendiente: construir mediante TDD a partir de C01.
FAILED tests/test_c01_compra_valida_efectivo.py::test_c01_confirma_compra_en_efectivo_con_pago_pendiente_en_boleteria
FAILED tests/test_c01_compra_valida_efectivo.py::test_c01_conserva_cantidad_y_fecha_validadas
FAILED tests/test_c01_compra_valida_efectivo.py::test_c01_registra_la_compra_confirmada
FAILED tests/test_c01_compra_valida_efectivo.py::test_c01_solicita_un_correo_al_visitante
============================== 4 failed in 0.26s ==============================
```

**Green.** `comprar` crea la `Compra` con los valores de la solicitud, estado
`CONFIRMADA` y pago `PENDIENTE_BOLETERIA`, la guarda en el repositorio y solicita
el correo (A02). Todavía no valida la solicitud ni distingue la forma de pago.

```text
$ python -m pytest -v
tests/test_c01_compra_valida_efectivo.py::test_c01_confirma_compra_en_efectivo_con_pago_pendiente_en_boleteria PASSED [ 25%]
tests/test_c01_compra_valida_efectivo.py::test_c01_conserva_cantidad_y_fecha_validadas PASSED [ 50%]
tests/test_c01_compra_valida_efectivo.py::test_c01_registra_la_compra_confirmada PASSED [ 75%]
tests/test_c01_compra_valida_efectivo.py::test_c01_solicita_un_correo_al_visitante PASSED [100%]
============================== 4 passed in 0.19s ==============================
$ python -m ruff check .
All checks passed!
$ python -m ruff format --check .
43 files already formatted
```

**Refactor.** No se identificaron duplicaciones; sin cambios.
