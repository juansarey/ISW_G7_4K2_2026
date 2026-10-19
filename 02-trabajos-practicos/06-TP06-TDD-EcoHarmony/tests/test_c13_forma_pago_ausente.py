"""C13 — Rechazo por forma de pago ausente.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA06
- Tipo: Rechazo
- Condición: Forma de pago ausente.
- Comportamiento esperado: Rechazar e identificar que falta seleccionar la forma de
  pago.
- Preparación sugerida: crear_solicitud(forma_pago=None)
- Motivo esperado: MotivoRechazo.FORMA_PAGO_AUSENTE

Tests previstos (nombres sugeridos):
- test_c13_rechaza_forma_de_pago_ausente

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
