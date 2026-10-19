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
