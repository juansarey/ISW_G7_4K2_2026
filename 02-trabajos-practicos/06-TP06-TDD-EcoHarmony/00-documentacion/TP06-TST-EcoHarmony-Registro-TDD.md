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

## C12 — Más de diez entradas (19/10/2026)

Responsable: Martina Lenta (95294).

**Red.** Se agregó `tests/test_c12_maximo_entradas.py` con efectivo y tarjeta.
La solicitud contiene `MAXIMO_ENTRADAS + 1` entradas y la misma cantidad de
edades válidas para aislar la regla de máximo. Ambas variantes se ejecutaron antes
de cambiar producción y fallaron porque la compra fue aceptada.

```text
$ python -m pytest -k c12 -v --tb=short
platform win32 -- Python 3.10.4, pytest-9.1.1
collected 20 items / 18 deselected / 2 selected
test_c12_rechaza_mas_de_diez_entradas[FormaPago.EFECTIVO] FAILED
test_c12_rechaza_mas_de_diez_entradas[FormaPago.TARJETA] FAILED
2 failed, 18 deselected in 0.18s
```

**Green.** `ServicioCompras.comprar` rechaza cantidades mayores que
`MAXIMO_ENTRADAS`; diez entradas continúan permitidas. La condición se evalúa antes
de registrar la compra o iniciar pago/correo.

```text
$ python -m pytest -k c12 -v --tb=short
2 passed, 18 deselected in 0.05s
$ python -m pytest -q
20 passed in 0.07s
```

**Refactor.** Se reutilizó `MAXIMO_ENTRADAS`; no hizo falta agregar lógica auxiliar.

**Verificación final de C11 y C12.** En Windows con Python 3.10.4 y pytest 9.1.1,
la suite completa pasó (`20 passed`). Ruff 0.17.1 pasa para `servicio_compras.py`
y los tests C11/C12. Los controles globales informan dos problemas preexistentes,
ambos `W292` por falta de salto de línea final en `test_c05_una_entrada.py` y
`test_c06_nueve_entradas.py`; `ruff format --check .` señala únicamente esos mismos
dos archivos. No se modificaron porque C05/C06 están fuera del alcance.

## C13 — Forma de pago ausente (19/10/2026)

Responsable: Tomas Zengaro (403344).

**Entorno.** Entorno virtual propio en `01-implementacion/.venv` (excluido por
`.gitignore`), con las dependencias de `requirements.txt`: Python 3.14.6,
pytest 9.1.1 y Ruff 0.17.1, en Windows 11. En las salidas copiadas se omiten las
líneas de encabezado que solo muestran la ruta local del equipo.

**Base previa.** Antes de escribir el test, la suite existente pasó completa:

```text
$ .venv\Scripts\python -m pytest -q
20 passed in 0.09s
```

**Red.** Se creó `tests/test_c13_forma_pago_ausente.py` con un único test,
`test_c13_rechaza_compra_sin_forma_de_pago_seleccionada`. La solicitud se arma con
`crear_solicitud(forma_pago=None)`, de modo que el resto de los datos de la
solicitud base sigue siendo válido y la omisión de la forma de pago es la única
causa posible de rechazo. No se parametrizó por efectivo y tarjeta: justamente es
el dato que falta. Además del motivo, el test exige que no haya compra registrada,
redirección, pedido de pago ni correo.

Al ejecutarlo sin tocar producción falló como se esperaba. El servicio no
distinguía la ausencia: todo lo que no era tarjeta seguía el camino de efectivo,
así que la compra quedó confirmada con `forma_pago=None`, pago pendiente en
boletería y correo enviado.

```text
$ .venv\Scripts\python -m pytest -k c13 -v --tb=short
collecting ... collected 21 items / 20 deselected / 1 selected

tests/test_c13_forma_pago_ausente.py::test_c13_rechaza_compra_sin_forma_de_pago_seleccionada FAILED [100%]

================================== FAILURES ===================================
___________ test_c13_rechaza_compra_sin_forma_de_pago_seleccionada ____________
tests\test_c13_forma_pago_ausente.py:27: in test_c13_rechaza_compra_sin_forma_de_pago_seleccionada
    assert resultado.aceptada is False
E   AssertionError: assert True is False
E    +  where True = ResultadoCompra(aceptada=True, compra=Compra(id_compra='03faa7822a80463ab03bda72d3edd2b2', usuario=Usuario(nombre_usuario='visitante01', correo='visitante@example.com', registrado=True), fecha_visita=datetime.date(2030, 6, 13), cantidad_entradas=2, edades=(24, 36), tipo_pase=<TipoPase.REGULAR: 'REGULAR'>, forma_pago=None, total=Decimal('20000'), estado_compra=<EstadoCompra.CONFIRMADA: 'CONFIRMADA'>, estado_pago=<EstadoPago.PENDIENTE_BOLETERIA: 'PENDIENTE_BOLETERIA'>, estado_correo=<EstadoCorreo.ENVIADO: 'ENVIADO'>), motivo=None, url_redireccion=None).aceptada
=========================== short test summary info ===========================
FAILED tests/test_c13_forma_pago_ausente.py::test_c13_rechaza_compra_sin_forma_de_pago_seleccionada
====================== 1 failed, 20 deselected in 0.18s =======================
```

**Green.** En `ServicioCompras.comprar` se agregó una guarda que devuelve
`MotivoRechazo.FORMA_PAGO_AUSENTE` cuando `forma_pago` es `None`. Se ubicó después
de la validación de cantidad y antes de elegir entre tarjeta y efectivo, como pide
el orden del contrato (§4), por lo que ningún camino de pago llega a ejecutarse.

```text
$ .venv\Scripts\python -m pytest -k c13 -v --tb=short
collecting ... collected 21 items / 20 deselected / 1 selected

tests/test_c13_forma_pago_ausente.py::test_c13_rechaza_compra_sin_forma_de_pago_seleccionada PASSED [100%]

====================== 1 passed, 20 deselected in 0.11s =======================
$ .venv\Scripts\python -m pytest -q
.....................                                                    [100%]
21 passed in 0.09s
```

**Refactor.** Se evaluó y no se aplicó. La guarda nueva tiene la misma forma que
las de fecha y cantidad y deja explícita una decisión que antes estaba implícita
(el `else` del efectivo absorbía cualquier valor que no fuera tarjeta). Con cuatro
guardas cortas `comprar` todavía se lee de corrido; extraerlas ahora sería mover
código sin una ganancia clara. Se vuelve a evaluar al incorporar C14.

**Verificación de Ruff.** `ruff check` y `ruff format --check` sobre
`ecoharmony/servicio_compras.py` y `tests/test_c13_forma_pago_ausente.py`
informaron `All checks passed!` y `2 files already formatted`. Sobre todo el
proyecto (`.`) persisten solo los dos problemas preexistentes ya registrados en C12
(`W292` en `test_c05_una_entrada.py` y `test_c06_nueve_entradas.py`, que también
son los dos archivos que `ruff format --check .` reformatearía). No se tocaron por
estar fuera del alcance de este caso.

## C14 — Usuario no registrado (19/10/2026)

Responsable: Tomas Zengaro (403344). Mismo entorno que C13 (Python 3.14.6,
pytest 9.1.1, Ruff 0.17.1, Windows 11); también se omiten las líneas de
encabezado con la ruta local.

**Base previa.** Con C13 ya integrado, la suite pasó completa antes de empezar:

```text
$ .venv\Scripts\python -m pytest -q
21 passed in 0.09s
```

**Red.** Se creó `tests/test_c14_usuario_no_registrado.py` con el test
`test_c14_rechaza_compra_de_visitante_sin_registro`, parametrizado con efectivo y
tarjeta. El visitante se obtiene con `replace(usuario_registrado, registrado=False)`:
conserva el nombre `visitante01` y el correo de referencia, así que la marca de
registro es lo único que difiere de la solicitud base. No se agregó una fixture a
`conftest.py` porque solo este caso usa ese visitante. Las dos variantes se
ejecutaron antes de cambiar producción y fallaron porque el servicio nunca miraba
el registro: en efectivo la compra quedó confirmada y con correo enviado, y con
tarjeta quedó registrada como pendiente y se abrió la pasarela.

```text
$ .venv\Scripts\python -m pytest -k c14 -v --tb=short
collecting ... collected 23 items / 21 deselected / 2 selected

tests/test_c14_usuario_no_registrado.py::test_c14_rechaza_compra_de_visitante_sin_registro[FormaPago.EFECTIVO] FAILED [ 50%]
tests/test_c14_usuario_no_registrado.py::test_c14_rechaza_compra_de_visitante_sin_registro[FormaPago.TARJETA] FAILED [100%]

================================== FAILURES ===================================
____ test_c14_rechaza_compra_de_visitante_sin_registro[FormaPago.EFECTIVO] ____
tests\test_c14_usuario_no_registrado.py:38: in test_c14_rechaza_compra_de_visitante_sin_registro
    assert resultado.aceptada is False
E   AssertionError: assert True is False
E    +  where True = ResultadoCompra(aceptada=True, compra=Compra(id_compra='e54ae90e08b54005b5d015b5a9713f9f', usuario=Usuario(nombre_usuario='visitante01', correo='visitante@example.com', registrado=False), fecha_visita=datetime.date(2030, 6, 13), cantidad_entradas=2, edades=(24, 36), tipo_pase=<TipoPase.REGULAR: 'REGULAR'>, forma_pago=<FormaPago.EFECTIVO: 'EFECTIVO'>, total=Decimal('20000'), estado_compra=<EstadoCompra.CONFIRMADA: 'CONFIRMADA'>, estado_pago=<EstadoPago.PENDIENTE_BOLETERIA: 'PENDIENTE_BOLETERIA'>, estado_correo=<EstadoCorreo.ENVIADO: 'ENVIADO'>), motivo=None, url_redireccion=None).aceptada
____ test_c14_rechaza_compra_de_visitante_sin_registro[FormaPago.TARJETA] _____
tests\test_c14_usuario_no_registrado.py:38: in test_c14_rechaza_compra_de_visitante_sin_registro
    assert resultado.aceptada is False
E   AssertionError: assert True is False
E    +  where True = ResultadoCompra(aceptada=True, compra=Compra(id_compra='a55e048ec907409da7e0d4dd72507e13', usuario=Usuario(nombre_usuario='visitante01', correo='visitante@example.com', registrado=False), fecha_visita=datetime.date(2030, 6, 13), cantidad_entradas=2, edades=(24, 36), tipo_pase=<TipoPase.REGULAR: 'REGULAR'>, forma_pago=<FormaPago.TARJETA: 'TARJETA'>, total=Decimal('20000'), estado_compra=<EstadoCompra.PENDIENTE: 'PENDIENTE'>, estado_pago=<EstadoPago.PENDIENTE_PASARELA: 'PENDIENTE_PASARELA'>, estado_correo=<EstadoCorreo.NO_SOLICITADO: 'NO_SOLICITADO'>), motivo=None, url_redireccion='https://pasarela.doble/pago/a55e048ec907409da7e0d4dd72507e13').aceptada
=========================== short test summary info ===========================
FAILED tests/test_c14_usuario_no_registrado.py::test_c14_rechaza_compra_de_visitante_sin_registro[FormaPago.EFECTIVO]
FAILED tests/test_c14_usuario_no_registrado.py::test_c14_rechaza_compra_de_visitante_sin_registro[FormaPago.TARJETA]
====================== 2 failed, 21 deselected in 0.16s =======================
```

**Green.** Se agregó al comienzo de `ServicioCompras.comprar` una guarda que
devuelve `MotivoRechazo.USUARIO_NO_REGISTRADO` si `solicitud.usuario.registrado`
es falso. Va antes de la fecha, la cantidad y la forma de pago porque el usuario
es el primer punto del orden del contrato (§4), y por eso tampoco llegan a
consultarse el reloj ni el calendario.

```text
$ .venv\Scripts\python -m pytest -k c14 -v --tb=short
collecting ... collected 23 items / 21 deselected / 2 selected

tests/test_c14_usuario_no_registrado.py::test_c14_rechaza_compra_de_visitante_sin_registro[FormaPago.EFECTIVO] PASSED [ 50%]
tests/test_c14_usuario_no_registrado.py::test_c14_rechaza_compra_de_visitante_sin_registro[FormaPago.TARJETA] PASSED [100%]

====================== 2 passed, 21 deselected in 0.10s =======================
$ .venv\Scripts\python -m pytest -q
.......................                                                  [100%]
23 passed in 0.11s
```

**Refactor.** Esta vez sí se aplicó. Con la guarda de C14, `comprar` acumulaba
cinco bloques que solo cambiaban el motivo y repetían la construcción de
`ResultadoCompra(aceptada=False, ...)`, mezclando la validación con la coordinación
del pago. Se extrajo el método privado `_motivo_de_rechazo(solicitud)`, que
devuelve el primer `MotivoRechazo` en el orden del contrato o `None`, y `comprar`
quedó en dos pasos: si hay motivo arma el rechazo en un único lugar; si no, despacha
a tarjeta o efectivo. Las condiciones y su orden son los mismos; solo se nombró
`fecha` para no repetir `solicitud.fecha_visita`. Las validaciones pendientes
(C15–C18) pueden sumarse ahí como una línea más sin tocar la parte de pago. No
cambia la interfaz pública ni el contrato. Tras el cambio se repitió la suite y,
por separado, los casos de rechazo ya existentes:

```text
$ .venv\Scripts\python -m pytest -q
.......................                                                  [100%]
23 passed in 0.10s
$ .venv\Scripts\python -m pytest -k "c10 or c11 or c12 or c13 or c14" -q
........                                                                 [100%]
8 passed, 15 deselected in 0.08s
```

**Verificación de Ruff.** Sobre `ecoharmony/servicio_compras.py`,
`tests/test_c13_forma_pago_ausente.py` y `tests/test_c14_usuario_no_registrado.py`:
`All checks passed!` y `3 files already formatted`. En el proyecto completo
`ruff check .` sigue mostrando únicamente los dos `W292` preexistentes de
`test_c05_una_entrada.py` y `test_c06_nueve_entradas.py`, y `ruff format --check .`
informa `2 files would be reformatted, 28 files already formatted` por esos mismos
archivos, que quedan fuera del alcance de C14.

## C15 — Fecha ausente (20/10/2026)

Responsable: Nicolas Steffolani (94196).

**Entorno.** Entorno virtual en `01-implementacion/.venv` con Python 3.12.3, pytest 9.1.1 y Ruff 0.17.1 en Linux. En las salidas copiadas se omiten las líneas de encabezado con rutas locales.

**Base previa.** Antes de escribir el test de C15, con C14 ya integrado, la suite pasó completa:

```text
$ python -m pytest -q
.......................                                                  [100%]
23 passed in 0.03s
```

**Red.** Se creó `tests/test_c15_fecha_ausente.py` con el test `test_c15_rechaza_compra_sin_fecha_de_visita`, parametrizado con `FormaPago.EFECTIVO` y `FormaPago.TARJETA`. La solicitud se genera con `crear_solicitud(fecha_visita=None, forma_pago=forma_pago)`, de modo que el resto de los datos (usuario registrado, cantidad de entradas con sus edades y tipo de pase) son válidos y la ausencia de la fecha es la única causa del rechazo. El test comprueba que el resultado no sea aceptado, que el motivo sea `FECHA_AUSENTE`, que no haya compra registrada ni URL de redirección, y que no se hayan registrado compras ni realizado pedidos de pago o intentos de envío de correo.

Al ejecutarlo antes de modificar producción falló en ambas variantes porque el servicio no validaba la ausencia de la fecha y procedía a confirmar la compra en efectivo o abrir la pasarela de pago con tarjeta:

```text
$ python -m pytest -k c15 -v --tb=short
collecting ... collected 25 items / 23 deselected / 2 selected

tests/test_c15_fecha_ausente.py::test_c15_rechaza_compra_sin_fecha_de_visita[FormaPago.EFECTIVO] FAILED [ 50%]
tests/test_c15_fecha_ausente.py::test_c15_rechaza_compra_sin_fecha_de_visita[FormaPago.TARJETA] FAILED [100%]

=================================== FAILURES ===================================
_______ test_c15_rechaza_compra_sin_fecha_de_visita[FormaPago.EFECTIVO] ________
tests/test_c15_fecha_ausente.py:34: in test_c15_rechaza_compra_sin_fecha_de_visita
    assert resultado.aceptada is False
E   AssertionError: assert True is False
E    +  where True = ResultadoCompra(aceptada=True, compra=Compra(id_compra='dcd6c88ec6ad434fbada23fe446606d9', usuario=Usuario(nombre_usuario='visitante01', correo='visitante@example.com', registrado=True), fecha_visita=None, cantidad_entradas=2, edades=(24, 36), tipo_pase=<TipoPase.REGULAR: 'REGULAR'>, forma_pago=<FormaPago.EFECTIVO: 'EFECTIVO'>, total=Decimal('20000'), estado_compra=<EstadoCompra.CONFIRMADA: 'CONFIRMADA'>, estado_pago=<EstadoPago.PENDIENTE_BOLETERIA: 'PENDIENTE_BOLETERIA'>, estado_correo=<EstadoCorreo.ENVIADO: 'ENVIADO'>), motivo=None, url_redireccion=None).aceptada
________ test_c15_rechaza_compra_sin_fecha_de_visita[FormaPago.TARJETA] ________
tests/test_c15_fecha_ausente.py:34: in test_c15_rechaza_compra_sin_fecha_de_visita
    assert resultado.aceptada is False
E   AssertionError: assert True is False
E    +  where True = ResultadoCompra(aceptada=True, compra=Compra(id_compra='3f87a518a49c473ca662cac3f09f4768', usuario=Usuario(nombre_usuario='visitante01', correo='visitante@example.com', registrado=True), fecha_visita=None, cantidad_entradas=2, edades=(24, 36), tipo_pase=<TipoPase.REGULAR: 'REGULAR'>, forma_pago=<FormaPago.TARJETA: 'TARJETA'>, total=Decimal('20000'), estado_compra=<EstadoCompra.PENDIENTE: 'PENDIENTE'>, estado_pago=<EstadoPago.PENDIENTE_PASARELA: 'PENDIENTE_PASARELA'>, estado_correo=<EstadoCorreo.NO_SOLICITADO: 'NO_SOLICITADO'>), motivo=None, url_redireccion='https://pasarela.doble/pago/3f87a518a49c473ca662cac3f09f4768').aceptada
=========================== short test summary info ============================
FAILED tests/test_c15_fecha_ausente.py::test_c15_rechaza_compra_sin_fecha_de_visita[FormaPago.EFECTIVO]
FAILED tests/test_c15_fecha_ausente.py::test_c15_rechaza_compra_sin_fecha_de_visita[FormaPago.TARJETA]
======================= 2 failed, 23 deselected in 0.04s =======================
```

**Green.** En `ServicioCompras._motivo_de_rechazo`, dentro del bloque de validaciones de fecha, se agregó la guarda que comprueba si `fecha is None` y devuelve `MotivoRechazo.FECHA_AUSENTE`. Se ubica inmediatamente después de la validación del usuario y antes de evaluar fecha pasada o parque cerrado, cumpliendo con el orden establecido en el contrato (§4).

```text
$ python -m pytest -k c15 -v --tb=short
collecting ... collected 25 items / 23 deselected / 2 selected

tests/test_c15_fecha_ausente.py::test_c15_rechaza_compra_sin_fecha_de_visita[FormaPago.EFECTIVO] PASSED [ 50%]
tests/test_c15_fecha_ausente.py::test_c15_rechaza_compra_sin_fecha_de_visita[FormaPago.TARJETA] PASSED [100%]

======================= 2 passed, 23 deselected in 0.02s =======================
$ python -m pytest -q
.........................                                                [100%]
25 passed in 0.04s
```

**Refactor.** Al haber garantizado que `fecha is None` corta inmediatamente y retorna `FECHA_AUSENTE`, las dos condiciones subsiguientes (`FECHA_PASADA` y `PARQUE_CERRADO`) ya no necesitan verificar defensivamente `fecha is not None and`. Se simplificaron ambas expresiones en `_motivo_de_rechazo`, mejorando la legibilidad sin alterar el comportamiento. Tras el cambio, se verificó nuevamente la suite completa:

```text
$ python -m pytest -q
.........................                                                [100%]
25 passed in 0.04s
```

**Verificación de Ruff.** Sobre `ecoharmony/servicio_compras.py` y `tests/test_c15_fecha_ausente.py`: `All checks passed!` y `2 files already formatted`.

## C16 — Edades incompletas (20/10/2026)

Responsable: Nicolas Steffolani (94196). Mismo entorno que C15 (Python 3.12.3, pytest 9.1.1, Ruff 0.17.1 en Linux).

**Base previa.** Antes de comenzar C16, con C15 integrado, la suite completa pasó:

```text
$ python -m pytest -q
.........................                                                [100%]
25 passed in 0.04s
```

**Red.** Se creó `tests/test_c16_edades_incompletas.py` con `test_c16_rechaza_compra_con_edades_incompletas`, parametrizado con `FormaPago.EFECTIVO` y `FormaPago.TARJETA`. Siguiendo la especificación del entregable (CA01: dos entradas y edad informada para un solo visitante), se construye la solicitud mediante `crear_solicitud(cantidad_entradas=2, edades=(24,), forma_pago=forma_pago)`, dejando todos los demás campos válidos. Se comprueba que el resultado devuelva `aceptada=False`, el motivo `EDADES_INCOMPLETAS`, y la ausencia de efectos secundarios (sin compra guardada, sin iniciar pago y sin enviar correo).

Al ejecutar los tests antes de modificar la lógica de producción, fallaron en ambas opciones de pago pues el servicio aceptaba la compra con una sola edad para dos entradas:

```text
$ python -m pytest -k c16 -v --tb=short
collecting ... collected 27 items / 25 deselected / 2 selected

tests/test_c16_edades_incompletas.py::test_c16_rechaza_compra_con_edades_incompletas[FormaPago.EFECTIVO] FAILED [ 50%]
tests/test_c16_edades_incompletas.py::test_c16_rechaza_compra_con_edades_incompletas[FormaPago.TARJETA] FAILED [100%]

=================================== FAILURES ===================================
______ test_c16_rechaza_compra_con_edades_incompletas[FormaPago.EFECTIVO] ______
tests/test_c16_edades_incompletas.py:37: in test_c16_rechaza_compra_con_edades_incompletas
    assert resultado.aceptada is False
E   AssertionError: assert True is False
E    +  where True = ResultadoCompra(aceptada=True, compra=Compra(id_compra='f3142059ed5944f38e4e23f6768db1bf', usuario=Usuario(nombre_usuario='visitante01', correo='visitante@example.com', registrado=True), fecha_visita=datetime.date(2030, 6, 13), cantidad_entradas=2, edades=(24,), tipo_pase=<TipoPase.REGULAR: 'REGULAR'>, forma_pago=<FormaPago.EFECTIVO: 'EFECTIVO'>, total=Decimal('20000'), estado_compra=<EstadoCompra.CONFIRMADA: 'CONFIRMADA'>, estado_pago=<EstadoPago.PENDIENTE_BOLETERIA: 'PENDIENTE_BOLETERIA'>, estado_correo=<EstadoCorreo.ENVIADO: 'ENVIADO'>), motivo=None, url_redireccion=None).aceptada
______ test_c16_rechaza_compra_con_edades_incompletas[FormaPago.TARJETA] _______
tests/test_c16_edades_incompletas.py:37: in test_c16_rechaza_compra_con_edades_incompletas
    assert resultado.aceptada is False
E   AssertionError: assert True is False
E    +  where True = ResultadoCompra(aceptada=True, compra=Compra(id_compra='f6de631e0fb845ac9646a7b4a7c89a1e', usuario=Usuario(nombre_usuario='visitante01', correo='visitante@example.com', registrado=True), fecha_visita=datetime.date(2030, 6, 13), cantidad_entradas=2, edades=(24,), tipo_pase=<TipoPase.REGULAR: 'REGULAR'>, forma_pago=<FormaPago.TARJETA: 'TARJETA'>, total=Decimal('20000'), estado_compra=<EstadoCompra.PENDIENTE: 'PENDIENTE'>, estado_pago=<EstadoPago.PENDIENTE_PASARELA: 'PENDIENTE_PASARELA'>, estado_correo=<EstadoCorreo.NO_SOLICITADO: 'NO_SOLICITADO'>), motivo=None, url_redireccion='https://pasarela.doble/pago/f6de631e0fb845ac9646a7b4a7c89a1e').aceptada
=========================== short test summary info ============================
FAILED tests/test_c16_edades_incompletas.py::test_c16_rechaza_compra_con_edades_incompletas[FormaPago.EFECTIVO]
FAILED tests/test_c16_edades_incompletas.py::test_c16_rechaza_compra_con_edades_incompletas[FormaPago.TARJETA]
======================= 2 failed, 25 deselected in 0.04s =======================
```

**Green.** En `ServicioCompras._motivo_de_rechazo`, a continuación de la validación de la cantidad de entradas y antes de las validaciones de tipo de pase y forma de pago (respetando el orden del contrato §4), se agregó la comprobación de que la cantidad de edades informadas no sea menor a la cantidad de entradas solicitadas:

```python
if cantidad is not None and len(solicitud.edades) < cantidad:
    return MotivoRechazo.EDADES_INCOMPLETAS
```

Se ejecutaron los tests de C16 y la suite completa:

```text
$ python -m pytest -k c16 -v --tb=short
collecting ... collected 27 items / 25 deselected / 2 selected

tests/test_c16_edades_incompletas.py::test_c16_rechaza_compra_con_edades_incompletas[FormaPago.EFECTIVO] PASSED [ 50%]
tests/test_c16_edades_incompletas.py::test_c16_rechaza_compra_con_edades_incompletas[FormaPago.TARJETA] PASSED [100%]

======================= 2 passed, 25 deselected in 0.02s =======================
$ python -m pytest -q
...........................                                              [100%]
27 passed in 0.04s
```

**Refactor.** Se analizó el método `_motivo_de_rechazo`. Las condiciones de validación quedaron agrupadas de forma ordenada y concisa respetando el contrato §4 (usuario -> fecha -> cantidad -> edades -> forma de pago). No se requirió extraer métodos adicionales ya que cada verificación es directa de una o dos líneas. Se ejecutaron la suite completa y la totalidad de los casos de rechazo existentes:

```text
$ python -m pytest -q
...........................                                              [100%]
27 passed in 0.04s
$ python -m pytest -k "c10 or c11 or c12 or c13 or c14 or c15 or c16" -q
............                                                             [100%]
12 passed, 15 deselected in 0.03s
```

**Verificación de Ruff.** Sobre `ecoharmony/servicio_compras.py`, `tests/test_c15_fecha_ausente.py` y `tests/test_c16_edades_incompletas.py`: `All checks passed!` y `3 files already formatted`. En el proyecto completo `ruff check .` continúa reportando únicamente los dos avisos `W292` preexistentes en `test_c05_una_entrada.py` y `test_c06_nueve_entradas.py` fuera del alcance de estos casos.

## C17 — Tipo de pase ausente (20/10/2026)

Entorno: Mac, Python 3.14.5, pytest 9.1.1, Ruff 0.17.1.
Responsable: Santiago Adaime (91316).

**Red.** Se creó `tests/test_c17_tipo_pase_ausente.py`, con una variante para
efectivo y otra para tarjeta (CA01). Cada una deja el tipo de pase en `None` y
verifica el rechazo con `TIPO_PASE_AUSENTE` y la ausencia de compra registrada,
solicitud de pago y correo. Fallan porque `ServicioCompras` todavía no valida el
tipo de pase:

```text
$ python -m pytest -k c17 -v --tb=short
========================================================================================== test session starts ==========================================================================================
platform darwin -- Python 3.14.5, pytest-9.1.1, pluggy-1.7.0 -- /Users/santiagoadaime/Documents/Facultad/Cuarto/ICW/ISW_G7_4K2_2026/02-trabajos-practicos/06-TP06-TDD-EcoHarmony/01-implementacion/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/santiagoadaime/Documents/Facultad/Cuarto/ICW/ISW_G7_4K2_2026/02-trabajos-practicos/06-TP06-TDD-EcoHarmony/01-implementacion
configfile: pyproject.toml
testpaths: tests
collected 29 items / 27 deselected / 2 selected                                                                                                                                                         

tests/test_c17_tipo_pase_ausente.py::test_c17_rechaza_compra_sin_tipo_de_pase[FormaPago.EFECTIVO] FAILED                                                                                          [ 50%]
tests/test_c17_tipo_pase_ausente.py::test_c17_rechaza_compra_sin_tipo_de_pase[FormaPago.TARJETA] FAILED                                                                                           [100%]

=============================================================================================== FAILURES ================================================================================================
_____________________________________________________________________ test_c17_rechaza_compra_sin_tipo_de_pase[FormaPago.EFECTIVO] ______________________________________________________________________
tests/test_c17_tipo_pase_ausente.py:29: in test_c17_rechaza_compra_sin_tipo_de_pase
    resultado = servicio_compras.comprar(solicitud)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ecoharmony/servicio_compras.py:46: in comprar
    return self._confirmar_en_efectivo(solicitud)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ecoharmony/servicio_compras.py:75: in _confirmar_en_efectivo
    compra = self._crear_compra(
ecoharmony/servicio_compras.py:110: in _crear_compra
    total=calcular_total(solicitud.cantidad_entradas, solicitud.tipo_pase),
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ecoharmony/tarifas.py:17: in calcular_total
    return TARIFAS_POR_PASE[tipo_pase] * cantidad_entradas
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   KeyError: None
______________________________________________________________________ test_c17_rechaza_compra_sin_tipo_de_pase[FormaPago.TARJETA] ______________________________________________________________________
tests/test_c17_tipo_pase_ausente.py:29: in test_c17_rechaza_compra_sin_tipo_de_pase
    resultado = servicio_compras.comprar(solicitud)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ecoharmony/servicio_compras.py:45: in comprar
    return self._iniciar_pago_con_tarjeta(solicitud)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ecoharmony/servicio_compras.py:85: in _iniciar_pago_con_tarjeta
    compra = self._crear_compra(
ecoharmony/servicio_compras.py:110: in _crear_compra
    total=calcular_total(solicitud.cantidad_entradas, solicitud.tipo_pase),
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ecoharmony/tarifas.py:17: in calcular_total
    return TARIFAS_POR_PASE[tipo_pase] * cantidad_entradas
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   KeyError: None
======================================================================================== short test summary info ========================================================================================
FAILED tests/test_c17_tipo_pase_ausente.py::test_c17_rechaza_compra_sin_tipo_de_pase[FormaPago.EFECTIVO] - KeyError: None
FAILED tests/test_c17_tipo_pase_ausente.py::test_c17_rechaza_compra_sin_tipo_de_pase[FormaPago.TARJETA] - KeyError: None
=================================================================================== 2 failed, 27 deselected in 0.10s ====================================================================================
```

**Green.** En `ServicioCompras._motivo_de_rechazo` se agregó, después del chequeo
de edades y antes del de forma de pago (orden del contrato §4), el rechazo con
`MotivoRechazo.TIPO_PASE_AUSENTE` cuando `solicitud.tipo_pase is None`.

```text
$ python -m pytest -q
.............................                                                                                                                                                                     [100%]
29 passed in 0.04s

```

**Refactor.**  Sin cambios



## C18 — Cantidad de entradas ausente (20/10/2026)

Entorno: Mac, Python 3.14.5, pytest 9.1.1, Ruff 0.17.1. 
Responsable: Santiago Adaime (91316).

**Red.** Se creó `tests/test_c18_cantidad_ausente.py`, con una variante para
efectivo y otra para tarjeta (CA01). Cada una deja la cantidad en `None`, conserva
las edades de la solicitud base y verifica el rechazo con `CANTIDAD_AUSENTE` y la
ausencia de compra registrada, solicitud de pago y correo. Fallan porque
`ServicioCompras` todavía no valida la cantidad:

```text
$ python -m pytest -k c18 -v --tb=short
========================================================================================== test session starts ==========================================================================================
platform darwin -- Python 3.14.5, pytest-9.1.1, pluggy-1.7.0 -- /Users/santiagoadaime/Documents/Facultad/Cuarto/ICW/ISW_G7_4K2_2026/02-trabajos-practicos/06-TP06-TDD-EcoHarmony/01-implementacion/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/santiagoadaime/Documents/Facultad/Cuarto/ICW/ISW_G7_4K2_2026/02-trabajos-practicos/06-TP06-TDD-EcoHarmony/01-implementacion
configfile: pyproject.toml
testpaths: tests
collected 31 items / 29 deselected / 2 selected                                                                                                                                                         

tests/test_c18_cantidad_ausente.py::test_c18_rechaza_compra_sin_cantidad_de_entradas[FormaPago.EFECTIVO] FAILED                                                                                   [ 50%]
tests/test_c18_cantidad_ausente.py::test_c18_rechaza_compra_sin_cantidad_de_entradas[FormaPago.TARJETA] FAILED                                                                                    [100%]

=============================================================================================== FAILURES ================================================================================================
_________________________________________________________________ test_c18_rechaza_compra_sin_cantidad_de_entradas[FormaPago.EFECTIVO] __________________________________________________________________
tests/test_c18_cantidad_ausente.py:29: in test_c18_rechaza_compra_sin_cantidad_de_entradas
    resultado = servicio_compras.comprar(solicitud)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ecoharmony/servicio_compras.py:46: in comprar
    return self._confirmar_en_efectivo(solicitud)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ecoharmony/servicio_compras.py:77: in _confirmar_en_efectivo
    compra = self._crear_compra(
ecoharmony/servicio_compras.py:112: in _crear_compra
    total=calcular_total(solicitud.cantidad_entradas, solicitud.tipo_pase),
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ecoharmony/tarifas.py:17: in calcular_total
    return TARIFAS_POR_PASE[tipo_pase] * cantidad_entradas
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   TypeError: unsupported operand type(s) for *: 'decimal.Decimal' and 'NoneType'
__________________________________________________________________ test_c18_rechaza_compra_sin_cantidad_de_entradas[FormaPago.TARJETA] __________________________________________________________________
tests/test_c18_cantidad_ausente.py:29: in test_c18_rechaza_compra_sin_cantidad_de_entradas
    resultado = servicio_compras.comprar(solicitud)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ecoharmony/servicio_compras.py:45: in comprar
    return self._iniciar_pago_con_tarjeta(solicitud)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ecoharmony/servicio_compras.py:87: in _iniciar_pago_con_tarjeta
    compra = self._crear_compra(
ecoharmony/servicio_compras.py:112: in _crear_compra
    total=calcular_total(solicitud.cantidad_entradas, solicitud.tipo_pase),
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ecoharmony/tarifas.py:17: in calcular_total
    return TARIFAS_POR_PASE[tipo_pase] * cantidad_entradas
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   TypeError: unsupported operand type(s) for *: 'decimal.Decimal' and 'NoneType'
======================================================================================== short test summary info ========================================================================================
FAILED tests/test_c18_cantidad_ausente.py::test_c18_rechaza_compra_sin_cantidad_de_entradas[FormaPago.EFECTIVO] - TypeError: unsupported operand type(s) for *: 'decimal.Decimal' and 'NoneType'
FAILED tests/test_c18_cantidad_ausente.py::test_c18_rechaza_compra_sin_cantidad_de_entradas[FormaPago.TARJETA] - TypeError: unsupported operand type(s) for *: 'decimal.Decimal' and 'NoneType'
=================================================================================== 2 failed, 29 deselected in 0.10s ====================================================================================
```

**Green.** En `ServicioCompras._motivo_de_rechazo` se agregó, al inicio del bloque
de cantidad y antes del chequeo del máximo, el rechazo con
`MotivoRechazo.CANTIDAD_AUSENTE` cuando `cantidad is None`.

```text
$ python -m pytest -q
...............................                                                                                                                                                                   [100%]
31 passed in 0.04s 
```

**Refactor.** Con `None` descartado antes, se quitó la condición
`cantidad is not None and` de los chequeos de `CANTIDAD_EXCEDE_MAXIMO` (C12) y
`EDADES_INCOMPLETAS` (C16), que había quedado como protección provisoria. El
comportamiento no cambia. Verificación posterior:

```text
$ python -m pytest -q
...............................                                          [100%]
31 passed in 0.04s
$ python -m ruff check .
W292 [*] No newline at end of file
  --> tests/test_c05_una_entrada.py:18:51
  (...)
W292 [*] No newline at end of file
  --> tests/test_c06_nueve_entradas.py:20:45
  (...)
Found 2 errors.
[*] 2 fixable with `--fix`.
$ python -m ruff format --check .
unformatted: File would be reformatted
  --> tests/test_c05_una_entrada.py:18:51
  (...)
unformatted: File would be reformatted
  --> tests/test_c06_nueve_entradas.py:20:45
  (...)
2 files would be reformatted, 32 files already formatted
```

Los dos avisos de Ruff (W292 y formato) son preexistentes: están en los tests de
C05 y C06, ajenos a C17 y C18, y no se modificaron en este caso. Los archivos de
este caso se verificaron por separado:

```text
$ python -m ruff check ecoharmony/servicio_compras.py tests/test_c17_tipo_pase_ausente.py tests/test_c18_cantidad_ausente.py

All checks passed!

$ python -m ruff format --check ecoharmony/servicio_compras.py tests/test_c17_tipo_pase_ausente.py tests/test_c18_cantidad_ausente.py

All checks passed!
```

## C19 — Correo de confirmación (20/10/2026)

Responsable: Lucas Schoninger (97927).

**Base previa.** Antes del test de C19, la suite completa pasó:

```text
$ python -m pytest -q
31 passed in 0.18s
```

**Red.** Se agregó `tests/test_c19_correo_confirmacion.py`. Sus cuatro variantes
cubren efectivo/tarjeta con envío exitoso o fallo inicial. También comprueban que
una notificación aprobada repetida no duplica correo ni pago, que una notificación
rechazada no confirma ni envía correo, y las precondiciones y transiciones
incompatibles de la operación nueva. Antes de modificar producción se ejecutó:

```text
$ python -m pytest -k c19 -v --tb=short
collected 39 items / 31 deselected / 8 selected
7 failed, 1 passed, 31 deselected in 0.43s
```

Las variantes que necesitan resultado de tarjeta fallaron porque aún no existía
`registrar_resultado_pago`; el envío fallido en efectivo propagó
`ErrorServicioCorreo`. Las otras guardas fallaron por la operación inexistente.
La variante de efectivo con correo exitoso ya pasaba.

**Green.** Se incorporó el manejo específico de `ErrorServicioCorreo` y
`registrar_resultado_pago`. La operación valida compra, forma y estado; aplica
los estados de A02, persiste la transición antes del correo y trata notificaciones
repetidas como idempotentes. No se implementó el reintento de C30.

```text
$ python -m pytest -k c19 -v --tb=short
8 passed, 31 deselected in 0.39s
$ python -m pytest -q
39 passed in 0.25s
```

La verificación global de Ruff continúa encontrando los dos avisos `W292` y los
dos archivos no formateados preexistentes de C05 y C06. El servicio y el test C19
se formatearon y verificaron por separado; esos archivos ajenos al caso no se
modificaron. C29 y C30 permanecen pendientes.

## C20 — Resumen de la compra (20/10/2026)

Responsable: Lucas Schoninger (97927).

**Primera ejecución (Green directo).** Se agregó
`tests/test_c20_resumen_compra.py` con cuatro variantes: pase regular/VIP por
efectivo/tarjeta. Se verifica compra confirmada de dos entradas para D0 + 1,
conservación de fecha, pase y forma de pago, total `Decimal("20000")` para regular
y `Decimal("30000")` para VIP, y estado de pago acorde con A02. Las cuatro pruebas
pasaron sin modificar código de producción:

```text
$ python -m pytest -k c20 -v --tb=short
collected 43 items / 39 deselected / 4 selected
4 passed, 39 deselected in 0.20s
```

Se reutilizaron `calcular_total` y `registrar_resultado_pago`, ya implementados.
El resumen se verifica en `ResultadoCompra.compra`; esto no prueba una
presentación visual en el navegador. C20 no añade comportamiento para C29 ni C30.

**Verificación final conjunta de C19 y C20.**

```text
$ python -m pytest -q
43 passed in 0.29s
$ python -m ruff check ecoharmony/servicio_compras.py tests/test_c19_correo_confirmacion.py tests/test_c20_resumen_compra.py
All checks passed!
$ python -m ruff format --check ecoharmony/servicio_compras.py tests/test_c19_correo_confirmacion.py tests/test_c20_resumen_compra.py
3 files already formatted
```

Los controles globales de Ruff siguen señalando únicamente los problemas
preexistentes `W292` y de formato en los tests de C05 y C06, que no se modificaron.

## C21 — Inicio del pago con tarjeta (20/10/2026)

Entorno: Windows, Python 3.12.3, pytest 9.1.1 y Ruff 0.17.1.
Responsable: Juan Pablo Sacco Rey (89319).

**Comportamiento existente — Green directo.** Se creó
`tests/test_c21_inicio_pago_tarjeta.py` y se comprobó el inicio exitoso del pago
con tarjeta. La prueba verifica una única solicitud a la pasarela con el
identificador y total correctos, la URL esperada, la compra registrada con estados
`PENDIENTE` / `PENDIENTE_PASARELA` y la ausencia de correo antes de aprobar el
pago. El comportamiento ya estaba implementado por C02.

```text
$ python -m pytest tests/test_c21_inicio_pago_tarjeta.py::test_c21_inicia_pago_una_vez_y_conserva_compra_pendiente_sin_correo -v --tb=short -p no:cacheprovider
collected 1 item

tests/test_c21_inicio_pago_tarjeta.py::test_c21_inicia_pago_una_vez_y_conserva_compra_pendiente_sin_correo PASSED [100%]

============================== 1 passed in 0.06s ==============================
```

**Red.** Se agregó
`test_c21_rechaza_con_error_pago_si_falla_el_inicio_de_pasarela`, configurando
`pago.falla_al_iniciar = True`. La prueba espera un resultado rechazado con
`ERROR_PAGO`, sin compra ni URL, con un único intento de iniciar el pago y sin
correo. El caso no agrega reglas sobre la persistencia interna del intento.

```text
$ python -m pytest tests/test_c21_inicio_pago_tarjeta.py::test_c21_rechaza_con_error_pago_si_falla_el_inicio_de_pasarela -v --tb=short -p no:cacheprovider
collected 1 item

tests/test_c21_inicio_pago_tarjeta.py::test_c21_rechaza_con_error_pago_si_falla_el_inicio_de_pasarela FAILED [100%]

tests/dobles.py:43: in iniciar_pago_tarjeta
    raise ErrorServicioPago("Fallo configurado en el doble de pago.")
E   ecoharmony.dependencias.ErrorServicioPago: Fallo configurado en el doble de pago.

============================== 1 failed in 0.11s ==============================
```

La prueba falló porque `_iniciar_pago_con_tarjeta` propagaba
`ErrorServicioPago` y no devolvía el resultado definido por A04 y el contrato.

**Green.** Se importó `ErrorServicioPago` y se capturó específicamente alrededor
de `iniciar_pago_tarjeta`. Ante ese fallo se devuelve
`ResultadoCompra(aceptada=False, motivo=MotivoRechazo.ERROR_PAGO)`. Se conservó
el orden de persistencia existente y no se modificó la lógica de C02, C19 o C20.

```text
$ python -m pytest tests/test_c21_inicio_pago_tarjeta.py -v --tb=short -p no:cacheprovider
collected 2 items

tests/test_c21_inicio_pago_tarjeta.py::test_c21_inicia_pago_una_vez_y_conserva_compra_pendiente_sin_correo PASSED [ 50%]
tests/test_c21_inicio_pago_tarjeta.py::test_c21_rechaza_con_error_pago_si_falla_el_inicio_de_pasarela PASSED [100%]

============================== 2 passed in 0.04s ==============================

$ python -m pytest -q -p no:cacheprovider
.............................................                            [100%]
45 passed in 0.23s
```

**Refactor.** Se revisó `_iniciar_pago_con_tarjeta` y no se identificaron
duplicaciones, nombres confusos ni una extracción que mejorara el diseño. No se
realizaron cambios. El manejo de `ErrorServicioPago` tiene una responsabilidad
distinta del manejo de correo y deja intacto `registrar_resultado_pago`.

**Verificación de Ruff.** Se instaló Ruff 0.17.1 en el entorno virtual local
excluido del repositorio. Los archivos de C21 pasan ambos controles:

```text
$ .\.venv\Scripts\python.exe -m ruff check --no-cache ecoharmony/servicio_compras.py tests/test_c21_inicio_pago_tarjeta.py
All checks passed!

$ .\.venv\Scripts\python.exe -m ruff format --check --no-cache ecoharmony/servicio_compras.py tests/test_c21_inicio_pago_tarjeta.py
2 files already formatted
```

Los controles globales continúan señalando únicamente los problemas preexistentes
de C05 y C06, que no se modificaron: dos avisos `W292` por falta de salto de línea
final y esos mismos dos archivos como pendientes de formato.
