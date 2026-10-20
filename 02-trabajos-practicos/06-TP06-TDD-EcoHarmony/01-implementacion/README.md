# TP6 — EcoHarmony Park: Comprar entradas (TDD)

Implementación en Python de la User Story **«Comprar entradas»** con desarrollo
conducido por pruebas (pytest) y una interfaz web de demostración (Flask).

> Antes de modificar código, leer `../00-documentacion/TP06-DES-EcoHarmony-Reglas-Codificacion.md`,
> `../00-documentacion/TP06-DES-EcoHarmony-Contrato-Implementacion.md` y `AGENTS.md` (también si se usa una IA).

## Estado

| Elemento | Estado |
|---|---|
| Contrato, modelos, dependencias y servicios simulados | Listo |
| Fixtures (`tests/conftest.py`) y dobles (`tests/dobles.py`) | Listo |
| C01 — compra válida en efectivo | Terminado (4 tests) |
| C02 — compra válida con tarjeta | Terminado (2 tests) |
| C03 — fecha actual con parque abierto | Terminado (2 variantes: efectivo y tarjeta) |
| C04 — fecha futura con parque abierto | Terminado (2 variantes: efectivo y tarjeta) |
| C05–C06 | Pendientes |
| C07 — diez entradas | Test agregado; Green directo |
| C09 — pase regular | Test agregado; Green directo |
| C10 — fecha pasada | Terminado (rechazo con FECHA_PASADA) |
| C11 — parque cerrado | Terminado (2 variantes: efectivo y tarjeta) |
| C12–C28 | Pendientes (especificados en el entregable, páginas 7 a 9) |
| Interfaz web | Lista; verificada manualmente |

Como las validaciones (C12–C18, C25–C28) todavía no se construyeron, la interfaz
**acepta** por ahora solicitudes que deberían rechazarse (por ejemplo, once
entradas), y una solicitud con datos ausentes devuelve un error del servidor. Los
escenarios de demostración pasarán a mostrar el rechazo correcto a medida que se
completen esos casos. C11 ya rechaza una fecha cerrada mediante el calendario
inyectado. Ver `../00-documentacion/TP06-DES-EcoHarmony-Asignacion-Casos.md`.

C03 y C04 verifican la aceptación de D0 y D0 + 1 con el parque abierto y conservan
la fecha en el resultado y en el registro. Sus cuatro variantes pasaron desde la
primera ejecución con la lógica existente; la evidencia está en
`../00-documentacion/TP06-TST-EcoHarmony-Registro-TDD.md`. La suite actual contiene
18 pruebas. C07 y C08 también pasan desde la primera ejecución, sin cambios en
producción; C11 verifica el rechazo del parque cerrado. C12 en adelante siguen
pendientes salvo los casos indicados como terminados en esta tabla.

## Instalación

Versiones verificadas: Python 3.13.7, Flask 3.1.3, pytest 9.1.1 y Ruff 0.17.1, en
Windows 11. Se requiere Python 3.11 o superior.

```text
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux / macOS
python -m pip install -r requirements.txt
```

## Comandos

Ejecutar desde `01-implementacion/` (donde está `pyproject.toml`):

```text
python -m pytest -q             # suite completa
python -m pytest -k c01 -v      # tests de un caso
python -m ruff check .          # linter
python -m ruff format --check . # formato
python -m ecoharmony.web        # interfaz web en http://127.0.0.1:5000
```

## Estructura

```text
ecoharmony/
  modelos.py            # SolicitudCompra, Compra, ResultadoCompra, estados y motivos
  tarifas.py            # MAXIMO_ENTRADAS y tarifas A03
  dependencias.py       # Protocolos Reloj, Calendario, ServicioPago, ServicioCorreo...
  servicio_compras.py   # ServicioCompras.comprar: lógica bajo prueba
  entrada.py            # Límite de entrada: JSON de la interfaz -> SolicitudCompra
  simulados.py          # Reloj fijo, calendario A01, pago y correo simulados
  web/                  # Flask (app.py, mensajes.py) y estáticos HTML/CSS/JS
tests/
  conftest.py           # Fixtures con los datos de referencia del entregable
  dobles.py             # Dobles de pago, correo, reloj, calendario y repositorio
  test_c01_*.py         # C01 (un archivo por caso)
  test_c02_*.py         # C02
  test_c03_fecha_actual.py # C03: fecha actual, efectivo y tarjeta
  test_c04_fecha_futura.py # C04: fecha futura, efectivo y tarjeta
  test_c07_diez_entradas.py # C07: límite máximo aceptado
  test_c08_pase_vip.py      # C08: pase VIP y tarifa
  test_c11_parque_cerrado.py # C11: rechazo del calendario cerrado
```

La documentación (contrato, asignación, trazabilidad, registro TDD y acuerdos)
está en `../00-documentacion/`.

## Cómo tomar un caso

1. Anotarse como responsable en `../00-documentacion/TP06-DES-EcoHarmony-Asignacion-Casos.md`.
2. Leer la especificación del caso en el entregable y crear
   `tests/test_cXX_<comportamiento>.py`.
3. **Red:** escribir el test usando las fixtures (`servicio_compras`,
   `crear_solicitud`, `pago`, `correo`, `repositorio`...), ejecutarlo y copiar la
   salida en `../00-documentacion/TP06-TST-EcoHarmony-Registro-TDD.md`.
4. **Green:** implementar lo mínimo en `ecoharmony/` y ejecutar toda la suite.
5. **Refactor:** mejorar el diseño, volver a ejecutar la suite y Ruff.
6. Actualizar la trazabilidad y la asignación en `../00-documentacion/`, y hacer un commit
   por caso: `<Legajo>: TP6 CXX: <comportamiento>`.

Ejemplo de test de rechazo:

```python
from ecoharmony.modelos import MotivoRechazo


def test_c12_rechaza_mas_de_diez_entradas(servicio_compras, crear_solicitud):
    solicitud = crear_solicitud(cantidad_entradas=11, edades=(30,) * 11)

    resultado = servicio_compras.comprar(solicitud)

    assert resultado.aceptada is False
    assert resultado.motivo == MotivoRechazo.CANTIDAD_EXCEDE_MAXIMO
```

## Simulación

El reloj está fijado en 12/06/2030 y el calendario sigue A01. El pago con tarjeta
abre una pasarela local (`/pasarela-simulada/<id>`) y el correo se guarda en una
bandeja en memoria. **No hay integración real con Mercado Pago ni con un servidor
de correo.** Los datos se pierden al reiniciar el servidor.
