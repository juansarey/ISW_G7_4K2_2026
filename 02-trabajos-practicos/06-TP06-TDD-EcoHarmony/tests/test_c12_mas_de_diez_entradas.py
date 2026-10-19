"""C12 — Rechazo por más de diez entradas.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA07
- Tipo: Rechazo
- Condición: Once entradas y once edades válidas.
- Comportamiento esperado: Rechazar por superar el máximo de diez entradas.
- Preparación sugerida: crear_solicitud(cantidad_entradas=11, edades=(30,) * 11)
- Motivo esperado: MotivoRechazo.CANTIDAD_EXCEDE_MAXIMO

Tests previstos (nombres sugeridos):
- test_c12_rechaza_mas_de_diez_entradas

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
