"""C28 — Edad inválida (DG04).

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: DG04
- Tipo: Rechazo (decisión del grupo)
- Condición: Edad negativa o no interpretable como entero; un dato por ejecución.
- Comportamiento esperado: Rechazar el dato inválido. No se impone un máximo de edad
  ni descuentos.
- Preparación sugerida: crear_solicitud(edades=(24, -1)) / convertir_solicitud con
  edad 'veinte'
- Motivo esperado: MotivoRechazo.EDAD_INVALIDA

Tests previstos (nombres sugeridos):
- test_c28_rechaza_edad_invalida

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
