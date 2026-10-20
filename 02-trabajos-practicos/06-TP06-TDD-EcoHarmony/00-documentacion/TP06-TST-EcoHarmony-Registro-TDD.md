# Registro de TDD

Evidencia real de cada ciclo Red → Green → Refactor (regla 8). Copiar la salida
observada de pytest; no reconstruir ejecuciones.

Entorno de las ejecuciones históricas de C01 y C02: Python 3.13.7, pytest 9.1.1,
Ruff 0.17.1, Windows 11. El entorno de C03 y C04 se detalla en su sección.

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

## C02 — Compra válida con tarjeta

**Red.** Dos tests en `tests/test_c02_compra_valida_tarjeta.py`. Fallan porque
`comprar` trata la tarjeta igual que el efectivo: no solicita el pago y confirma la
compra.

```text
$ python -m pytest -k c02 -v --tb=short
tests\test_c02_compra_valida_tarjeta.py:21: in test_c02_acepta_y_abre_la_pasarela_de_pago
    assert len(pago.solicitudes) == 1
E   assert 0 == 1
tests\test_c02_compra_valida_tarjeta.py:32: in test_c02_mantiene_compra_y_pago_pendientes_hasta_la_aprobacion
    assert resultado.compra.estado_compra == EstadoCompra.PENDIENTE
E   AssertionError: assert <EstadoCompra.CONFIRMADA: 'CONFIRMADA'> == <EstadoCompra.PENDIENTE: 'PENDIENTE'>
FAILED tests/test_c02_compra_valida_tarjeta.py::test_c02_acepta_y_abre_la_pasarela_de_pago
FAILED tests/test_c02_compra_valida_tarjeta.py::test_c02_mantiene_compra_y_pago_pendientes_hasta_la_aprobacion
======================= 2 failed, 4 deselected in 0.33s =======================
```

**Green.** Con tarjeta, `comprar` deja compra `PENDIENTE` y pago
`PENDIENTE_PASARELA`, guarda la compra, solicita `iniciar_pago_tarjeta` y devuelve
la URL en `url_redireccion`. No envía correo (A02).

```text
$ python -m pytest -v
tests/test_c01_compra_valida_efectivo.py::test_c01_confirma_compra_en_efectivo_con_pago_pendiente_en_boleteria PASSED [ 16%]
tests/test_c01_compra_valida_efectivo.py::test_c01_conserva_cantidad_y_fecha_validadas PASSED [ 33%]
tests/test_c01_compra_valida_efectivo.py::test_c01_registra_la_compra_confirmada PASSED [ 50%]
tests/test_c01_compra_valida_efectivo.py::test_c01_solicita_un_correo_al_visitante PASSED [ 66%]
tests/test_c02_compra_valida_tarjeta.py::test_c02_acepta_y_abre_la_pasarela_de_pago PASSED [ 83%]
tests/test_c02_compra_valida_tarjeta.py::test_c02_mantiene_compra_y_pago_pendientes_hasta_la_aprobacion PASSED [100%]
============================== 6 passed in 0.27s ==============================
```

**Refactor.** La versión Green creaba la compra como confirmada y luego cambiaba
sus estados para tarjeta. Se extrajeron `_crear_compra`, `_confirmar_en_efectivo`
e `_iniciar_pago_con_tarjeta`, de modo que cada flujo crea la compra con su estado
inicial. Verificación posterior:

```text
$ python -m pytest -q
6 passed in 0.13s
$ python -m ruff check .
All checks passed!
$ python -m ruff format --check .
44 files already formatted
```

## Interfaz web (sin ciclo TDD)

Se agregaron `ecoharmony/entrada.py` y `ecoharmony/web/` (Flask, HTML, CSS y JS).
No tienen tests automáticos: se verificaron manualmente con el cliente de pruebas de
Flask y una captura del navegador (regla 12: distinguir la verificación manual de
los tests automáticos). Resultados observados:

- `POST /api/compras` con la solicitud base en efectivo: `CONFIRMADA`,
  `PENDIENTE_BOLETERIA`, `ENVIADO`, total `20000`.
- Con tarjeta y pase VIP: `PENDIENTE`, `PENDIENTE_PASARELA`, URL
  `/pasarela-simulada/<id>`, total `30000`; la página de la pasarela responde 200.
- Fecha `31/02/2030`: respuesta 400 con mensaje de formato inválido (genérico hasta
  construir C27).
- Tipo de pase vacío: respuesta 500 con el mensaje de caso pendiente (hasta
  construir C17).

`entrada.py` deja que los formatos inválidos lancen el `ValueError` propio de la
conversión; C25–C28 deben escribir sus tests y reemplazarlo por motivos estables.

Suite tras agregar la interfaz:

```text
$ python -m pytest -q
6 passed
$ python -m ruff check .
All checks passed!
```

## Ajuste de la estructura

Se quitaron los archivos de especificación `test_c03`–`test_c28`: en ese momento,
la suite contenía solo C01 y C02. Cada responsable crea el archivo de su caso al
comenzarlo.

## C03 y C04 — Entorno de verificación (19/10/2026)

Estas ejecuciones usan Windows, Python 3.13.5, pytest 9.1.1 y Ruff 0.17.1.
Se creó `.venv/` y se instalaron las versiones de `requirements.txt` sin cambiar
las dependencias del proyecto. Los comandos se ejecutaron desde
`01-implementacion/` con `.venv\Scripts\python.exe`.

**Confirmado:** el entregable (página 7) requiere aceptar D0 abierto para C03 y
D0 + 1 abierto para C04, manteniendo válida la solicitud restante. Se añadieron
dos variantes por caso, una por forma de pago, con las fixtures compartidas.

## C03 — Fecha actual con parque abierto

**Primera ejecución (Green directo).** Se creó `tests/test_c03_fecha_actual.py`
para comprobar aceptación de D0 y conservación de la fecha en el resultado y en
el repositorio. Ambas variantes pasaron sin modificar código de producción:

```text
$ .venv\Scripts\python.exe -m pytest -k c03 -v --tb=short
tests/test_c03_fecha_actual.py::test_c03_acepta_fecha_actual_con_parque_abierto[FormaPago.EFECTIVO] PASSED [ 50%]
tests/test_c03_fecha_actual.py::test_c03_acepta_fecha_actual_con_parque_abierto[FormaPago.TARJETA] PASSED [100%]
======================= 2 passed, 8 deselected in 0.09s =======================
```

**Código y refactorización.** `ServicioCompras.comprar` ya acepta esta solicitud;
`_crear_compra` conserva `fecha_visita` y ambos flujos registran la compra.
No hizo falta cambiar esos métodos ni refactorizar. Se registra el comportamiento
existente, conforme a la regla 8; no hubo una fase Red.

## C04 — Fecha futura con parque abierto

**Primera ejecución (Green directo).** Se creó `tests/test_c04_fecha_futura.py`
para comprobar aceptación de D0 + 1 abierto y conservación de la fecha en el
resultado y en el repositorio. Ambas variantes pasaron sin modificar producción:

```text
$ .venv\Scripts\python.exe -m pytest -k c04 -v --tb=short
tests/test_c04_fecha_futura.py::test_c04_acepta_fecha_futura_con_parque_abierto[FormaPago.EFECTIVO] PASSED [ 50%]
tests/test_c04_fecha_futura.py::test_c04_acepta_fecha_futura_con_parque_abierto[FormaPago.TARJETA] PASSED [100%]
======================= 2 passed, 8 deselected in 0.05s =======================
```

**Código y refactorización.** El flujo compartido de C01 y C02 ya conserva la
fecha futura solicitada. Se reutilizó sin cambios. Se registra Green directo,
sin provocar un fallo artificial ni introducir otra implementación.

## Verificación de C01–C04

```text
$ .venv\Scripts\python.exe -m pytest -q
..........                                                               [100%]
10 passed in 0.03s
$ .venv\Scripts\python.exe -m ruff check .
All checks passed!
$ .venv\Scripts\python.exe -m ruff format --check .
20 files already formatted
```

Los casos C03 y C04 comprueban aceptación bajo las precondiciones de apertura
preparadas. Los rechazos por fecha pasada, parque cerrado y fecha ausente siguen
pendientes en C10, C11 y C15. No se ejecutaron pruebas de navegador: el cambio
agrega pruebas de la lógica compartida y documentación.

## C07 y C08 — Máximo de entradas y pase VIP (19/10/2026)

Ejecuciones observadas en Windows con Python 3.12.2 y pytest 9.1.1. Las pruebas
se escribieron en `tests/test_c07_diez_entradas.py` y
`tests/test_c08_pase_vip.py`.

**Primera ejecución (Green directo).** C07 comprueba la aceptación de diez
entradas, la conservación de cantidad y edades y el total regular de $100.000.
C08 comprueba la aceptación y conservación del pase VIP y el total de $30.000
para las dos entradas de la solicitud base. Ambas pruebas pasaron sin cambios en
código de producción:

```text
$ python -m pytest -k 'c07 or c08' -v --tb=short
tests/test_c07_diez_entradas.py::test_c07_acepta_el_maximo_de_diez_entradas PASSED [ 50%]
tests/test_c08_pase_vip.py::test_c08_acepta_y_conserva_el_pase_vip PASSED [100%]
====================== 2 passed, 12 deselected in 0.14s =======================
```

**Verificación.** La suite completa pasó con 14 tests. Ruff y formato pasan
para ambos archivos nuevos. La ejecución global de Ruff todavía señala dos
problemas preexistentes de salto de línea final en los tests C05 y C06; no se
modificaron porque son ajenos a estos casos.

```text
$ python -m pytest -q
14 passed in 0.07s
$ python -m ruff check tests/test_c07_diez_entradas.py tests/test_c08_pase_vip.py
All checks passed!
$ python -m ruff format --check tests/test_c07_diez_entradas.py tests/test_c08_pase_vip.py
2 files already formatted
```
