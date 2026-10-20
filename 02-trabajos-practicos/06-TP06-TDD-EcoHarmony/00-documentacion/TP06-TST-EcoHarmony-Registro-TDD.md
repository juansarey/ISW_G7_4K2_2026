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
## C09 — pase regular (19/10/2026)

maxit@DESKTOP-KGI56OT MINGW64 /t/Maxi/Maxi Facu/4to año/ISW/Repo/ISW_G7_4K2_2026 (main)      
$ python -m pytest -k c09 -v
=================================== test session starts ====================================
platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\maxit\AppData\Local\Programs\Python\Python313\python.exe
cachedir: .pytest_cache
rootdir: T:\Maxi\Maxi Facu\4to año\ISW\Repo\ISW_G7_4K2_2026
plugins: anyio-4.14.1, hydra-core-1.3.3, mock-3.15.1
collected 16 items / 15 deselected / 1 selected

02-trabajos-practicos/06-TP06-TDD-EcoHarmony/01-implementacion/tests/test_c09_pase_regular.py::test_c09_acepta_y_conserva_el_pase_regular PASSED [100%]

**Primera prueba (Green directo):** Como la tarifa de pase regular ya está resuelta, este test pasa directamente en verde.

## C10 — fecha pasada (19/10/2026)
$ python -m pytest -k c10 -v
=================================== test session starts ====================================
platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\maxit\AppData\Local\Programs\Python\Python313\python.exe
cachedir: .pytest_cache
rootdir: T:\Maxi\Maxi Facu\4to año\ISW\Repo\ISW_G7_4K2_2026
plugins: anyio-4.14.1, hydra-core-1.3.3, mock-3.15.1
collected 16 items / 15 deselected / 1 selected

02-trabajos-practicos/06-TP06-TDD-EcoHarmony/01-implementacion/tests/test_c10_fecha_pasada.py::test_c10_rechaza_fecha_anterior_a_la_actual FAILED [100%]

========================================= FAILURES ========================================= 
_______________________ test_c10_rechaza_fecha_anterior_a_la_actual ________________________ 

servicio_compras = <ecoharmony.servicio_compras.ServicioCompras object at 0x00000267EFC40830>crear_solicitud = <function crear_solicitud.<locals>._crear at 0x00000267EFC3BF60>
fecha_actual = datetime.date(2030, 6, 12)
calendario = <tests.dobles.CalendarioDoble object at 0x00000267EFC402F0>

    def test_c10_rechaza_fecha_anterior_a_la_actual(
        servicio_compras, crear_solicitud, fecha_actual, calendario
    ):
        fecha_pasada = fecha_actual - timedelta(days=1)
        assert calendario.esta_abierto(fecha_pasada) is True

        solicitud = crear_solicitud(fecha_visita=fecha_pasada)

        resultado = servicio_compras.comprar(solicitud)

>       assert resultado.aceptada is False
E       AssertionError: assert True is False
E        +  where True = ResultadoCompra(aceptada=True, compra=Compra(id_compra='b5723616589d4167a155a0381d6419b8', usuario=Usuario(nombre_usuario='visitante01', correo='visitante@example.com', registrado=True), fecha_visita=datetime.date(2030, 6, 11), cantidad_entradas=2, edades=(24, 36), tipo_pase=<TipoPase.REGULAR: 'REGULAR'>, forma_pago=<FormaPago.EFECTIVO: 'EFECTIVO'>, total=Decimal('20000'), estado_compra=<EstadoCompra.CONFIRMADA: 'CONFIRMADA'>, estado_pago=<EstadoPago.PENDIENTE_BOLETERIA: 'PENDIENTE_BOLETERIA'>, estado_correo=<EstadoCorreo.ENVIADO: 'ENVIADO'>), motivo=None, url_redireccion=None).aceptada

02-trabajos-practicos\06-TP06-TDD-EcoHarmony\01-implementacion\tests\test_c10_fecha_pasada.py:22: AssertionError
================================= short test summary info ================================== 
FAILED 02-trabajos-practicos/06-TP06-TDD-EcoHarmony/01-implementacion/tests/test_c10_fecha_pasada.py::test_c10_rechaza_fecha_anterior_a_la_actual - AssertionError: assert True is False  
============================= 1 failed, 15 deselected in 0.28s =============================

**Red**: falla porque el servicio todavía no valida la fecha contra el error. 

**Validación:** se agrega la validación de la fecha en el `servicio_compras.py`:
if (
            solicitud.fecha_visita is not None
            and solicitud.fecha_visita < self._reloj.hoy()
        ):
            return ResultadoCompra(
                aceptada=False, motivo=MotivoRechazo.FECHA_PASADA
            )

**Test:**
maxit@DESKTOP-KGI56OT MINGW64 /t/Maxi/Maxi Facu/4to año/ISW/Repo/ISW_G7_4K2_2026 (main)      
$ python -m pytest -k c10 -v
=================================== test session starts ====================================
platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\maxit\AppData\Local\Programs\Python\Python313\python.exe
cachedir: .pytest_cache
rootdir: T:\Maxi\Maxi Facu\4to año\ISW\Repo\ISW_G7_4K2_2026
plugins: anyio-4.14.1, hydra-core-1.3.3, mock-3.15.1
collected 16 items / 15 deselected / 1 selected

02-trabajos-practicos/06-TP06-TDD-EcoHarmony/01-implementacion/tests/test_c10_fecha_pasada.py::test_c10_rechaza_fecha_anterior_a_la_actual PASSED [100%]

**Green (verde):** El test pasa correctamente.

maxit@DESKTOP-KGI56OT MINGW64 /t/Maxi/Maxi Facu/4to año/ISW/Repo/ISW_G7_4K2_2026 (main)      
$ python -m ruff check .
W292 [*] No newline at end of file
  --> 02-trabajos-practicos\06-TP06-TDD-EcoHarmony\01-implementacion\tests\test_c05_una_entrada.py:18:51
   |
16 |     assert resultado.motivo is None
17 |     assert resultado.compra is not None
18 |     assert resultado.compra.cantidad_entradas == 1
   |                                                   ^
   |
help: Add trailing newline

W292 [*] No newline at end of file
  --> 02-trabajos-practicos\06-TP06-TDD-EcoHarmony\01-implementacion\tests\test_c06_nueve_entradas.py:20:45
   |
18 |     assert resultado.compra is not None
19 |     assert resultado.compra.cantidad_entradas == 9
20 |     assert resultado.compra.edades == edades
   |                                             ^
   |
help: Add trailing newline

Found 2 errors.
[*] 2 fixable with the `--fix` option.

maxit@DESKTOP-KGI56OT MINGW64 /t/Maxi/Maxi Facu/4to año/ISW/Repo/ISW_G7_4K2_2026 (main)      
$ python -m ruff format --check .
Would reformat: 02-trabajos-practicos\06-TP06-TDD-EcoHarmony\01-implementacion\ecoharmony\servicio_compras.py
Would reformat: 02-trabajos-practicos\06-TP06-TDD-EcoHarmony\01-implementacion\tests\test_c05_una_entrada.py
Would reformat: 02-trabajos-practicos\06-TP06-TDD-EcoHarmony\01-implementacion\tests\test_c06_nueve_entradas.py
3 files would be reformatted, 21 files already formatted

**Refactor:** La validación de fecha pasada se ubicó al inicio de `comprar` aplicando el principio de salida temprana y validación previa antes de producir efectos colaterales (DD02). No se detectaron duplicaciones ni se requirió extraer métodos auxiliares. Se aplicó el formato de código con Ruff sobre `servicio_compras.py` para cumplir con el estándar de estilo del proyecto.

## C11 — Parque cerrado (19/10/2026)

Responsable: Martina Lenta (95294).

**Base previa.** Antes de agregar el test de C11, la suite existente pasó: `16 passed
in 0.08s`.

**Red.** Se agregó `tests/test_c11_parque_cerrado.py` con variantes en efectivo y
tarjeta. El calendario compartido considera cerrado D0 + 2. Ambas variantes se
ejecutaron antes de cambiar producción y fallaron porque el servicio aceptó la
compra (`AssertionError: assert True is False`). En efectivo se registró la compra
y se intentó enviar correo; con tarjeta se registró la compra y se inició el pago.

Ejecución de C11 desde `01-implementacion`, antes del cambio de producción:

```text
platform win32 -- Python 3.10.4, pytest-9.1.1
collected 18 items / 16 deselected / 2 selected
test_c11_rechaza_fecha_futura_con_parque_cerrado[FormaPago.EFECTIVO] FAILED
test_c11_rechaza_fecha_futura_con_parque_cerrado[FormaPago.TARJETA] FAILED
2 failed, 16 deselected in 0.15s
```

**Green.** `ServicioCompras.comprar` consulta el calendario inyectado después de
conservar la validación de fecha pasada y rechaza el día cerrado antes de registrar
la compra o iniciar pago/correo.

```text
$ python -m pytest -k c11 -v --tb=short
2 passed, 16 deselected in 0.04s
$ python -m pytest -q
18 passed in 0.07s
```

**Refactor.** No fue necesario extraer lógica: la validación queda en el flujo
común antes de los dos caminos de pago.