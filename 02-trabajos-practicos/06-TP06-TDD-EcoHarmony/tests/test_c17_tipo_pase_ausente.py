"""C17 — Rechazo por tipo de pase ausente.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA01
- Tipo: Rechazo
- Condición: Tipo de pase ausente.
- Comportamiento esperado: Rechazar por falta de selección del tipo de pase.
- Preparación sugerida: crear_solicitud(tipo_pase=None)
- Motivo esperado: MotivoRechazo.TIPO_PASE_AUSENTE

Tests previstos (nombres sugeridos):
- test_c17_rechaza_tipo_de_pase_ausente

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
