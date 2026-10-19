"""C15 — Rechazo por fecha de visita ausente.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA01
- Tipo: Rechazo
- Condición: Fecha de visita ausente.
- Comportamiento esperado: Rechazar por falta de fecha de visita.
- Preparación sugerida: crear_solicitud(fecha_visita=None)
- Motivo esperado: MotivoRechazo.FECHA_AUSENTE

Tests previstos (nombres sugeridos):
- test_c15_rechaza_fecha_de_visita_ausente

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
