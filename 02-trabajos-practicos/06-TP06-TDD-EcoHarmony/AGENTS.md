# Instrucciones para asistentes de IA

Antes de modificar archivos, leer:

1. `TP06-DES-EcoHarmony-Reglas-Codificacion.md`: reglas de codificación y pruebas.
2. `docs/CONTRATO_IMPLEMENTACION.md`: nombres públicos, resultados y motivos.
3. `docs/ASIGNACION_CASOS.md` y `docs/TRAZABILIDAD_PRUEBAS.md`: caso asignado y estado.
4. `docs/Acuerdos_del_grupo.md`: acuerdos A01–A04, DG01–DG04 y decisiones técnicas.
5. Los tests existentes en `tests/` y las fixtures de `tests/conftest.py`.

Reglas clave:

- Desarrollar por TDD: primero el test del caso asignado (Red), luego el código
  mínimo (Green) y después refactorizar. Registrar la evidencia real en
  `docs/REGISTRO_TDD.md`.
- Reutilizar `ServicioCompras`, `ResultadoCompra`, `MotivoRechazo` y las fixtures; no
  crear implementaciones paralelas.
- No usar skip ni xfail, no detectar pytest ni identificadores C01–C28 en el código.
- No inventar reglas de negocio (edades, precios, descuentos) que no estén acordadas.
- Ejecutar `python -m pytest -q`, `python -m ruff check .` y
  `python -m ruff format --check .` antes de integrar e informar los resultados
  realmente observados.
